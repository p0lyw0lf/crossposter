import { produce } from "solid-js/store";
import { resizeTextArea } from "../components/TextArea";
import { getFormElements, useComposerContext } from "./ComposerContext";

export interface Draft {
  draftId: string;
  title: string;
  body: string;
  tags: string[];
}

const allDraftsKey = "allDrafts";

const hasStringKeys = (a: any, ks: string[]): boolean => {
  return ks.every((k) => k in a && typeof a[k] === "string");
};

// Parses s as a JSON string containing a Draft. returns undefined if parsing fails.
const draftFromString = (s: string): Draft | undefined => {
  try {
    const draft = JSON.parse(s);
    if (
      hasStringKeys(draft, ["draftId", "title", "body"]) &&
      "tags" in draft &&
      Array.isArray(draft.tags) &&
      draft.tags.every((tag: any) => typeof tag === "string")
    ) {
      return draft;
    }
    return undefined;
  } catch {
    return undefined;
  }
};

export const draftFromFormData = (f: FormData): Draft | undefined => {
  const draftId = f.get("draftId")?.toString();
  if (!draftId) return undefined;
  const title = f.get("title")?.toString() || "untitled";
  const body = f.get("body")?.toString() || "empty";
  const tags = f.getAll("tags")?.map((tag) => tag.toString()) ?? [];
  return { draftId, title, body, tags };
};

export const populateFormFromDraft = (
  form: HTMLFormElement,
  draft: Draft,
): void => {
  const { draftId, title, body } = getFormElements(form);
  draftId.value = draft.draftId;
  title.value = draft.title;
  body.value = draft.body;

  resizeTextArea(title);
  resizeTextArea(body);

  // NOTE: tags must be restored separately
};

export const listDraftKeys = (): string[] => {
  return [
    ...new Set(
      (window.localStorage.getItem(allDraftsKey) ?? "").split(","),
    ).values(),
  ];
};

export const listDrafts = (): Draft[] => {
  const draftMappings = listDraftKeys().flatMap(
    (draftKey): Array<[string, Draft]> => {
      const draft = draftFromString(
        window.localStorage.getItem(draftKey) ?? "{}",
      );
      return draft ? [[draftKey, draft]] : [];
    },
  );

  const newDraftKeys = draftMappings.map(([draftKey]) => draftKey).join(",");
  window.localStorage.setItem(allDraftsKey, newDraftKeys);
  return draftMappings.map(([, draft]) => draft);
};

export const addDraft = (draft: Draft) => {
  window.localStorage.setItem(draft.draftId, JSON.stringify(draft));
  const draftKeys = new Set(listDraftKeys());
  draftKeys.add(draft.draftId);
  window.localStorage.setItem(allDraftsKey, [...draftKeys.values()].join(","));
};

export const removeDraft = (draftId: string) => {
  const draftKeys = new Set(listDraftKeys());
  draftKeys.delete(draftId);
  window.localStorage.setItem(allDraftsKey, [...draftKeys.values()].join(","));
};

// Creates a function that will save the current form into a draft.
// The returned function returns whether the save was successful.
export const useSaveDraft = (): (() => boolean) => {
  const { store, setStore } = useComposerContext();
  return () => {
    const data = new FormData(store.formRef);
    const draft = draftFromFormData(data);
    if (!draft) {
      setStore("message", "");
      setStore("error", "ERROR: something went wrong");
      return false;
    }

    addDraft(draft);
    setStore(
      "drafts",
      produce((drafts) => {
        const existingIndex = drafts.findIndex(
          (existingDraft) => existingDraft.draftId === draft.draftId,
        );
        if (existingIndex >= 0) {
          drafts[existingIndex] = draft;
        } else {
          drafts[drafts.length] = draft;
        }
      }),
    );

    return true;
  };
};

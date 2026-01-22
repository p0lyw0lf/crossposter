import { produce } from "solid-js/store";
import { resizeTextArea } from "../components/TextArea";
import { getFormElements, useComposerContext } from "./ComposerContext";

export interface Draft {
  draftId: string;
  title: string;
  body: string;
  tags: string[];
}

/** Returns whether the draft is empty. If it is, it should not be saved. */
export const isEmptyDraft = (draft: Draft): boolean => {
  return !draft.title && !draft.body && !draft.tags.length;
};

const hasStringKeys = (a: any, ks: string[]): boolean => {
  return ks.every((k) => k in a && typeof a[k] === "string");
};

/** Parses o as Draft object. Returns undefined if parsing fails. */
const draftFromObject = (o: unknown): Draft | undefined => {
  try {
    if (
      typeof o === "object" &&
      o !== null &&
      hasStringKeys(o, ["draftId", "title", "body"]) &&
      "tags" in o &&
      Array.isArray(o.tags) &&
      o.tags.every((tag: any) => typeof tag === "string")
    ) {
      return o as Draft;
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

const formDataFromDraft = (draft: Draft): FormData => {
  const formData = new FormData();
  formData.set("draftId", draft.draftId);
  formData.set("title", draft.title);
  formData.set("body", draft.body);
  for (const tag of draft.tags) {
    formData.append("tags", tag);
  }
  return formData;
};

export const listDrafts = async (
  setError: (err: string) => void,
): Promise<Draft[]> => {
  try {
    const response = await fetch("/drafts/list");
    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const drafts = await response.json();
    return Object.values(drafts)
      .map(draftFromObject)
      .filter((d) => d !== undefined);
  } catch (err) {
    setError(String(err));
    return [];
  }
};

/** Returns undefined if the fetch was unsuccessful for any reason. */
export const getDraft = async (draftId: string): Promise<Draft | undefined> => {
  try {
    const response = await fetch(`/drafts/by_id/${draftId}`);
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    const rawDraft = await response.json();
    return draftFromObject(rawDraft);
  } catch {
    // TODO: real error message here
    return undefined;
  }
};

/** Returns whether the upsert was successful. */
export const upsertDraft = async (draft: Draft): Promise<boolean> => {
  try {
    const formData = formDataFromDraft(draft);
    const response = await fetch(`/drafts/by_id/${draft.draftId}`, {
      body: formData,
      method: "PUT",
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    return true;
  } catch {
    // TODO: show proper error text
    return false;
  }
};

/** Returns whether the removal was successful. */
export const removeDraft = async (draftId: string): Promise<boolean> => {
  try {
    const response = await fetch(`/drafts/by_id/${draftId}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    return true;
  } catch {
    // TODO: real error reporting
    return false;
  }
};

// Creates a function that will save the current form into a draft.
// The returned function returns whether the save was successful.
export const useSaveDraft = (): (() => Promise<boolean>) => {
  const { store, setStore } = useComposerContext();
  return async (): Promise<boolean> => {
    const data = new FormData(store.formRef);
    const draft = draftFromFormData(data);
    if (!draft) {
      setStore("message", "");
      setStore("error", "ERROR: something went wrong");
      return false;
    }

    if (isEmptyDraft(draft)) {
      return false;
    }

    await upsertDraft(draft);
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

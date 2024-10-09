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
  const title = f.get("title")?.toString();
  if (!title) return undefined;
  const body = f.get("body")?.toString();
  if (!body) return undefined;
  const tags = f.getAll("tags")?.map((tag) => tag.toString());
  if (!tags) return undefined;
  return { draftId, title, body, tags };
};

export const listDraftKeys = (): string[] => {
  return [
    ...new Set(
      (window.localStorage.getItem(allDraftsKey) ?? "").split(",")
    ).values(),
  ];
};

export const listDrafts = (): Draft[] => {
  const draftMappings = listDraftKeys().flatMap(
    (draftKey): Array<[string, Draft]> => {
      const draft = draftFromString(
        window.localStorage.getItem(draftKey) ?? "{}"
      );
      return draft ? [[draftKey, draft]] : [];
    }
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

import type { Component } from "solid-js";
import { removeDraft, type Draft as DraftModel } from "./drafts";

export interface DraftProps {
  draft: DraftModel;
  formRef: HTMLFormElement;
  setTags: (tags: string[]) => void;
}

export const Draft: Component<DraftProps> = ({ draft, formRef, setTags }) => {
  return (
    <>
      <span>{draft.title}</span>
      <button
        onClick={() => {
          // NOTE: need to do this because typescript HATES elements
          const elements: any = formRef.elements;
          elements.draftId.value = draft.draftId;
          elements.title.value = draft.title;
          elements.body.value = draft.body;
          setTags(draft.tags);
        }}
      >
        load
      </button>
      <button
        onClick={() => {
          removeDraft(draft.draftId);
        }}
      >
        delete
      </button>
    </>
  );
};

import type { Component } from "solid-js";
import { populateFormFromDraft, removeDraft } from "./drafts";
import type { Draft as DraftModel } from "./drafts";
import styles from "./Draft.module.css";
import buttonStyles from "./Button.module.css";
import { useComposerContext } from "./ComposerContext";

export interface DraftProps {
  draft: DraftModel;
}

export const Draft: Component<DraftProps> = ({ draft }) => {
  const { store, setStore } = useComposerContext();
  return (
    <span class={styles.draft}>
      <span>{draft.title}</span>
      <button
        class={buttonStyles.button}
        onClick={() => {
          populateFormFromDraft(store.formRef, draft);
          setStore("tags", draft.tags);
        }}
      >
        load
      </button>
      <button
        class={buttonStyles.button}
        onClick={() => {
          removeDraft(draft.draftId);
          setStore("drafts", (drafts: DraftModel[]) =>
            drafts.filter((oldDraft) => draft.draftId !== oldDraft.draftId)
          );
        }}
      >
        delete
      </button>
    </span>
  );
};

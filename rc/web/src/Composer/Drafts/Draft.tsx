import type { Component } from "solid-js";
import buttonStyles from "../../components/Button.module.css";
import { useComposerContext } from "../ComposerContext";
import type { Draft as DraftModel } from "../drafts";
import { populateFormFromDraft, removeDraft } from "../drafts";
import styles from "./Draft.module.css";

export interface DraftProps {
  draft: DraftModel;
}

export const Draft: Component<DraftProps> = (props) => {
  const { store, setStore } = useComposerContext();
  return (
    <span class={styles.draft}>
      <span>{props.draft.title}</span>
      <button
        type="button"
        class={buttonStyles.button}
        onClick={() => {
          populateFormFromDraft(store.formRef, props.draft);
          setStore("tags", props.draft.tags);
        }}
      >
        load
      </button>
      <button
        type="button"
        class={buttonStyles.button}
        onClick={() => {
          removeDraft(props.draft.draftId);
          /* eslint-disable-next-line solid/reactivity */
          setStore("drafts", (drafts: DraftModel[]) =>
            drafts.filter(
              (oldDraft) => props.draft.draftId !== oldDraft.draftId,
            ),
          );
        }}
      >
        delete
      </button>
    </span>
  );
};

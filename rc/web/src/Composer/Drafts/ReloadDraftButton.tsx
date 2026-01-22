import type { Component } from "solid-js";
import buttonStyles from "../../components/Button.module.css";
import { resizeTextArea } from "../../components/TextArea";
import { getFormElements, useComposerContext } from "../ComposerContext";
import { getDraft, populateFormFromDraft } from "../drafts";

export const ReloadDraftButton: Component = () => {
  const { store, setStore } = useComposerContext();

  return (
    <button
      type="button"
      class={buttonStyles.button}
      onClick={async () => {
        const { draftId, title, body } = getFormElements(store.formRef);
        const draft = await getDraft(draftId.value, (error: string): void => {
          setStore("message", "");
          setStore("error", error);
        });

        if (!draft) {
          return;
        }

        populateFormFromDraft(store.formRef, draft);
        setStore("tags", draft.tags);

        resizeTextArea(title);
        resizeTextArea(body);

        setStore("message", "Draft reloaded successfully!");
        setStore("error", "");
      }}
    >
      reload draft
    </button>
  );
};

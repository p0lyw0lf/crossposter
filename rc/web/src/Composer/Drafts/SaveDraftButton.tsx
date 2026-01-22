import type { Component } from "solid-js";
import { Show } from "solid-js";
import { v7 as uuidv7 } from "uuid";
import buttonStyles from "../../components/Button.module.css";
import { resizeTextArea } from "../../components/TextArea";
import { getFormElements, useComposerContext } from "../ComposerContext";
import { populateFormFromDraft, useSaveDraft } from "../drafts";

interface Props {
  andCreateNewDraft: boolean;
}

export const SaveDraftButton: Component<Props> = (props: Props) => {
  const { store, setStore } = useComposerContext();
  const saveDraft = useSaveDraft();

  return (
    <button
      type="button"
      class={buttonStyles.button}
      onClick={async () => {
        if (!(await saveDraft())) {
          return;
        }

        if (props.andCreateNewDraft) {
          // Create fresh post so that further typing doesn't overwrite draft
          populateFormFromDraft(store.formRef, {
            draftId: uuidv7(),
            title: "",
            body: "",
            tags: [],
          });
          setStore("tags", []);
          const { title, body } = getFormElements(store.formRef);
          resizeTextArea(title);
          resizeTextArea(body);
        }

        setStore("message", "Draft saved successfully!");
        setStore("error", "");
      }}
    >
      <Show when={props.andCreateNewDraft} fallback={"save draft"}>
        new draft
      </Show>
    </button>
  );
};

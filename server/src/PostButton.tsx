import type { Component } from "solid-js";
import { createSignal } from "solid-js";
import { addDraft, draftFromFormData, populateFormFromDraft } from "./drafts";
import styles from "./PostButton.module.css";
import buttonStyles from "./components/Button.module.css";
import { useComposerContext } from "./ComposerContext";
import { produce } from "solid-js/store";
import { v7 as uuidv7 } from "uuid";

type Mode = "post" | "save-draft";

export const PostButton: Component = () => {
  const [mode, setMode] = createSignal<Mode>("post");
  const { store, setStore } = useComposerContext();

  const showError = (err: string) => {
    setStore("message", "");
    setStore("error", err);
  };

  const showMessage = (msg: string) => {
    setStore("message", msg);
    setStore("error", "");
  };

  const clear = () => {
    setStore("message", "");
    setStore("error", "");
  };

  const postButton = () => {
    switch (mode()) {
      case "post":
        clear();
        return (
          <button class={buttonStyles.button} type={"submit"}>
            post now
          </button>
        );
      case "save-draft":
        return (
          <button
            class={buttonStyles.button}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              const data = new FormData(store.formRef);
              const draft = draftFromFormData(data);
              if (!draft) {
                showError("ERROR: something went wrong.");
                return;
              }

              addDraft(draft);
              setStore(
                "drafts",
                produce((drafts) => {
                  const existingIndex = drafts.findIndex(
                    (existingDraft) => existingDraft.draftId === draft.draftId
                  );
                  if (existingIndex >= 0) {
                    drafts[existingIndex] = draft;
                  } else {
                    drafts[drafts.length] = draft;
                  }
                })
              );

              // Create fresh post so that further typing doesn't overwrite draft
              populateFormFromDraft(store.formRef, {
                draftId: uuidv7(),
                title: "",
                body: "",
                tags: [],
              });
              setStore("tags", []);

              showMessage("Draft saved successfully!");
            }}
          >
            save draft
          </button>
        );
    }
  };

  return (
    <div class={styles.container}>
      {postButton()}
      <button
        classList={{ [buttonStyles.button]: true, [styles.toggle]: true }}
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          setMode((prevMode) => {
            switch (prevMode) {
              case "post":
                return "save-draft";
              case "save-draft":
                return "post";
            }
          });
        }}
      >
        {"%"}
      </button>
    </div>
  );
};

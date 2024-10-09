import type { Component, JSXElement } from "solid-js";
import { createSignal } from "solid-js";
import { addDraft, draftFromFormData } from "./drafts";

import styles from "./PostButton.module.css";

interface Props {
  formRef: HTMLFormElement;
  showError: (error: string) => void;
  showMessage: (message: string) => void;
}

type Mode = "post" | "save-draft";

export const PostButton: Component<Props> = ({
  formRef,
  showError,
  showMessage,
}) => {
  const [mode, setMode] = createSignal<Mode>("post");

  const postButton = () => {
    switch (mode()) {
      case "post":
        showError("");
        showMessage("");
        return (
          <button class={styles.button} type={"submit"}>
            post now
          </button>
        );
      case "save-draft":
        return (
          <button
            class={styles.button}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              const data = new FormData(formRef);
              const draft = draftFromFormData(data);
              if (!draft) {
                showError(
                  "ERROR: something went wrong. Are you missing a field?"
                );
                showMessage("");
                return;
              }
              addDraft(draft);
              showError("");
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
        classList={{ [styles.button]: true, [styles.toggle]: true }}
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

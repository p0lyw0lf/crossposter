import type { Component } from "solid-js";
import { createSignal, createEffect, onCleanup } from "solid-js";
import { useSaveDraft, populateFormFromDraft } from "./drafts";
import styles from "./PostButton.module.css";
import buttonStyles from "./components/Button.module.css";
import { useComposerContext } from "./ComposerContext";
import { v7 as uuidv7 } from "uuid";

type Mode = "post" | "save-draft";

export const PostButton: Component = () => {
  const [mode, setMode] = createSignal<Mode>("post");
  const { store, setStore } = useComposerContext();
  const saveDraft = useSaveDraft();

  // Automatically save drafts every 30s
  createEffect(() => {
    let timeout: NodeJS.Timeout;
    const schedule = () => {
      saveDraft();
      timeout = setTimeout(schedule, 30_000);
    };
    timeout = setTimeout(schedule, 30_000);
    onCleanup(() => clearTimeout(timeout));
  });

  const postButton = () => {
    switch (mode()) {
      case "post":
        setStore("message", "");
        setStore("error", "");
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
              if (!saveDraft()) {
                return;
              }

              // Create fresh post so that further typing doesn't overwrite draft
              populateFormFromDraft(store.formRef, {
                draftId: uuidv7(),
                title: "",
                body: "",
                tags: [],
              });
              setStore("tags", []);

              setStore("message", "Draft saved successfully!");
              setStore("error", "");
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

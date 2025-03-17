import type { Component } from "solid-js";
import { Suspense } from "solid-js";
import { useComposerContext } from "../ComposerContext";
import { draftFromFormData } from "../drafts";
import { render } from "../renderer";
import { createResource } from "solid-js";
import styles from "./Preview.module.css";

export const Preview: Component = () => {
  const { store } = useComposerContext();

  const draft = draftFromFormData(new FormData(store.formRef));
  if (!draft) {
    return "ERROR: could not create draft";
  }

  const markdown = `# ${draft.title}\n\n${draft.body}`;
  const [html] = createResource(() => render(markdown));

  return (
    <Suspense fallback={<div class={styles.preview}>Loading...</div>}>
      <div class={styles.preview} innerHTML={html()} />
    </Suspense>
  );
};

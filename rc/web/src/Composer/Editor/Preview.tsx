import type { Component } from "solid-js";
import { createResource, Suspense } from "solid-js";
import { useComposerContext } from "../ComposerContext";
import { draftFromFormData } from "../drafts";
import { render } from "../renderer";
import styles from "./Preview.module.css";

export const Preview: Component = () => {
  const { store } = useComposerContext();

  const draft = draftFromFormData(new FormData(store.formRef));

  const markdown = () => (draft ? `# ${draft.title}\n\n${draft.body}` : null);
  const [html] = createResource(markdown, render);

  return (
    <Suspense fallback={<div class={styles.preview}>Loading...</div>}>
      {/* eslint-disable-next-line solid/no-innerhtml */}
      <div class={styles.preview} innerHTML={html()} />
    </Suspense>
  );
};

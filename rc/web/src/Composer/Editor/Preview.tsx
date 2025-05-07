import type { Component } from "solid-js";
import { createResource, For, Suspense } from "solid-js";
import { useComposerContext } from "../ComposerContext";
import { draftFromFormData } from "../drafts";
import { render } from "../renderer";
import styles from "./Preview.module.css";

export const Preview: Component = () => {
  const { store } = useComposerContext();

  const draft = draftFromFormData(new FormData(store.formRef));

  const markdown = () => (draft ? `# ${draft.title}\n\n${draft.body}` : null);
  const tags = () => (draft ? draft.tags : []);
  const [html] = createResource(markdown, render);

  return (
    <Suspense
      fallback={
        <div class={styles.preview}>
          <p>Loading...</p>
        </div>
      }
    >
      {/* eslint-disable-next-line solid/no-innerhtml */}
      <div class={styles.preview} innerHTML={html()} />
      {tags().length && (
        <div class={styles.tags}>
          <For each={tags()}>{(tag) => <span>#{tag}</span>}</For>
        </div>
      )}
    </Suspense>
  );
};

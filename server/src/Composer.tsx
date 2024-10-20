import { createEffect, Show } from "solid-js";
import type { Component } from "solid-js";
import { Tags } from "./Tags/Tags";
import { Toggle } from "./Toggle";
import { Textarea } from "./Textarea";
import { PostButton } from "./PostButton";
import { v7 as uuidv7 } from "uuid";
import styles from "./Composer.module.css";
import { DraftList } from "./DraftList";
import { listDrafts } from "./drafts";
import { createStore } from "solid-js/store";
import { ComposerProvider } from "./ComposerContext";

export const Composer: Component = () => {
  let formRef!: HTMLFormElement;

  const [store, setStore] = createStore({
    formRef,
    tags: [] as string[],
    message: "",
    error: "",
    drafts: listDrafts(),
  });

  createEffect(() => {
    setStore("formRef", formRef);
  });

  return (
    <ComposerProvider value={{ store, setStore }}>
      <form ref={formRef} class={styles.composer} action="/" method="post">
        <input type="hidden" name="draftId" value={uuidv7()} />
        <div class={styles.editor}>
          <Textarea
            class={styles.title}
            name="title"
            placeholder="headline"
            rows={1}
            required
          />
          <Textarea
            class={styles.body}
            name="body"
            placeholder="post body (accepts markdown!)"
            required
          />
          <Tags />
        </div>
        <div class={styles.toolbar}>
          <Toggle />
          <PostButton />
        </div>
      </form>
      <Show when={store.error}>
        <p classList={{ message: true, error: true }}>{store.error}</p>
      </Show>
      <Show when={store.message}>
        <p classList={{ message: true }}>{store.message}</p>
      </Show>
      <DraftList />
    </ComposerProvider>
  );
};

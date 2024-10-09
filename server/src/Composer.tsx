import { createSignal, Show } from "solid-js";
import type { Component } from "solid-js";
import { Tags } from "./Tags/Tags";
import { Toggle } from "./Toggle";
import { Textarea } from "./Textarea";
import { PostButton } from "./PostButton";
import { v7 as uuidv7 } from "uuid";

import styles from "./Composer.module.css";
import { DraftList } from "./DraftList";

export const Composer: Component = () => {
  let formRef: HTMLFormElement;

  const [message, setMessage] = createSignal("");
  const [error, setError] = createSignal("");

  const [tags, setTags] = createSignal<string[]>([]);

  return (
    <>
      <form ref={formRef!} class={styles.composer} action="/" method="post">
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
          <Tags tags={tags} setTags={setTags} />
        </div>
        <div class={styles.toolbar}>
          <Toggle />
          <PostButton
            formRef={formRef!}
            showError={setError}
            showMessage={setMessage}
          />
        </div>
      </form>
      <Show when={!!error()}>
        <p classList={{ message: true, error: true }}>{error()}</p>
      </Show>
      <Show when={!!message()}>
        <p classList={{ message: true }}>{message()}</p>
      </Show>
      <DraftList formRef={formRef!} setTags={setTags} />
    </>
  );
};

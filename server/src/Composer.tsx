import type { Component } from "solid-js";
import { Tags } from "./Tags/Tags";
import { Toggle } from "./Toggle";
import { Textarea } from "./Textarea";

import styles from "./Composer.module.css";

export const Composer: Component = () => {
  return (
    <form class={styles.composer} action="/" method="post">
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
        <button class={styles["submit-button"]} type="submit">
          post now
        </button>
      </div>
    </form>
  );
};

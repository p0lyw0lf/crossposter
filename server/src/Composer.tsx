import type { Component } from "solid-js";
import { Tags } from "./Tags";
import { Toggle } from "./Toggle";
import { Textarea } from "./Textarea";

import styles from "./Composer.module.css";

export const Composer: Component = () => {
  return (
    <div class={styles.composer}>
      <div class={styles.editor}>
        <Textarea
          class={styles.title}
          name="title"
          placeholder="headline"
          rows={1}
        />
        <Textarea name="body" placeholder="post body (accepts markdown!)" />
        <Tags />
      </div>
      <div class={styles.toolbar}>
        <Toggle />
        <button class={styles["submit-button"]}>post now</button>
      </div>
    </div>
  );
};

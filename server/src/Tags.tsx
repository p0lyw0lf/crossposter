import { createSignal, For, onMount, type Component } from "solid-js";
import { TextInput } from "./TextInput";

import styles from "./Tags.module.css";

export const Tags: Component = () => {
  let input: HTMLInputElement | undefined;
  const [tags, setTags] = createSignal<string[]>([]);

  onMount(() => {
    if (!input) return;

    input.addEventListener("keydown", (ev) => {
      console.log(ev.code);
      if (ev.code === "Enter" || ev.code === "Comma") {
        ev.stopPropagation();
        ev.preventDefault();
        setTags((tags) => [
          ...tags.filter((tag) => tag !== input.value),
          input.value,
        ]);
        input.value = "";
      }
      if (ev.code === "Backspace" && !input.value) {
        ev.stopPropagation();
        ev.preventDefault();
        setTags((tags) => tags.slice(0, -1));
      }
    });
  });

  return (
    <div class={styles["tag-list"]}>
      <For each={tags()}>
        {(tag) => (
          <span class={styles.tag}>
            <button
              onclick={() =>
                setTags((tags) => tags.filter((oldTag) => oldTag !== tag))
              }
            >
              x
            </button>
            {`#${tag}`}
          </span>
        )}
      </For>
      <TextInput ref={input} type="text" placeholder="#add tags" />
    </div>
  );
};

import { createSignal, For, onMount, type Component } from "solid-js";
import { TextInput } from "../TextInput";
import { Tag } from "./Tag";

import styles from "./Tags.module.css";

export const Tags: Component = () => {
  let input: HTMLInputElement | undefined;
  const [tags, setTags] = createSignal<string[]>([]);

  onMount(() => {
    if (!input) return;

    input.addEventListener("keydown", (ev) => {
      if (ev.code === "Enter" || ev.code === "Comma") {
        ev.stopPropagation();
        ev.preventDefault();
        if (!input.value) return;
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
          <Tag
            tag={tag}
            onClose={() =>
              setTags((tags) => tags.filter((oldTag) => oldTag !== tag))
            }
          />
        )}
      </For>
      <TextInput ref={input} type="text" placeholder="#add tags" />
    </div>
  );
};
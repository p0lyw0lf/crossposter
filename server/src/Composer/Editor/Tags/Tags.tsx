import type { Component } from "solid-js";
import { For, onMount } from "solid-js";
import { TextInput } from "../../../components/TextInput";
import { useComposerContext } from "../../ComposerContext";
import { Tag } from "./Tag";
import styles from "./Tags.module.css";

export const Tags: Component = () => {
  let input!: HTMLInputElement;

  const { store, setStore } = useComposerContext();

  onMount(() => {
    input.addEventListener("keydown", (ev) => {
      if (ev.code === "Enter" || ev.code === "Comma") {
        ev.stopPropagation();
        ev.preventDefault();
        if (!input.value) return;
        setStore("tags", (tags: string[]) => [
          ...tags.filter((tag) => tag !== input.value),
          input.value,
        ]);
        input.value = "";
      }
      if (ev.code === "Backspace" && !input.value) {
        ev.stopPropagation();
        ev.preventDefault();
        setStore("tags", (tags: string[]) => tags.slice(0, -1));
      }
    });
  });

  return (
    <div class={styles["tag-list"]}>
      <For each={store.tags}>
        {(tag) => (
          <Tag
            tag={tag}
            onClose={() =>
              setStore("tags", (tags: string[]) =>
                tags.filter((oldTag) => oldTag !== tag),
              )
            }
          />
        )}
      </For>
      <TextInput ref={input} type="text" placeholder="#add tags" />
    </div>
  );
};

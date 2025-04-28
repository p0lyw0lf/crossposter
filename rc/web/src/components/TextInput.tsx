import type { Component, JSX } from "solid-js";
import { onMount } from "solid-js";

export const TextInput: Component<JSX.InputHTMLAttributes<HTMLInputElement>> = (
  props,
) => {
  let input!: HTMLInputElement;
  onMount(() => {
    // Magic code from https://stackoverflow.com/a/25621277
    input.style.width = "9ch";
    input.style.width = input.scrollWidth + "px";
    input.style.overflowY = "hidden";

    input.addEventListener("input", () => {
      input.style.width = "9ch";
      input.style.width = input.scrollWidth + "px";
    });
  });

  return <input ref={input} {...props} />;
};

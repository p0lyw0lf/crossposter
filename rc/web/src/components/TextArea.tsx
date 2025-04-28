import type { Component, JSX } from "solid-js";
import { onMount } from "solid-js";

export const resizeTextArea = (textArea: HTMLTextAreaElement) => {
  // Magic code from https://stackoverflow.com/a/25621277
  const oldScrollX = window.scrollX;
  const oldScrollY = window.scrollY;

  textArea.style.height = "auto";
  textArea.style.height = textArea.scrollHeight + "px";

  window.scrollTo(oldScrollX, oldScrollY);
};

export const TextArea: Component<
  JSX.TextareaHTMLAttributes<HTMLTextAreaElement>
> = (props) => {
  let textarea!: HTMLTextAreaElement;
  onMount(() => {
    textarea.style.height = textarea.scrollHeight + "px";
    textarea.style.overflowY = "hidden";

    textarea.addEventListener("input", () => {
      resizeTextArea(textarea);
    });
  });

  return <textarea ref={textarea} {...props} />;
};

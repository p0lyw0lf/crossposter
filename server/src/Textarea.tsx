import { onMount, type Component } from "solid-js";
import type { JSX } from "solid-js";

export const Textarea: Component<
  JSX.TextareaHTMLAttributes<HTMLTextAreaElement>
> = (props) => {
  let textarea: HTMLTextAreaElement | undefined;
  onMount(() => {
    if (!textarea) return;
    // Magic code from https://stackoverflow.com/a/25621277
    textarea.style.height = textarea.scrollHeight + "px";
    textarea.style.overflowY = "hidden";

    textarea.addEventListener("input", () => {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    });
  });

  return <textarea ref={textarea} {...props} />;
};

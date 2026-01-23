import type { JSX, ParentComponent } from "solid-js";
import { children, onMount } from "solid-js";
import styles from "../Button.module.css";

interface Props extends JSX.InputHTMLAttributes<HTMLInputElement> {
  buttonClassList?: Record<string, boolean>;
}

export const FileInputButton: ParentComponent<Props> = (props) => {
  let inputRef!: HTMLInputElement;
  let buttonRef!: HTMLButtonElement;

  onMount(() => {
    // See https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications#using_hidden_file_input_elements_using_the_click_method
    buttonRef.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      inputRef.click();
    });
  });

  const safeChildren = children(() => props.children);

  return (
    <>
      <input
        style={{ display: "none" }}
        {...props}
        ref={inputRef}
        type="file"
      />
      <button
        ref={buttonRef}
        type="button"
        classList={{ [styles.button]: true, ...props.buttonClassList }}
      >
        {safeChildren()}
      </button>
    </>
  );
};

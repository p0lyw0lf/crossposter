import type { ParentComponent, JSX } from "solid-js";
import { children, onMount } from "solid-js";
import styles from "./Button.module.css";

interface Props extends JSX.InputHTMLAttributes<HTMLInputElement> {
  buttonClassList?: { [c in string]: boolean };
}

export const FileInput: ParentComponent<Props> = ({
  buttonClassList,
  children: propsChildren,
  ...props
}) => {
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

  const safeChildren = children(() => propsChildren);

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
        classList={{ [styles.button]: true, ...buttonClassList }}
      >
        {safeChildren()}
      </button>
    </>
  );
};

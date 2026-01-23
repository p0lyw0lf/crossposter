import { children, createSignal, ParentComponent, Show } from "solid-js";
import { useComposerContext } from "../../Composer/ComposerContext";
import styles from "./FileInputArea.module.css";

interface Props {
  onUploadFiles: (files: File[]) => void;
  classList?: { [k in string]: boolean | undefined };
}

export const FileInputArea: ParentComponent<Props> = (props) => {
  const { setStore } = useComposerContext();
  const [dragging, setDragging] = createSignal(false);

  const safeChildren = children(() => props.children);

  return (
    <div
      classList={{ ...props.classList, [styles.area]: true }}
      onDrop={(event) => {
        event.preventDefault();
        setDragging(false);

        // From https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
        if (!event.dataTransfer) return;
        let files: File[];
        if (event.dataTransfer.items) {
          files = [...event.dataTransfer.items]
            .filter((item) => item.kind === "file")
            .map((item) => item.getAsFile())
            .filter((file) => file !== null);
        } else {
          files = [...event.dataTransfer.files];
        }

        setStore("message", "Uploading...");

        props.onUploadFiles(files);
      }}
      onDragOver={(event) => {
        event.preventDefault();
      }}
      onDragEnter={() => {
        setDragging(true);
      }}
      onDragLeave={() => {
        // TODO: this caused flickering in the past, but seems to not now maybe?? hrm
        setDragging(false);
      }}
    >
      {safeChildren()}
      <Show when={dragging()}>
        <div class={styles.overlay}>drop to upload</div>
      </Show>
    </div>
  );
};

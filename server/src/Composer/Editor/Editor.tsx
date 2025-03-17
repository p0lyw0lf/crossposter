import type { Component } from "solid-js";
import { createSignal, Show } from "solid-js";
import { Tags } from "./Tags/Tags";
import { TextArea } from "../../components/TextArea";
import styles from "./Editor.module.css";
import { uploadFilesAndInsert } from "../fileUpload";
import { useComposerContext } from "../ComposerContext";
import { Preview } from "./Preview";

export const Editor: Component = () => {
  const { store, setStore } = useComposerContext();
  const [dragging, setDragging] = createSignal(false);
  return (
    <>
      <div
        class={styles.editor}
        style={store.preview ? { display: "none" } : undefined}
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

          uploadFilesAndInsert(store.formRef, files)
            .then((filenames) => {
              setStore("error", "");
              setStore("message", `Files uploaded to ${filenames.join(", ")}`);
            })
            .catch((err) => {
              setStore("error", `Error uploading file: ${err}`);
              setStore("message", "");
            });
        }}
        onDragOver={(event) => {
          event.preventDefault();
        }}
        onDragEnter={() => {
          setDragging(true);
          // NOTE: onDragLeave is set on the overlay, since that recieves the
          // drag events once it shows up
        }}
      >
        <TextArea
          class={styles.title}
          name="title"
          placeholder="headline"
          rows={1}
          required
        />
        <TextArea
          class={styles.body}
          name="body"
          placeholder="post body (accepts markdown!)"
          required
        />
        <Tags />
        <Show when={dragging()}>
          <div
            class={styles.overlay}
            onDragLeave={() => {
              setDragging(false);
            }}
          >
            Drop image to upload
          </div>
        </Show>
      </div>
      <Show when={store.preview}>
        <Preview />
      </Show>
    </>
  );
};

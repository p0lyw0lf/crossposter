import type { Component } from "solid-js";
import { createSignal, Show } from "solid-js";
import { Tags } from "./Tags/Tags";
import { resizeTextArea, TextArea } from "../components/TextArea";
import styles from "./Editor.module.css";
import { uploadFiles } from "../fileUpload";
import { getFormElements, useComposerContext } from "../ComposerContext";

export const Editor: Component = () => {
  const { store, setStore } = useComposerContext();
  const [dragging, setDragging] = createSignal(false);
  return (
    <div
      class={styles.editor}
      onDrop={(event) => {
        console.log("onDrop");
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

        setStore("error", "");
        setStore("message", "");

        const id = getFormElements(store.formRef).draftId.value;

        uploadFiles(id, files)
          .then((filenames) => {
            setStore("error", "");
            setStore("message", `files uploaded to ${filenames.join(", ")}`);

            const { body } = getFormElements(store.formRef);
            body.setRangeText(
              filenames
                .map((filename) => `<img src="${filename}" />`)
                .join("\n")
            );
            resizeTextArea(body);
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
  );
};

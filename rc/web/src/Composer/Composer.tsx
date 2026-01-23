import type { Component } from "solid-js";
import { For, Show } from "solid-js";
import { createStore } from "solid-js/store";
import { v7 as uuidv7 } from "uuid";
import { FileInputArea } from "../components/FileInput/FileInputArea";
import { FileInputButton } from "../components/FileInput/FileInputButton";
import styles from "./Composer.module.css";
import { ComposerProvider } from "./ComposerContext";
import { uploadFiles } from "./fileUpload";

export const Composer: Component = () => {
  const [store, setStore] = createStore({
    id: uuidv7(),
    message: "",
    error: "",
    uploadedFiles: [] as string[],
  });

  const onUploadFiles = (files: File[]) => {
    uploadFiles(store.id, files)
      .then((newFiles) => {
        setStore("error", "");
        setStore("message", `Files uploaded to ${newFiles.join(", ")}`);
        setStore("uploadedFiles", (existingFiles) => [
          ...existingFiles,
          ...newFiles,
        ]);
      })
      .catch((err) => {
        setStore("error", `Error uploading file: ${err}`);
        setStore("message", "");
      });
  };

  return (
    <ComposerProvider value={{ store, setStore }}>
      <FileInputArea
        onUploadFiles={onUploadFiles}
        classList={{ [styles.composer]: true }}
      >
        <FileInputButton
          multiple
          accept="image/*"
          onChange={(event) => {
            const files = event.target.files;
            if (files && files.length > 0) {
              setStore("message", "Uploading...");
              onUploadFiles([...files]);
            }
          }}
        >
          upload file
        </FileInputButton>
      </FileInputArea>
      <ul>
        <For each={store.uploadedFiles}>
          {(filename) => <li>{filename}</li>}
        </For>
      </ul>
      <Show when={store.error}>
        <p classList={{ message: true, error: true }}>
          {store.error}
          <button type="button" onClick={() => setStore("error", "")}>
            x
          </button>
        </p>
      </Show>
      <Show when={store.message}>
        <p classList={{ message: true }}>
          {store.message}
          <button type="button" onClick={() => setStore("message", "")}>
            x
          </button>
        </p>
      </Show>
    </ComposerProvider>
  );
};

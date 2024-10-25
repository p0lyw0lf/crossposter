import { createEffect, Show } from "solid-js";
import type { Component } from "solid-js";
import { Toggle } from "./Toggle";
import { PostButton } from "./PostButton";
import { v7 as uuidv7 } from "uuid";
import styles from "./Composer.module.css";
import { DraftList } from "./Drafts/DraftList";
import { listDrafts } from "./drafts";
import { createStore } from "solid-js/store";
import { ComposerProvider } from "./ComposerContext";
import { Editor } from "./Editor/Editor";
import { FileInput } from "./components/FileInput";
import { uploadFilesAndInsert } from "./fileUpload";

export const Composer: Component = () => {
  let formRef!: HTMLFormElement;

  const [store, setStore] = createStore({
    formRef,
    preview: false,
    tags: [] as string[],
    message: "",
    error: "",
    drafts: listDrafts(),
  });

  createEffect(() => {
    // NOTE: we need to make this reactive because, if it isn't, the base store
    // contains an undefined `formRef` despite our non-null assertion.
    setStore("formRef", formRef);
  });

  return (
    <ComposerProvider value={{ store, setStore }}>
      <form ref={formRef} class={styles.composer} action="/" method="post">
        <input type="hidden" name="draftId" value={uuidv7()} />
        <Editor />
        <div class={styles.toolbar}>
          <Toggle />
          <FileInput
            multiple
            accept="image/*"
            onChange={(event) => {
              const files = event.target.files;
              if (files && files.length > 0) {
                setStore("message", "Uploading...");
                uploadFilesAndInsert(formRef, [...files])
                  .then((filenames) => {
                    setStore("error", "");
                    setStore(
                      "message",
                      `Files uploaded to ${filenames.join(", ")}`
                    );
                  })
                  .catch((err) => {
                    setStore("error", `Error uploading file: ${err}`);
                    setStore("message", "");
                  });
              }
            }}
          >
            add attachment
          </FileInput>
          <PostButton />
        </div>
      </form>
      <Show when={store.error}>
        <p classList={{ message: true, error: true }}>{store.error}</p>
      </Show>
      <Show when={store.message}>
        <p classList={{ message: true }}>{store.message}</p>
      </Show>
      <DraftList />
    </ComposerProvider>
  );
};

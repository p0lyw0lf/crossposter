import type { Component } from "solid-js";
import { createEffect, createResource, Show } from "solid-js";
import { createStore } from "solid-js/store";
import { v7 as uuidv7 } from "uuid";
import { FileInput } from "../components/FileInput";
import styles from "./Composer.module.css";
import { ComposerProvider } from "./ComposerContext";
import { DraftList } from "./Drafts/DraftList";
import { Editor } from "./Editor/Editor";
import { PostButton } from "./PostButton";
import { Toggle } from "./Toggle";
import { listDrafts } from "./drafts";
import { uploadFilesAndInsert } from "./fileUpload";

export const Composer: Component = () => {
  let formRef!: HTMLFormElement;
  let setError!: (error: string) => void;

  const [drafts] = createResource(async () => listDrafts(setError));

  const [store, setStore] = createStore({
    formRef,
    preview: false,
    tags: [] as string[],
    message: "",
    error: "",
    drafts: drafts() ?? [],
  });
  setError = (error: string): void => {
    setStore("error", error);
  };

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
                      `Files uploaded to ${filenames.join(", ")}`,
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
        <button type="button" onClick={() => setStore("error", "")}>
          x
        </button>
      </Show>
      <Show when={store.message}>
        <p classList={{ message: true }}>
          {store.message}
          <button type="button" onClick={() => setStore("message", "")}>
            x
          </button>
        </p>
      </Show>
      <DraftList />
    </ComposerProvider>
  );
};

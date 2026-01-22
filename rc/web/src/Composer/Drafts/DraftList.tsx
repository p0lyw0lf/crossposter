import type { Component } from "solid-js";
import { createEffect, For, onCleanup } from "solid-js";
import { useComposerContext } from "../ComposerContext";
import { useSaveDraft } from "../drafts";
import type { DraftProps } from "./Draft";
import { Draft } from "./Draft";
import styles from "./DraftList.module.css";
import { SaveDraftButton } from "./SaveDraftButton";

export const DraftList: Component<Omit<DraftProps, "draft">> = (props) => {
  const { store } = useComposerContext();

  const saveDraft = useSaveDraft();

  // Automatically save drafts every 30s
  createEffect(() => {
    const schedule = () => {
      saveDraft();
      timeout = setTimeout(schedule, 30_000);
    };
    let timeout = setTimeout(schedule, 30_000);
    onCleanup(() => clearTimeout(timeout));
  });

  return (
    <>
      <ul class={styles.list}>
        <For each={store.drafts} fallback={<li>no drafts</li>}>
          {(draft) => (
            <li>
              <Draft {...props} draft={draft} />
            </li>
          )}
        </For>
      </ul>

      <div class={styles.buttonContainer}>
        <SaveDraftButton andCreateNewDraft={true} />
        <SaveDraftButton andCreateNewDraft={false} />
      </div>
    </>
  );
};

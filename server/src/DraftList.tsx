import type { Component } from "solid-js";
import { For } from "solid-js";
import type { DraftProps } from "./Draft";
import { Draft } from "./Draft";
import { useComposerContext } from "./ComposerContext";

export const DraftList: Component<Omit<DraftProps, "draft">> = (props) => {
  const { store } = useComposerContext();
  return (
    <ul>
      <For each={store.drafts} fallback={<li>no drafts</li>}>
        {(draft) => (
          <li>
            <Draft {...props} draft={draft} />
          </li>
        )}
      </For>
    </ul>
  );
};

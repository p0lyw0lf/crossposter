import type { Component } from "solid-js";
import { createSignal, Show, For } from "solid-js";
import { listDrafts } from "./drafts";
import type { DraftProps } from "./Draft";
import { Draft } from "./Draft";

export const DraftList: Component<Omit<DraftProps, "draft">> = (props) => {
  const [show, setShow] = createSignal(false);

  return (
    <Show
      when={show()}
      fallback={<button onClick={() => setShow(true)}>show drafts</button>}
    >
      <button onClick={() => setShow(false)}>hide drafts</button>
      <ul>
        <For each={listDrafts()} fallback={<p>no drafts</p>}>
          {(draft) => (
            <li>
              <Draft {...props} draft={draft} />
            </li>
          )}
        </For>
      </ul>
    </Show>
  );
};

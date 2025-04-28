import type { Component } from "solid-js";
import { Show } from "solid-js";
import styles from "./ClearFilterChip.module.css";
import type { FilterKey } from "./DBContext";
import { useDBContext } from "./DBContext";

interface Props {
  keyName: FilterKey;
}

export const ClearFilterChip: Component<Props> = (props) => {
  const { filters, setFilters } = useDBContext();

  const filter = () => filters[props.keyName];

  return (
    <Show when={!!filter()}>
      <button
        class={styles.chip}
        onClick={() => {
          setFilters(props.keyName, undefined);
        }}
      >
        {filter()}
      </button>
    </Show>
  );
};

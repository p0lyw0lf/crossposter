import type { Component } from "solid-js";
import styles from "./PagingControls.module.css";

interface Props {
  enableBack: boolean;
  firstPage: () => void;
  prevPage: () => void;
  page: number;
  numPages: number;
  nextPage: () => void;
  lastPage: () => void;
  enableForward: boolean;
}

export const PagingControls: Component<Props> = (props) => {
  return (
    <div class={styles.container}>
      <button disabled={!props.enableBack} onClick={props.firstPage}>
        ⟪
      </button>
      <button disabled={!props.enableBack} onClick={props.prevPage}>
        ‹
      </button>
      <span class={styles.count}>
        Page {props.page + 1} of {props.numPages}
      </span>
      <button disabled={!props.enableForward} onClick={props.nextPage}>
        ›
      </button>
      <button disabled={!props.enableForward} onClick={props.lastPage}>
        ⟫
      </button>
    </div>
  );
};

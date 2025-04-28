import type { Component } from "solid-js";

import styles from "./Tags.module.css";

interface Props {
  tag: string;
  onClose: () => void;
}

export const Tag: Component<Props> = (props) => {
  return (
    <>
      <input type="hidden" name="tags" value={props.tag} />
      <span class={styles.tag}>
        <button type="button" onClick={() => props.onClose()} />
        {props.tag}
      </span>
    </>
  );
};

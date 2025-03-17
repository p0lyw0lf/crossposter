import type { Component } from "solid-js";

import styles from "./Tags.module.css";

interface Props {
  tag: string;
  onClose: () => void;
}

export const Tag: Component<Props> = ({ tag, onClose }) => {
  return (
    <>
      <input type="hidden" name="tags" value={tag} />
      <span class={styles.tag}>
        <button type="button" onclick={onClose} />
        {tag}
      </span>
    </>
  );
};

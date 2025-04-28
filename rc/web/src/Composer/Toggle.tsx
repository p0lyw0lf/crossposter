import type { Component } from "solid-js";
import styles from "../components/Button.module.css";
import { useComposerContext } from "./ComposerContext";

export const Toggle: Component = () => {
  const { store, setStore } = useComposerContext();
  return (
    <div style={{ display: "flex", gap: "4px" }}>
      <button
        type="button"
        classList={{
          [styles.button]: true,
          [styles.secondary]: store.preview,
        }}
        onClick={() => {
          setStore("preview", false);
        }}
      >
        compose
      </button>
      <button
        type="button"
        classList={{
          [styles.button]: true,
          [styles.secondary]: !store.preview,
        }}
        onClick={() => {
          setStore("preview", true);
        }}
      >
        preview
      </button>
    </div>
  );
};

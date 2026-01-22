import type { Component } from "solid-js";
import buttonStyles from "../components/Button.module.css";

export const PostButton: Component = () => {
  return (
    <button type="submit" class={buttonStyles.button}>
      post now
    </button>
  );
};

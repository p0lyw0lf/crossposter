import type { Component } from "solid-js";
import { createEffect, createSignal } from "solid-js";

export const Dashboard: Component = () => {
  const [site, setSite] = createSignal("");

  createEffect(() => {
    const hiddenElem: HTMLInputElement | null = document.querySelector("#site");
    setSite(hiddenElem?.value ?? "");
  });

  return <h2>{site()}</h2>;
};

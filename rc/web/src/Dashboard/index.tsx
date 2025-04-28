/* @refresh reload */
import "vite/modulepreload-polyfill";

import { render } from "solid-js/web";
import { Dashboard } from "./Dashboard";
import "./index.css";

const root = document.getElementById("root");

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
  throw new Error(
    "Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?",
  );
}

render(() => <Dashboard />, root!);

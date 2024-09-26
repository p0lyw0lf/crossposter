import type { Component } from "solid-js";
import { Composer } from "./Composer";

import styles from "./App.module.css";

const App: Component = () => {
  return (
    <main class={styles.App}>
      <header>
        <h2>PolyWolf's Post Composer</h2>
      </header>
      <Composer />
      <footer>Have a nice day!!</footer>
    </main>
  );
};

export default App;

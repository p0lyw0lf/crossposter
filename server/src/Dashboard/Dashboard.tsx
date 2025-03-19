import type { Component } from "solid-js";
import {
  createEffect,
  createResource,
  createSignal,
  onCleanup,
  Show,
} from "solid-js";
import { DBProvider } from "./DBContext";
import { HitsPerDay } from "./HitsPerDay";
import { getConn, getDB } from "./duckdb";

export const Dashboard: Component = () => {
  const [loadingState, setLoadingState] = createSignal<string | null>(
    "Loading...",
  );
  const [site, setSite] = createSignal("");

  createEffect(() => {
    const hiddenElem: HTMLInputElement | null = document.querySelector("#site");
    setSite(hiddenElem?.value ?? "");
  });

  const uri = () =>
    site() ? `${window.location.origin}/log_files/${site()}.parquet` : null;

  const [conn] = createResource(uri, async (uri) => {
    setLoadingState("Initializing DuckDB...");
    const db = await getDB();
    setLoadingState("Downloading log files...");
    const conn = await getConn(db, uri);
    setLoadingState(null);
    return conn;
  });

  onCleanup(async () => {
    await conn()?.close();
  });

  return (
    <DBProvider value={{ conn }}>
      <Show when={!conn.loading} fallback={<h3>{loadingState()}</h3>}>
        <HitsPerDay />
      </Show>
    </DBProvider>
  );
};

import type { Component } from "solid-js";
import {
  createEffect,
  createResource,
  createSignal,
  onCleanup,
  Show,
} from "solid-js";
import { DBProvider } from "./DBContext";
import { getConn, getDB } from "./duckdb";
import { HitsPerDay } from "./HitsPerDay";
import { HitsPerReferrer } from "./HitsPerReferrer";
import { HitsPerStatus } from "./HitsPerStatus";
import { HitsPerUri } from "./HitsPerUri";

export const Dashboard: Component = () => {
  const [loadingState, setLoadingState] = createSignal<string | null>(
    "Loading...",
  );
  const [site, setSite] = createSignal<string | null>(null);

  createEffect(() => {
    const hiddenElem: HTMLInputElement | null = document.querySelector("#site");
    setSite(hiddenElem?.value ?? null);
  });

  const [conn] = createResource(site, async (site) => {
    setLoadingState("Initializing DuckDB...");
    const db = await getDB();
    setLoadingState("Downloading log files...");
    const uri = `${window.location.origin}/log_files/${site}.parquet`;
    const res = await fetch(uri);
    const buf = new Uint8Array(await res.arrayBuffer());
    setLoadingState("Creating table from logs...");
    const conn = await getConn(db, site, buf);
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
        <HitsPerUri />
        <HitsPerReferrer />
        <HitsPerStatus />
      </Show>
    </DBProvider>
  );
};

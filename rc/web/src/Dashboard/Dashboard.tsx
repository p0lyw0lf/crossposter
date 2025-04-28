import type { Component } from "solid-js";
import {
  createEffect,
  createResource,
  createSignal,
  onCleanup,
  Show,
} from "solid-js";
import { createStore } from "solid-js/store";
import { DBProvider } from "./DBContext";
import { getConn, getDB } from "./duckdb";
import { HitsPerDay } from "./HitsPerDay";
import { HitsPerReferrer } from "./HitsPerReferrer";
import { HitsPerStringKey } from "./HitsPerStringKey";
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
    const conn = await getConn(db, uri);
    setLoadingState(null);
    return conn;
  });

  onCleanup(async () => {
    await conn()?.close();
  });

  const [filters, setFilters] = createStore({});

  return (
    <DBProvider value={{ conn, filters, setFilters }}>
      <Show when={!conn.loading} fallback={<h3>{loadingState()}</h3>}>
        <HitsPerDay />
        <HitsPerUri />
        <HitsPerReferrer />
        <HitsPerStringKey colName="c-ip" keyName="IP" hasPaging />
        <HitsPerStringKey
          colName="cs(User-Agent)"
          keyName="UserAgent"
          hasPaging
          transformKey={{ toDisplay: decodeURI, fromDisplay: encodeURI }}
        />
        <HitsPerStringKey
          colName="sc-status"
          keyName="Status"
          hasPaging={false}
        />
      </Show>
    </DBProvider>
  );
};

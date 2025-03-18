import type { Component } from "solid-js";
import {
  createEffect,
  createSignal,
  createResource,
  onCleanup,
} from "solid-js";
import { DBProvider } from "./DBContext";
import { Table } from "./Table";
import { getConn, getDB } from "./duckdb";

export const Dashboard: Component = () => {
  const [site, setSite] = createSignal("");

  createEffect(() => {
    const hiddenElem: HTMLInputElement | null = document.querySelector("#site");
    setSite(hiddenElem?.value ?? "");
  });

  const uri = () =>
    site() ? `${window.location.origin}/log_files/${site()}.parquet` : null;

  const [conn] = createResource(uri, async (uri) => {
    console.log("getting db");
    const db = await getDB();
    console.log("getting conn");
    const conn = await getConn(db, uri);
    console.log("returning conn");
    return conn;
  });

  onCleanup(async () => {
    await conn()?.close();
  });

  return (
    <DBProvider value={{ conn }}>
      <Table />
    </DBProvider>
  );
};

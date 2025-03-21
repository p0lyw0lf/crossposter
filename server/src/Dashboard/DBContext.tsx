import type * as duckdb from "@duckdb/duckdb-wasm";
import type { ResourceReturn } from "solid-js";
import { createContext, useContext } from "solid-js";
import { SetStoreFunction } from "solid-js/store";

const filterKeys = [
  "Date",
  "URI",
  "Referrer",
  "IP",
  "UserAgent",
  "Status",
] as const;
export type FilterKey = (typeof filterKeys)[number];
export type FilterStore = { [k in FilterKey]?: string };

/**
 * Consumes the filter store, getting reactive updates for all the keys
 */
export const filtersToString = (filters: FilterStore): string => {
  return [
    ...filterKeys
      .map((key) => filters[key])
      .filter((f) => !!f)
      .map((f) => `(${f})`),
    "1 = 1",
  ].join(" AND ");
};

interface Context {
  conn: ResourceReturn<duckdb.AsyncDuckDBConnection>[0];
  filters: FilterStore;
  setFilters: SetStoreFunction<FilterStore>;
}
const DBContext = createContext<Context>();

// Same problem as I found earlier in ComposerContext: SolidJS _really_ doesn't deal well with these wrapper provider components for some reason, huh
export const DBProvider = DBContext.Provider;

interface FullContext extends Context {
  ctx: () => { conn: duckdb.AsyncDuckDBConnection; filters: string } | null;
}

export const useDBContext = (): FullContext => {
  const context = useContext(DBContext);
  if (context === undefined) {
    throw new Error("useDBContext must be used inside DBProvider");
  }

  const ctx = () => {
    const boundConn = context.conn();
    const filterString = filtersToString(context.filters);
    return boundConn ? { conn: boundConn, filters: filterString } : null;
  };

  return { ...context, ctx };
};

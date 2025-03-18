import type * as duckdb from "@duckdb/duckdb-wasm";
import type { ResourceReturn } from "solid-js";
import { createContext, useContext } from "solid-js";

interface DB {
  conn: ResourceReturn<duckdb.AsyncDuckDBConnection>[0];
}
const DBContext = createContext<DB>();

// Same problem as I found earlier in ComposerContext: SolidJS _really_ doesn't deal well with these wrapper provider components for some reason, huh
export const DBProvider = DBContext.Provider;

export const useDBContext = (): DB => {
  const context = useContext(DBContext);
  if (context === undefined) {
    throw new Error("useDBContext must be used inside DBProvider");
  }
  return context;
};

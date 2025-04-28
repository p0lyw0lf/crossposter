import * as duckdb from "@duckdb/duckdb-wasm";
import eh_worker from "@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url";
import mvp_worker from "@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url";
import duckdb_wasm_eh from "@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url";
import duckdb_wasm from "@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url";

const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
  mvp: {
    mainModule: duckdb_wasm,
    mainWorker: mvp_worker,
  },
  eh: {
    mainModule: duckdb_wasm_eh,
    mainWorker: eh_worker,
  },
};

export const getDB = async (): Promise<duckdb.AsyncDuckDB> => {
  // Select a bundle based on browser checks
  const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
  // Instantiate the asynchronous version of DuckDB-wasm
  const worker = new Worker(bundle.mainWorker!);
  const logger = new duckdb.ConsoleLogger();
  const db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  return db;
};

/**
 * Get a connection to the database backed by the Parquet file at `uri`. The
 * file's contents are loaded into the table "logs".
 *
 * MUST call `await c.close()` when this connection is no longer used.
 */
export const getConn = async (
  db: duckdb.AsyncDuckDB,
  uri: string,
): Promise<duckdb.AsyncDuckDBConnection> => {
  const c = await db.connect();
  await c.query(`
DROP TABLE IF EXISTS logs
`);
  await c.query(`
CREATE TABLE logs AS
  SELECT * from "${uri}"
`);
  return c;
};

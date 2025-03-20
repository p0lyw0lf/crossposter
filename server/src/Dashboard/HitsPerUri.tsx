import type * as arrow from "apache-arrow";
import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { LabelBarChart } from "./charts/LabelBarChart";
import { createPagingControls } from "./createPagingControls";
import { useDBContext } from "./DBContext";
import { PagingControls } from "./PagingControls";

export const HitsPerUri: Component = () => {
  const { conn } = useDBContext();

  const [uriCount] = createResource(conn, async (conn) => {
    const rows = await conn.query<{ count: arrow.Int }>(`
SELECT COUNT(DISTINCT "cs-uri-stem") as count
FROM logs
`);
    return Number(rows.get(0)?.count ?? 0);
  });

  const paging = createPagingControls(
    uriCount,
    () => 10,
    () => refetch(),
  );

  const [data, { refetch }] = createResource(conn, async (conn) => {
    const data = await conn.query(`
SELECT "cs-uri-stem" as uri, COUNT() as hits
FROM logs
GROUP BY uri
ORDER BY hits DESC
LIMIT ${paging.limit()}
OFFSET ${paging.offset()}
`);
    return (
      data
        ?.toArray()
        .map(({ uri, hits }) => ({ key: String(uri), value: Number(hits) })) ??
      []
    );
  });
  return (
    <>
      <h2>URI</h2>
      <PagingControls
        enableBack={paging.enableBack()}
        firstPage={paging.firstPage}
        prevPage={paging.prevPage}
        page={paging.page()}
        numPages={paging.numPages()}
        nextPage={paging.nextPage}
        lastPage={paging.lastPage}
        enableForward={paging.enableForward()}
      />
      <Show
        when={data.state === "ready" || data.state === "refreshing"}
        fallback={<h3>Querying...</h3>}
      >
        <LabelBarChart data={data()!} />
      </Show>
    </>
  );
};

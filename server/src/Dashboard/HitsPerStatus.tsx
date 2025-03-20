import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { LabelBarChart } from "./charts/LabelBarChart";
import { useDBContext } from "./DBContext";

export const HitsPerStatus: Component = () => {
  const { conn } = useDBContext();

  const [data] = createResource(conn, async (conn) => {
    const data = await conn.query(`
SELECT "sc-status" as status, COUNT() as hits
FROM logs
GROUP BY status
ORDER BY hits DESC
`);
    return (
      data
        ?.toArray()
        .map(({ status, hits }) => ({
          key: String(status),
          value: Number(hits),
        })) ?? []
    );
  });
  return (
    <>
      <h2>Status</h2>
      <Show
        when={data.state === "ready" || data.state === "refreshing"}
        fallback={<h3>Querying...</h3>}
      >
        <LabelBarChart data={data()!} />
      </Show>
    </>
  );
};

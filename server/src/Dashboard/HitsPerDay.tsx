import type * as arrow from "apache-arrow";
import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { useDBContext } from "./DBContext";
import { DateBarChart } from "./charts/DateBarChart";

export const HitsPerDay: Component = () => {
  const { conn } = useDBContext();

  const [data] = createResource(conn, async (conn) => {
    const data = await conn.query<{ date: arrow.Int; hits: arrow.Int }>(`
SELECT date, COUNT() as hits
FROM logs
GROUP BY date
ORDER BY date ASC
`);
    return (
      data?.toArray().map(({ date, hits }) => ({
        key: new Date(Number(date)),
        value: Number(hits),
      })) ?? []
    );
  });

  return (
    <>
      <h2>Date</h2>
      <Show
        when={data.state === "ready" || data.state === "refreshing"}
        fallback={<h3>Querying...</h3>}
      >
        <DateBarChart data={data()!} />
      </Show>
    </>
  );
};

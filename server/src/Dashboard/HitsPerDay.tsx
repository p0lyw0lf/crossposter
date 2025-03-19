import type * as arrow from "apache-arrow";
import { createResource, Show, type Component } from "solid-js";
import { useDBContext } from "./DBContext";
import { BarChart } from "./charts/BarChart";

export const HitsPerDay: Component = () => {
  const { conn } = useDBContext();

  const [data] = createResource(conn, async (conn) => {
    const data = await conn.query<{ date: arrow.Int; hits: arrow.Int }>(`
SELECT date, COUNT() as hits
FROM logs
GROUP BY date
ORDER BY date ASC
`);
    return data
      ?.toArray()
      .map(({ date, hits }) => ({
        key: new Date(Number(date)).toISOString(),
        hits: Number(hits),
      }));
  });

  return (
    <Show
      when={data.state === "ready" || data.state === "refreshing"}
      fallback={<h3>Querying...</h3>}
    >
      <BarChart data={data()!} />
    </Show>
  );
};

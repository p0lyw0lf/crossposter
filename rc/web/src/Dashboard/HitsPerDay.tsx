import type * as arrow from "apache-arrow";
import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { DateBarChart } from "./charts/DateBarChart";
import { ClearFilterChip } from "./ClearFilterChip";
import { useDBContext } from "./DBContext";

export const HitsPerDay: Component = () => {
  const { ctx, setFilters } = useDBContext();

  const [data] = createResource(ctx, async ({ conn, filters }) => {
    const data = await conn.query<{ date: arrow.Int; hits: arrow.Int }>(`
SELECT date, COUNT() as hits
FROM logs
WHERE ${filters}
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
      <h2>
        Date
        <ClearFilterChip keyName="Date" />
      </h2>
      <Show
        when={data.state === "ready" || data.state === "refreshing"}
        fallback={<h3>Querying...</h3>}
      >
        <DateBarChart
          data={data()!}
          onClickFactory={(key) => () => {
            setFilters("Date", `date = '${key.toISOString().slice(0, 10)}'`);
          }}
        />
      </Show>
    </>
  );
};

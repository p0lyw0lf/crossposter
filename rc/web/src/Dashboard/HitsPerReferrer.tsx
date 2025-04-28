import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { LabelBarChart } from "./charts/LabelBarChart";
import { ClearFilterChip } from "./ClearFilterChip";
import { createPagingControls } from "./createPagingControls";
import { useDBContext } from "./DBContext";
import { PagingControls } from "./PagingControls";

export const HitsPerReferrer: Component = () => {
  const { ctx, setFilters } = useDBContext();

  const [referrerCount] = createResource(ctx, async ({ conn, filters }) => {
    const rows = await conn.query(`
SELECT COUNT(DISTINCT SPLIT_PART("cs(Referer)", '/', 3)) as count
FROM logs
WHERE SPLIT_PART("cs(Referer)", '/', 3) != '' AND ${filters}
`);
    return Number(rows.get(0)?.count ?? 0);
  });

  const paging = createPagingControls(
    referrerCount,
    () => 10,
    () => refetch(),
  );

  const [data, { refetch }] = createResource(ctx, async ({ conn, filters }) => {
    const data = await conn.query(`
SELECT SPLIT_PART("cs(Referer)", '/', 3) as referrer, COUNT() as hits
FROM logs
WHERE referrer != '' AND ${filters}
GROUP BY referrer
ORDER BY hits DESC
LIMIT ${paging.limit()}
OFFSET ${paging.offset()}
`);
    return (
      data?.toArray().map(({ referrer, hits }) => ({
        key: String(referrer),
        value: Number(hits),
      })) ?? []
    );
  });
  return (
    <>
      <h2>
        Referrer
        <ClearFilterChip keyName="Referrer" />
      </h2>
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
        <LabelBarChart
          data={data()!}
          onClickFactory={(key) => () => {
            setFilters(
              "Referrer",
              `SPLIT_PART("cs(Referer)", '/', 3) = '${key}'`,
            );
          }}
        />
      </Show>
    </>
  );
};

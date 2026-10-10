import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { LabelBarChart } from "./charts/LabelBarChart";
import { ClearFilterChip } from "./ClearFilterChip";
import { createPagingControls } from "./createPagingControls";
import { useDBContext } from "./DBContext";
import { PagingControls } from "./PagingControls";

const REFERRER = `"cs(Referer)"`;
const REFERRER_HOST = `SPLIT_PART("cs(Referer)", '/', 3)`;

export const HitsPerReferrer: Component = () => {
  const { ctx, filters, setFilters } = useDBContext();

  const hasHost = () => filters["Referrer-Host"] !== undefined;
  const filterBy = () => (hasHost() ? REFERRER : REFERRER_HOST);

  // Wishing I had a simple `Option::map` right now...
  const ctxWithCol = () => {
    const maybeCtx = ctx();
    if (maybeCtx) return { ...maybeCtx, col: filterBy() };
    else return null;
  };

  const [referrerCount] = createResource(
    ctxWithCol,
    async ({ conn, filters, col }) => {
      const rows = await conn.query(`
SELECT COUNT(DISTINCT ${col}) as count
FROM logs
WHERE ${col} != '' AND ${filters}
`);
      return Number(rows.get(0)?.count ?? 0);
    },
  );

  const paging = createPagingControls(
    referrerCount,
    () => 10,
    () => refetch(),
  );

  const [data, { refetch }] = createResource(
    ctxWithCol,
    async ({ conn, filters, col }) => {
      const query = `
SELECT ${col} as referrer, COUNT() as hits
FROM logs
WHERE referrer != '' AND referrer != '-' AND ${filters}
GROUP BY referrer
ORDER BY hits DESC
LIMIT ${paging.limit()}
OFFSET ${paging.offset()}
`;
      const data = await conn.query(query);
      return (
        data?.toArray().map(({ referrer, hits }) => ({
          key: String(referrer),
          value: Number(hits),
        })) ?? []
      );
    },
  );
  return (
    <>
      <h2>
        Referrer
        <ClearFilterChip keyName="Referrer-Host" />
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
          onClickFactory={
            hasHost()
              ? (key) => () => {
                  setFilters("Referrer", `${REFERRER} = '${key}'`);
                }
              : (key) => () => {
                  setFilters("Referrer-Host", `${REFERRER_HOST} = '${key}'`);
                }
          }
        />
      </Show>
    </>
  );
};

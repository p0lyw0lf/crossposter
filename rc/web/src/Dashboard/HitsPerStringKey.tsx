import type * as arrow from "apache-arrow";
import type { Component } from "solid-js";
import { createResource, Show } from "solid-js";
import { LabelBarChart } from "./charts/LabelBarChart";
import { ClearFilterChip } from "./ClearFilterChip";
import { createPagingControls } from "./createPagingControls";
import type { FilterKey } from "./DBContext";
import { useDBContext } from "./DBContext";
import { PagingControls } from "./PagingControls";

interface Props {
  colName: string;
  keyName: FilterKey;
  hasPaging: boolean;
  transformKey?: {
    toDisplay: (key: string) => string;
    fromDisplay: (display: string) => string;
  };
}

export const HitsPerStringKey: Component<Props> = (props) => {
  const { ctx, setFilters } = useDBContext();

  const [count] = createResource(
    () => {
      if (!props.hasPaging) return null;
      const c = ctx();
      if (!c) return null;
      return { ctx: c, colName: props.colName };
    },
    async ({ ctx: { conn, filters }, colName }) => {
      const rows = await conn.query<{ count: arrow.Int }>(`
SELECT COUNT(DISTINCT "${colName}") as count
FROM logs
WHERE ${filters}
`);
      return Number(rows.get(0)?.count ?? 0);
    },
  );

  const paging = createPagingControls(
    count,
    () => 10,
    () => refetch(),
  );

  const [data, { refetch }] = createResource(
    () => {
      const c = ctx();
      if (!c) return null;
      return {
        ctx: c,
        colName: props.colName,
        keyName: props.keyName,
        transformKey: props.transformKey,
        page: props.hasPaging
          ? { limit: paging.limit(), offset: paging.offset() }
          : null,
      };
    },
    async ({
      ctx: { conn, filters },
      colName,
      keyName,
      transformKey,
      page,
    }) => {
      let query = `
SELECT "${colName}" as "${keyName}", COUNT() as hits
FROM logs
WHERE ${filters}
GROUP BY "${keyName}"
ORDER BY hits DESC
`;
      if (page) {
        query += `
LIMIT ${page.limit}
OFFSET ${page.offset}
`;
      }
      const rows = await conn.query(query);
      return (
        rows?.toArray().map((row) => {
          const key = String(row[keyName]);
          const value = Number(row.hits);
          return {
            key: transformKey?.toDisplay(key) ?? key,
            value,
          };
        }) ?? []
      );
    },
  );

  const [onClickFactory] = createResource(
    () => ({
      colName: props.colName,
      keyName: props.keyName,
      transformKey: props.transformKey,
    }),
    ({ colName, keyName, transformKey }) =>
      (key: string) =>
      () => {
        const realKey = transformKey?.fromDisplay(key) ?? key;
        setFilters(keyName, `"${colName}" = '${realKey}'`);
      },
  );

  return (
    <>
      <h2>
        {props.keyName}
        <ClearFilterChip keyName={props.keyName} />
      </h2>
      {props.hasPaging && (
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
      )}
      <Show
        when={data.state === "ready" || data.state === "refreshing"}
        fallback={<h3>Querying...</h3>}
      >
        <LabelBarChart data={data()!} onClickFactory={onClickFactory()} />
      </Show>
    </>
  );
};

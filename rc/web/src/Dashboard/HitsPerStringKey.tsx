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
    () => props.hasPaging && ctx(),
    async ({ conn, filters }) => {
      const rows = await conn.query<{ count: arrow.Int }>(`
SELECT COUNT(DISTINCT "${props.colName}") as count
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

  const [data, { refetch }] = createResource(ctx, async ({ conn, filters }) => {
    let query = `
SELECT "${props.colName}" as "${props.keyName}", COUNT() as hits
FROM logs
WHERE ${filters}
GROUP BY "${props.keyName}"
ORDER BY hits DESC
`;
    if (props.hasPaging) {
      query += `
LIMIT ${paging.limit()}
OFFSET ${paging.offset()}
`;
    }
    const rows = await conn.query(query);
    return (
      rows?.toArray().map((row) => {
        const key = String(row[props.keyName]);
        const value = Number(row.hits);
        return {
          key: props.transformKey?.toDisplay(key) ?? key,
          value,
        };
      }) ?? []
    );
  });
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
        <LabelBarChart
          data={data()!}
          onClickFactory={(key) => () => {
            const realKey = props.transformKey?.fromDisplay(key) ?? key;
            setFilters(props.keyName, `"${props.colName}" = '${realKey}'`);
          }}
        />
      </Show>
    </>
  );
};

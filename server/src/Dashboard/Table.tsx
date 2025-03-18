import type * as arrow from "apache-arrow";
import { createResource, For, Show, type Component } from "solid-js";
import { useDBContext } from "./DBContext";

export const Table: Component = () => {
  const { conn } = useDBContext();

  const [data] = createResource(conn, async (conn) => {
    console.log("querying table");
    const data = await conn.query<{ uri: arrow.Utf8; hits: arrow.Int }>(`
SELECT "cs-uri-stem" AS uri, COUNT() as hits
FROM logs
GROUP BY uri
ORDER BY hits DESC
LIMIT 10
`);
    console.log("got data", data.toArray());
    return data;
  });

  return (
    <Show when={data.state === "ready"} fallback={<h2>Loading...</h2>}>
      <ol>
        <For each={data()?.toArray() ?? []}>
          {({ uri, hits }) => (
            <li>
              {uri}: {String(hits)}
            </li>
          )}
        </For>
      </ol>
    </Show>
  );
};

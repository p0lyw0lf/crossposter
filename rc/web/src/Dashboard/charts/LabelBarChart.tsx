import * as d3 from "d3";
import { Component, createEffect, createMemo, For, Show } from "solid-js";

interface Datum {
  key: string;
  value: number;
}

interface Props {
  data: Array<Datum>;
  onClickFactory?: (key: string) => () => void;
}

const width = 800;
const height = 450;
const marginTop = 30;
const marginRight = 0;
const marginBottom = 30;
const marginLeft = 40;

export const LabelBarChart: Component<Props> = (props) => {
  const data = () => props.data;

  const x = createMemo(() =>
    d3
      .scaleLinear()
      .domain([0, d3.max(data(), (d) => d.value) ?? 1])
      .range([marginLeft, width - marginRight]),
  );

  const midpoint = (width - marginRight + marginLeft) / 2;

  const y = createMemo(() =>
    d3
      .scaleBand()
      .domain(d3.map(data(), (d) => d.key))
      .range([marginTop, height - marginBottom])
      .padding(0.1),
  );

  const yAxis = () => d3.axisLeft(y());

  const xAxis = () => d3.axisTop(x());

  let gx!: SVGGElement;
  let gy!: SVGGElement;

  createEffect(() => {
    // Append the axes
    d3.select(gx).call(xAxis());
    d3.select(gy).call(yAxis()).selectAll("text").remove();
  });

  return (
    <Show when={data().length > 0} fallback={<p>No Data</p>}>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        style={{ "max-width": "100%", height: "auto" }}
      >
        <g class="bars" fill="var(--color-text-primary-accent)">
          <For each={data()}>
            {(d) => (
              <rect
                onClick={props.onClickFactory?.(d.key)}
                x={x()(0)}
                y={y()(d.key)!}
                width={x()(d.value) - x()(0)}
                height={y().bandwidth()}
              />
            )}
          </For>
        </g>
        <g
          class="text"
          fill="var(--color-background-primary)"
          text-anchor="end"
        >
          <For each={data()}>
            {(d) => {
              const vx = x()(d.value);
              return (
                <text
                  onClick={props.onClickFactory?.(d.key)}
                  x={vx}
                  y={y()(d.key)! + y().bandwidth() / 2}
                  text-anchor={vx < midpoint ? "start" : undefined}
                  fill={vx < midpoint ? "var(--color-text-primary)" : undefined}
                  dy="0.35em"
                  dx={vx < midpoint ? 4 : -4}
                >
                  {d.key}
                </text>
              );
            }}
          </For>
        </g>
        <g ref={gx} class="x-axis" transform={`translate(0,${marginTop})`} />
        <g ref={gy} class="y-axis" transform={`translate(${marginLeft},0)`} />
      </svg>
    </Show>
  );
};

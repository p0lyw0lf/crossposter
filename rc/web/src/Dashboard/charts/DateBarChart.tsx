import * as d3 from "d3";
import { Component, createEffect, For, Show } from "solid-js";

interface Datum {
  key: Date;
  value: number;
}

interface Props {
  data: Array<Datum>;
  onClickFactory?: (key: Date) => () => void;
}

const width = 800;
const height = 450;
const marginTop = 30;
const marginRight = 0;
const marginBottom = 30;
const marginLeft = 40;

export const DateBarChart: Component<Props> = (props) => {
  const data = () => props.data;

  const x = () =>
    d3
      .scaleUtc()
      .domain([d3.min(data(), (d) => d.key)!, d3.max(data(), (d) => d.key)!])
      .range([marginLeft, width - marginRight]);

  const xAxis = () => d3.axisBottom(x()!);

  const y = () =>
    d3
      .scaleLinear()
      .domain([0, d3.max(data(), (d) => d.value) ?? 1])
      .range([height - marginBottom, marginTop]);

  const yAxis = () => d3.axisLeft(y());

  const barWidth = () =>
    ((width - marginRight - marginLeft) / data().length) * 0.95;

  let gx!: SVGGElement;
  let gy!: SVGGElement;

  createEffect(() => {
    // Append the axes
    d3.select(gx).call(xAxis());
    d3.select(gy)
      .call(yAxis())
      .call((g) => g.select(".domain").remove());
  });

  return (
    <Show when={data().length > 0} fallback={<p>No Data</p>}>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width={width}
        height={height}
        style={{ "max-width": "100%", height: "auto" }}
      >
        <g class="bars" fill="var(--color-text-secondary-accent)">
          <For each={data()}>
            {(d) => (
              <rect
                onClick={props.onClickFactory?.(d.key)}
                x={x()(d.key)}
                y={y()(d.value)}
                height={y()(0) - y()(d.value)}
                width={barWidth()}
              />
            )}
          </For>
        </g>
        <g
          ref={gx}
          class="x-axis"
          transform={`translate(0,${height - marginBottom})`}
        />
        <g ref={gy} class="y-axis" transform={`translate(${marginLeft},0)`} />
      </svg>
    </Show>
  );
};

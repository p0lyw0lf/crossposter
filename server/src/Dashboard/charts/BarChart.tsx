import * as d3 from "d3";
import {
  Component,
  createEffect,
  createResource,
  createSignal,
} from "solid-js";

interface Datum {
  key: string;
  hits: number;
}

interface Props {
  data: Array<Datum>;
}

const width = 800;
const height = 450;
const marginTop = 30;
const marginRight = 0;
const marginBottom = 30;
const marginLeft = 40;

// Currently heavily adapted from https://observablehq.com/@d3/zoomable-bar-chart
export const BarChart: Component<Props> = (props) => {
  const data = () => props.data;

  // TODO: figure out better ways to configure this, so we don't hardcode UTC
  const [x, { mutate: setX }] = createResource(data, (data) =>
    d3
      .scaleUtc()
      .domain([
        d3.min(data, (d) => new Date(d.key))!,
        d3.max(data, (d) => new Date(d.key))!,
      ])
      .range([marginLeft, width - marginRight]),
  );

  const xAxis = () => d3.axisBottom(x()!);

  const y = () =>
    d3
      .scaleLinear()
      .domain([0, d3.max(data(), (d) => d.hits) ?? 1])
      .range([height - marginBottom, marginTop]);

  const yAxis = () => d3.axisLeft(y());

  let svgElement!: SVGSVGElement;
  const [svg, setSvg] =
    createSignal<d3.Selection<SVGSVGElement, unknown, null, undefined>>();

  const zoom =
    () => (svg: d3.Selection<SVGSVGElement, unknown, null, undefined>) => {
      console.log("zoom");
      const extent: [[number, number], [number, number]] = [
        [marginLeft, marginTop],
        [width - marginRight, height - marginTop],
      ];
      svg.call(
        d3
          .zoom<SVGSVGElement, unknown>()
          .scaleExtent([1, Infinity])
          .translateExtent(extent)
          .extent(extent)
          .on("zoom", zoomed()),
      );
    };

  const zoomed = () => (event: d3.D3ZoomEvent<SVGSVGElement, Datum>) => {
    console.log("zoomed");
    setX(
      (x: d3.ScaleTime<number, number, never>) =>
        x.range(
          [marginLeft, width - marginRight].map((d) =>
            event.transform.applyX(d),
          ),
        ) as any,
    );
    svg()
      ?.selectAll(".bars rect")
      .attr("x", (d) => x()!(new Date((d as Datum).key)) ?? null)
      .attr("width", event.transform.applyX(20) - event.transform.applyX(0));
    svg()
      ?.selectAll(".x-axis")
      .call(xAxis() as any);
  };

  createEffect(() => {
    setSvg(d3.select(svgElement).call(zoom()));

    // Append the bars
    svg()
      ?.append("g")
      .attr("class", "bars")
      .attr("fill", "steelblue")
      .selectAll("rect")
      .data(data())
      .join("rect")
      .attr("x", (d) => x()!(new Date(d.key)))
      .attr("y", (d) => y()(d.hits))
      .attr("height", (d) => y()(0) - y()(d.hits))
      .attr("width", 20); // TODO: calculate correct width

    // Append the axes
    svg()
      ?.append("g")
      .attr("class", "x-axis")
      .attr("transform", `translate(0,${height - marginBottom})`)
      .call(xAxis());
    svg()
      ?.append("g")
      .attr("class", "y-axis")
      .attr("transform", `translate(${marginLeft},0)`)
      .call(yAxis())
      .call((g) => g.select(".domain").remove());
  });

  return (
    <svg
      ref={svgElement}
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      style={{ "max-width": "100%", height: "auto" }}
    />
  );
};

import type { BufferLevel } from "@/lib/buffersStore";
import type { BufferItem, Buffers, Buffer, K2470 } from "@/lib/ParamTreeType";
import type { DeviceBundle, Keithley2470Props } from "@/lib/types";
import { EndpointSlider, OdinGraph, type AdapterEndpoint } from "@dssg/odin-react";
import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import type Denque from "denque";
import type { Data, Layout } from "plotly.js";
import { useEffect, useState } from "react";
import { DropdownButton, Dropdown, Form, InputGroup, Container, Row, Col } from "react-bootstrap";

import uPlot, { type AlignedData, type Options } from 'uplot';
import UplotReact from "uplot-react";
import 'uplot/dist/uPlot.min.css';

const col = (arr, index) => arr.map((row) => row[index]);

const evenlySpaced = (arr, count = 6) => {
  if (arr.length <= count) return [...arr];
  return Array.from({ length: count }, (_, i) =>
    arr[Math.round((i * (arr.length - 1)) / (count - 1))]
  );
}

const toGraphData = (range: number, buffer: Denque<BufferItem>): AlignedData => {
  const lastItem = buffer.peekBack();
  const startTimestamp = Math.max(0, lastItem![0] - (range * 1_000_000));

  const graphDataX = [];
  const graphDataY = [];
  let i = -2;
  while (true) {
    const item = buffer.peekAt(i);
    if (!item || item[0] < startTimestamp) break;
    graphDataX.push(item[0]);
    graphDataY.push(item[2]);
    i--;
  }

  return [graphDataX.reverse(), graphDataY.reverse()]
};

export const BufferGraph = ({ buffers }: { buffers: Record<string, BufferLevel> }) => {
  const [selectedBufferName, setSelectedBufferName] = useState(Object.keys(buffers).at(0) ?? "");
  const selectedBuffer = buffers[selectedBufferName].buffer;
  const [range, setRange] = useState(10);

  if (selectedBuffer.length < 2) return <div>Hit start to begin acquisition</div>;

  const graphData: AlignedData = toGraphData(range, selectedBuffer);

  const graphOpts: Options = {
    width: 600,
    height: 800,
    scales: {
      x: {
        time: false,
      }
    },
    series: [
      {},
      {
        stroke: 'blue',
      }
    ]
  };
  //
  // const graphLayout: Partial<Layout> = {
  //   uirevision: "fixed",
  //   xaxis: {
  //     range: [
  //       col(selectedBuffer, 0).at(-1) - (range * 1_000_000),
  //       col(selectedBuffer, 0).at(-1),
  //     ]
  //   }
  // };
  //
  return (
    <div className="container-fluid p-3">
      <div className="row">
        <div className="col">
          {/*<OdinGraph data={graphData} layout={graphLayout} style={{ height: "auto" }} /> */}
          <UplotReact data={graphData} options={graphOpts} />
        </div>
      </div>
      <div className="row align-items-center">
        <div className="col-3 col-sm-4">
          <InputGroup>
            <InputGroup.Text>Show last</InputGroup.Text>
            <Form.Control value={range} onChange={(event) => setRange(parseFloat(event.target.value))} />
            <InputGroup.Text>s</InputGroup.Text>
          </InputGroup>
        </div>
        <div className="col">
          <Form.Range min={0} max={600} value={range} onChange={(event) => setRange(event.target.valueAsNumber)} />
        </div>
        <div className="col-auto">
          <Dropdown>
            <Dropdown.Toggle className="w-100">
              {selectedBufferName}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {Object.keys(buffers).map((name) =>
                <Dropdown.Item key={name} onClick={() => {
                  setSelectedBufferName(name);
                }}>{name}</Dropdown.Item>
              )}
            </Dropdown.Menu>
          </Dropdown>
        </div>
      </div>
    </div >
  );
}

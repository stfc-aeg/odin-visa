import type { Keithley2470Props } from "@/lib/types";
import { EndpointSlider, OdinGraph } from "@dssg/odin-react";
import type { Data, Layout } from "plotly.js";
import { useState } from "react";
import { DropdownButton, Dropdown, Form, InputGroup, Container, Row, Col } from "react-bootstrap";

const col = (arr, index) => arr.map((row) => row[index]);

const evenlySpaced = (arr, count = 6) => {
  if (arr.length <= count) return [...arr];
  return Array.from({ length: count }, (_, i) =>
    arr[Math.round((i * (arr.length - 1)) / (count - 1))]
  );
}

export const BufferGraph = ({ bundle }: Keithley2470Props) => {
  const buffers = bundle.device.acquisition.buffers;
  const [selectedBuffer, setSelectedBuffer] = useState(Object.keys(buffers)[0]);
  const [range, setRange] = useState(10);

  const selectedBufferData = buffers[selectedBuffer].buffer;

  const slicedGraphData = (x: number[], y: number[], range: number): Partial<Data> => {
    if (x.length == 0) {
      return { x: [], y: [] };
    }
    const lowerBound = x.at(-1)! - range;
    const lowerBoundIndex = x.findIndex((t) => t >= lowerBound);
    return {
      x: x.slice(lowerBoundIndex, -1),
      y: y.slice(lowerBoundIndex, -1),
    }
  }
  const graphData: Partial<Data>[] = [slicedGraphData(col(selectedBufferData, 0), col(selectedBufferData, 1), range * 1_000_000)];
  const unslicedGraphData: Partial<Data>[] = [{
    x: col(selectedBufferData, 0),
    y: col(selectedBufferData, 1),
  }];

  const tickvals = evenlySpaced(col(selectedBufferData, 0), 8);
  const ticktext = tickvals.map((val) => `${Math.floor(val / 1_000_000)}s`)

  const graphLayout: Partial<Layout> = {
    xaxis: {
      // rangeslider: {},
      tickvals: tickvals,
      ticktext: ticktext,
      range: [
        col(selectedBufferData, 0).at(-1) - (range * 1_000_000),
        col(selectedBufferData, 0).at(-1),
      ]
    }
  };

  return (
    <div className="container-fluid p-3">
      <div className="row">
        <div className="col">
          <OdinGraph data={unslicedGraphData} layout={graphLayout} style={{ height: "auto" }} />
        </div>
      </div>
      <div className="row align-items-center">
        <div className="col-3 col-sm-4">
          <InputGroup>
            <InputGroup.Text>Show last</InputGroup.Text>
            <Form.Control value={range} />
            <InputGroup.Text>s</InputGroup.Text>
          </InputGroup>
        </div>
        <div className="col">
          <Form.Range min={0} max={600} value={range} onChange={(event) => setRange(event.target.valueAsNumber)} />
        </div>
        <div className="col-2">
          <Dropdown>
            <Dropdown.Toggle className="w-100">
              {selectedBuffer}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {Object.keys(buffers).map((name) =>
                <Dropdown.Item key={name} onClick={() => setSelectedBuffer(name)}>{name}</Dropdown.Item>
              )}
            </Dropdown.Menu>
          </Dropdown>
        </div>
      </div>
    </div >
  );
}

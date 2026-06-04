import type { BufferItem, Buffers, Buffer, K2470 } from "@/lib/ParamTreeType";
import type { DeviceBundle, Keithley2470Props } from "@/lib/types";
import { EndpointSlider, OdinGraph, type AdapterEndpoint } from "@dssg/odin-react";
import { useInfiniteQuery, useQuery } from "@tanstack/react-query";
import type { Data, Layout } from "plotly.js";
import { useEffect, useState } from "react";
import { DropdownButton, Dropdown, Form, InputGroup, Container, Row, Col } from "react-bootstrap";

const col = (arr, index) => arr.map((row) => row[index]);

const evenlySpaced = (arr, count = 6) => {
  if (arr.length <= count) return [...arr];
  return Array.from({ length: count }, (_, i) =>
    arr[Math.round((i * (arr.length - 1)) / (count - 1))]
  );
}

// const useBuffersQuery = (bundle: DeviceBundle<K2470>, buffer: string) => {
//   return useInfiniteQuery({
//     queryKey: ["buffer", buffer],
//     queryFn: async ({ pageParam }) => {
//       await bundle.endpoint.put(pageParam, `${bundle.path}/acquisition/buffers/${buffer}/start_from`);
//       return bundle.device.acquisition.buffers[buffer].buffer;
//     },
//     initialPageParam: 0,
//     getNextPageParam: (lastPage, pages) => {
//       if (lastPage) {
//         return (lastPage.at(-1) ?? [0])[0]
//       }
//       else return 0;
//     },
//   })
// }

export const BufferGraph = ({ data }: { data: BufferItem[] }) => {
  const [range, setRange] = useState(10);

  if (!data) return <h1>Loading</h1>;

  // const { data, isLoading, isError, fetchNextPage } = useBuffersQuery(bundle, "full");
  // const [bufferData, setBufferData] = useState([]);
  // const buffers = bundle.device.acquisition.buffers;
  // const [selectedBuffer, setSelectedBuffer] = useState(Object.keys(buffers)[0]);
  // const selectedBufferData = buffers[selectedBuffer].buffer;
  //
  // // useEffect(() => {
  // //   const interval = setInterval(() => {
  // //     bundle.endpoint.put({ start_from: lastTimestamp }, `${bundle.path}/acquisition/buffers/${selectedBuffer}`);
  // //     setBufferData(bufferData.concat(selectedBufferData));
  // //     setLastTimestamp(selectedBufferData.at(-1)[0])
  // //   }, 1000);
  // //   return () => clearInterval(interval);
  // // }, [bufferData, bundle.endpoint, bundle.path, lastTimestamp, selectedBufferData]);
  //
  //
  //
  //
  // const slicedGraphData = (x: number[], y: number[], range: number): Partial<Data> => {
  //   if (x.length == 0) {
  //     return { x: [], y: [] };
  //   }
  //   const lowerBound = x.at(-1)! - range;
  //   const lowerBoundIndex = x.findIndex((t) => t >= lowerBound);
  //   return {
  //     x: x.slice(lowerBoundIndex, -1),
  //     y: y.slice(lowerBoundIndex, -1),
  //   }
  // }
  const graphData: Partial<Data>[] = [{ x: col(data, 0), y: col(data, 1) }];

  // const tickvals = evenlySpaced(col(bufferData, 0), 8);
  // const ticktext = tickvals.map((val) => `${Math.floor(val / 1_000_000)}s`)
  //
  const graphLayout: Partial<Layout> = {
    xaxis: {
      // rangeslider: {},
      range: [
        col(data, 0).at(-1) - (range * 1_000_000),
        col(data, 0).at(-1),
      ]
    }
  };
  //
  return (
    <div className="container-fluid p-3">
      <div className="row">
        <div className="col">
          <OdinGraph data={graphData} layout={graphLayout} style={{ height: "auto" }} />
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
        <div className="col-auto">
          {/*
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
        */}
        </div>
      </div>
    </div >
  );
}

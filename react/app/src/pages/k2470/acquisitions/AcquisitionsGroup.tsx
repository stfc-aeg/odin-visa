import type { BuffersEndpointProp, ControlEndpointProp } from "@/lib/types";
import { AcquisitionStatus } from "./AcquisitionStatus";
import { BufferGraph } from "./BufferGraph";
import { EndpointButton, EndpointInput } from "@dssg/odin-react";
import { useState } from "react";
import { Dropdown } from "react-bootstrap";
import { useQuery } from "@tanstack/react-query";
import type { BufferItem } from "@/lib/ParamTreeType";

export const AcquisitionsGroup = ({ control_endpoint, buffers_endpoint }: ControlEndpointProp & BuffersEndpointProp) => {
  const output = control_endpoint.data.acquisitions.output;
  const state = control_endpoint.data.acquisitions.status.state;
  const running = state == "RUNNING" || state == "WAITING";
  const buffers = buffers_endpoint.data.buffers;

  const [lastTimestamp, setLastTimestamp] = useState(0);
  const [selectedBufferName, setSelectedBufferName] = useState(Object.keys(buffers).at(0) ?? "");
  const [bufferData, setBufferData] = useState<Record<string, BufferItem[]>>({});
  const { data, isLoading, isError } = useQuery({
    queryKey: ["bufferData"],
    queryFn: async () => {
      const state = control_endpoint.data.acquisitions.status.state;

      if (state == "RUNNING" || state == "WAITING") {
        // only show buffer elements added since the last fetch
        await buffers_endpoint.put({ timestamp: lastTimestamp + 1 }, "start_from");
        // get the new data for the current buffer
        const new_data = await buffers_endpoint.get<Record<string, BufferItem[]>>(`buffers`);

        // get the timestamp of the last element in each buffer, and find the most recent
        const lastElementTimestamp = Math.max(...Object.values(new_data)
          .filter((buffer) => buffer.length != 0) // filter buffers that haven't been updated
          .map((buffer) => buffer.at(-1)![0]) // get the timestamp from the buffer
        );
        if (lastElementTimestamp) setLastTimestamp(lastElementTimestamp);

        // update all the buffers in the useState
        setBufferData((current) => {
          // create a copy of the buffers, required for react to detect state change
          const copy = { ...current };
          for (const key in new_data) {
            // set the buffer to the old data + new data
            copy[key] = [...(copy[key] ?? []), ...new_data[key]];
          }
          return copy;
        })
      }
      // return the full data state (as required by tanstack query)
      return bufferData;
    },
    refetchInterval: 1000,
    staleTime: 1000,
  })

  if (isLoading || isError || !data) return <h1>Loading Graph</h1>;

  return (
    <div className="container-fluid p-3">
      <div className="row">
        <div className="col">
          <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">Acquisition</h3>
        </div>
        <div className="col d-flex justify-content-end">
          <AcquisitionStatus control_endpoint={control_endpoint} />
        </div>
      </div>
      <div className="row">
        <div className="col-auto">
          <EndpointButton
            className={output ? "bg-primary" : "bg-secondary"}
            value={!output}
            endpoint={control_endpoint}
            fullpath="acquisitions/output"
          >
            Output {output ? "On" : "Off"}
          </EndpointButton>
        </div>
        <div className="col-auto">
          <div className="border h-100" />
        </div>
        <div className="col-auto">
          <EndpointButton
            className={`bg-success border-success ${running ? "disabled" : ""}`}
            endpoint={control_endpoint}
            fullpath="acquisitions/start"
            post_method={() => {
              setBufferData({});
              setLastTimestamp(0);
            }}
          >
            Start
          </EndpointButton>
        </div>
        <div className="col-auto">
          <EndpointButton
            className={`bg-danger border-danger ${!running ? "disabled" : ""}`}
            endpoint={control_endpoint}
            fullpath="acquisitions/stop"
          >
            Stop
          </EndpointButton>
        </div>
        <div className="col-auto">
          <EndpointInput endpoint={control_endpoint} fullpath="config/savefile/dataset_name" />
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
      <div className="row my-3">
        <div className="border w-100" />
      </div>
      <div className="row">
        <BufferGraph data={data[selectedBufferName]} />
      </div>
    </div>
  );
}

import type { BuffersEndpointProp, ConfigEndpointProp } from "@/lib/types";
import { AcquisitionStatus } from "./AcquisitionStatus";
import { BufferGraph } from "./BufferGraph";
import { EndpointButton, EndpointInput } from "@dssg/odin-react";
import { useState } from "react";
import { Dropdown, Form } from "react-bootstrap";
import { useQuery } from "@tanstack/react-query";
import type { BufferItem } from "@/lib/ParamTreeType";
import { useBufferStore } from "@/lib/buffersStore";

export const AcquisitionsGroup = ({ config_endpoint, buffers_endpoint }: ConfigEndpointProp & BuffersEndpointProp) => {
  const output = config_endpoint.data.acquisitions.output;
  const state = config_endpoint.data.acquisitions.status.state;
  const running = state == "RUNNING" || state == "WAITING";
  const buffers = useBufferStore((s) => s.buffers);
  const refreshTime = useBufferStore((s) => s.refreshTime);
  const setRefreshTime = useBufferStore((s) => s.setRefreshTime);
  const [draftRefreshTime, setDraftRefreshTime] = useState(refreshTime.toString());


  return (
    <div className="container-fluid p-3">
      <div className="row">
        <div className="col">
          <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">Acquisition</h3>
        </div>
        <div className="col d-flex justify-content-end">
          <AcquisitionStatus config_endpoint={config_endpoint} />
        </div>
      </div>
      <div className="row">
        <div className="col-auto">
          <EndpointButton
            className={output ? "bg-primary" : "bg-secondary"}
            value={!output}
            endpoint={config_endpoint}
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
            endpoint={config_endpoint}
            fullpath="acquisitions/start"
            post_method={() => {
              // setBufferData({});
              // setLastTimestamp(0);
            }}
          >
            Start
          </EndpointButton>
        </div>
        <div className="col-auto">
          <EndpointButton
            className={`bg-danger border-danger ${!running ? "disabled" : ""}`}
            endpoint={config_endpoint}
            fullpath="acquisitions/stop"
          >
            Stop
          </EndpointButton>
        </div>
        <div className="col-auto">
          <EndpointInput endpoint={config_endpoint} fullpath="config/savefile/dataset_name" />
        </div>
      </div>
      <div className="row my-3">
        <div className="border w-100" />
      </div>
      <div className="row my-3">
        <Form
          onSubmit={(e) => {
            e.preventDefault();
            setRefreshTime(parseFloat(draftRefreshTime));
          }}
        >
          <Form.Control
            value={draftRefreshTime}
            onChange={(e) => setDraftRefreshTime(e.target.value)}
          />
        </Form>
      </div>
      <div className="row">
        {buffers && Object.keys(buffers).length >= 2 &&
          <BufferGraph buffers={buffers} />
        }
      </div>
    </div>
  );
}

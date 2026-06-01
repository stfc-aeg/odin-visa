import type { Keithley2470Props } from "@/lib/types";
import { AcquisitionStatus } from "./AcquisitionStatus";
import { BufferGraph } from "./BufferGraph";
import { EndpointButton } from "@dssg/odin-react";

export const AcquisitionsGroup = ({ control_endpoint, buffers_endpoint }: Keithley2470Props) => {
  const output = control_endpoint.data.acquisitions.output;
  const state = control_endpoint.data.acquisitions.status.state;
  const running = state == "RUNNING" || state == "WAITING";

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
      </div>
      <div className="row my-3">
        <div className="border w-100" />
      </div>
      <div className="row">
        <BufferGraph buffers_endpoint={buffers_endpoint} control_endpoint={control_endpoint} />
      </div>
    </div>
  );
}

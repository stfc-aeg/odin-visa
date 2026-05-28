import type { Keithley2470Props } from "@/lib/types";
import { AcquisitionStatus } from "./AcquisitionStatus";
import { BufferGraph } from "./BufferGraph";
import { EndpointButton } from "@/lib/componentWithBundle";

export const AcquisitionsGroup = ({ bundle }: Keithley2470Props) => {
  const output = bundle.device.acquisition.output;
  const state = bundle.device.acquisition.status.state;
  const running = state == "RUNNING" || state == "WAITING";

  return (
    <div className="container-fluid p-3">
      <div className="row">
        <div className="col">
          <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">Acquisition</h3>
        </div>
        <div className="col d-flex justify-content-end">
          <AcquisitionStatus bundle={bundle} />
        </div>
      </div>
      <div className="row">
        <div className="col-auto">
          <EndpointButton
            className={output ? "bg-primary" : "bg-secondary"}
            value={!output}
            bundle={bundle}
            path="acquisition/output"
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
            bundle={bundle}
            path="acquisition/start"
          >
            Start
          </EndpointButton>
        </div>
        <div className="col-auto">
          <EndpointButton
            className={`bg-danger border-danger ${!running ? "disabled" : ""}`}
            bundle={bundle}
            path="acquisition/stop"
          >
            Stop
          </EndpointButton>
        </div>
      </div>
      <div className="row my-3">
        <div className="border w-100" />
      </div>
      <div className="row">
        <BufferGraph bundle={bundle} />
      </div>
    </div>
  );
}

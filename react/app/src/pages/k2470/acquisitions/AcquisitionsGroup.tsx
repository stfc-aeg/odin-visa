import type { Keithley2470Props } from "@/lib/types";
import { AcquisitionStatus } from "./AcquisitionStatus";
import { BufferGraph } from "./BufferGraph";
import { EndpointButton } from "@/lib/componentWithBundle";

export const AcquisitionsGroup = ({ bundle }: Keithley2470Props) => {
  const output = bundle.device.acquisition.output;
  const paused = bundle.device.acquisition.paused;
  const state = bundle.device.acquisition.status.state;
  const running = state == "RUNNING" || state == "WAITING";

  return (
    <div className="d-flex flex-column gap-2">
      <div className="d-flex justify-content-between">
        <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">Acquisition</h3>
        <AcquisitionStatus bundle={bundle} />
      </div>
      <div className="d-flex gap-3">
        <EndpointButton
          className={output ? "bg-primary" : "bg-secondary"}
          value={!output}
          bundle={bundle}
          path="acquisition/output"
        >
          Output {output ? "On" : "Off"}
        </EndpointButton>
        <div className="border" />
        <EndpointButton
          className={`bg-success border-success ${running ? "disabled" : ""}`}
          bundle={bundle}
          path="acquisition/start"
        >
          Start
        </EndpointButton>
        <EndpointButton
          className={`bg-danger border-danger ${!running ? "disabled" : ""}`}
          bundle={bundle}
          path="acquisition/stop"
        >
          Stop
        </EndpointButton>
        <EndpointButton
          className={paused ? "bg-secondary" : "bg-primary"}
          value={!paused}
          bundle={bundle}
          path="acquisition/paused"
        >
          {paused ? "Resume" : "Pause"}
        </EndpointButton>
      </div>
      <div>
        <BufferGraph bundle={bundle} />
      </div>
    </div>
  )
}

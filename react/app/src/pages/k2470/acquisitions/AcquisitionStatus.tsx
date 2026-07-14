import type { StatusType } from "@/lib/ParamTreeType";
import type { ConfigEndpointProp } from "@/lib/types";

export type TextColors = "text-primary" | "text-secondary" | "text-success" | "text-danger" | "text-warning" | "text-info";

const statusColorMap: Record<StatusType, TextColors> = {
  IDLE: "text-primary",
  RUNNING: "text-success",
  WAITING: "text-success",
  PAUSED: "text-warning",
  EMPTY: "text-secondary",
  BUILDING: "text-warning",
  FAILED: "text-danger",
  ABORTING: "text-danger",
  ABORTED: "text-danger",
};

export const AcquisitionStatus = ({ config_endpoint }: ConfigEndpointProp) => {
  return (
    <div className="d-flex gap-2">
      <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">Status:</h3>
      <h3 className={`
        text-uppercase fs-4 fw-bold mb-2 
        ${statusColorMap[config_endpoint.data.acquisitions.status.state]}
      `}>
        {config_endpoint.data.acquisitions.status.state}
      </h3>
    </div>
  )
}

import { TitleCard } from "@/components/TitleCard";
import type { BufferEndpointProp, ConfigEndpointProp } from "@/lib/types";
import { EndpointButton } from "@dssg/odin-react";
import { BufferGraph } from "./BufferGraph";

export interface AcquisitionsCardProps extends ConfigEndpointProp, BufferEndpointProp {
  acquiring: boolean;
}

export const AcquisitionsCard = ({ config_endpoint, buffer_endpoint, acquiring }: AcquisitionsCardProps) => {
  return (
    <TitleCard title="Acquisition">
      {config_endpoint.data.savefile.exists
        && config_endpoint.data.savefile.enable
        && !config_endpoint.data.acquisition.acquiring
        ? (
          <div className="alert alert-warning">
            <div className="row align-items-center">
              <div className="col">
                File already exists, cannot start acqusition.
              </div>
              <div className="col-auto">
                <EndpointButton
                  disabled={acquiring || !config_endpoint.data.savefile.enable}
                  className="btn-warning"
                  endpoint={config_endpoint}
                  fullpath="savefile/set_file_from_timestamp"
                >
                  Set From Current Time
                </EndpointButton>
              </div>
            </div>
          </div>
        ) :
        (
          <EndpointButton
            endpoint={config_endpoint}
            fullpath="acquisition/acquiring"
            className={acquiring ? "bg-danger" : "bg-success"}
            value={!acquiring}
          >
            {acquiring ? "Stop" : "Start"}
          </EndpointButton>
        )}
      <BufferGraph buffer_endpoint={buffer_endpoint} />
    </TitleCard>
  );
}

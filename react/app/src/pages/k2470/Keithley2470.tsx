import { hasData } from "@/lib/types";
import { useAdapterEndpoint, EndpointButton } from "@dssg/odin-react";
import { SourceSettingsGroup } from "./settings/SourceSettingsGroup";
import type { Buffer, Config } from "@/lib/ParamTreeType";
import { SaveFileSettingsGroup } from "./settings/SaveFileSettingsGroup";
import { SenseSettingsGroup } from "./settings/SenseSettingsGroup";
import { BufferGraph } from "./BufferGraph";
import { SettingsGroup } from "./settings/SettingsGroup";
import { OutputSettingsGroup } from "./settings/OutputSettingsGroup";
import { useErrorLog } from "@/lib/useErrorLog";

export const Keithley2470 = ({ name }: { name: string }) => {
  const config_endpoint = useAdapterEndpoint<Config>(`visa/devices/${name}/config`, import.meta.env.VITE_ENDPOINT_URL, 100);
  const buffers_endpoint = useAdapterEndpoint<Buffer>(`visa/devices/${name}/buffer`, import.meta.env.VITE_ENDPOINT_URL, 100);
  useErrorLog(name);

  if (!hasData(config_endpoint)) return <h1>Loading</h1>;
  if (!hasData(buffers_endpoint)) return <h1>Loading</h1>;

  const acquiring = config_endpoint.data.acquisition.acquiring

  return (
    <div className="container-fluid p-2 d-flex flex-column">
      <div className="row">
        <div className="col-lg">
          <div className="container-fluid p-3">
            <div className="row row-cols-1 gy-3">
              <div className="col">
                <SourceSettingsGroup disabled={acquiring} config_endpoint={config_endpoint} />
              </div>
              <div className="col">
                <SenseSettingsGroup disabled={acquiring} config_endpoint={config_endpoint} />
              </div>
              <div className="col">
                <OutputSettingsGroup disabled={acquiring} config_endpoint={config_endpoint} />
              </div>
            </div>
          </div>
        </div>
        <div className="col-lg p-3">
          <div className="mb-3">
            <SettingsGroup title="Acquisition">
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
              <BufferGraph buffer_endpoint={buffers_endpoint} />
            </SettingsGroup>
          </div>
          <SaveFileSettingsGroup disabled={acquiring} config_endpoint={config_endpoint} />
        </div>
      </div>
    </div>
  );
}

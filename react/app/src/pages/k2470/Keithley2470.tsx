import { hasData } from "@/lib/types";
import { useAdapterEndpoint, EndpointCheckbox } from "@dssg/odin-react";
import { SourceSettingsGroup } from "./settings/SourceSettingsGroup";
import type { Buffer, Config } from "@/lib/ParamTreeType";
import { SaveFileSettingsGroup } from "./settings/SaveFileSettingsGroup";
import { SenseSettingsGroup } from "./settings/SenseSettingsGroup";
import { BufferGraph } from "./BufferGraph";
import { SettingsGroup } from "./settings/SettingsGroup";
import { OutputSettingsGroup } from "./settings/OutputSettingsGroup";

export const Keithley2470 = ({ name }: { name: string }) => {
  const control_endpoint = useAdapterEndpoint<Config>(`visa/devices/${name}/config`, import.meta.env.VITE_ENDPOINT_URL, 500);
  const buffers_endpoint = useAdapterEndpoint<Buffer>(`visa/devices/${name}/buffer`, import.meta.env.VITE_ENDPOINT_URL, 500);

  if (!hasData(control_endpoint)) return <h1>Loading</h1>;
  if (!hasData(buffers_endpoint)) return <h1>Loading</h1>;

  return (
    <div className="container-fluid p-2 d-flex flex-column">
      <div className="row">
        <div className="col-lg">
          <div className="container-fluid p-3">
            <div className="row row-cols-1 gy-3">
              <div className="col">
                <SourceSettingsGroup control_endpoint={control_endpoint} />
              </div>
              <div className="col">
                <SenseSettingsGroup control_endpoint={control_endpoint} />
              </div>
              <div className="col">
                <OutputSettingsGroup control_endpoint={control_endpoint} />
              </div>
            </div>
          </div>
        </div>
        <div className="col-lg p-3">
          <div className="mb-3">
            <SettingsGroup title="Acquisition">
              {control_endpoint.data.savefile.exists && !control_endpoint.data.acquisition.acquiring ? (
                <div className="alert alert-warning">
                  File already exists, cannot start acqusition.
                </div>
              ) :
                (
                  <EndpointCheckbox
                    endpoint={control_endpoint}
                    fullpath="acquisition/acquiring"
                    label="Acquiring"
                  />
                )}
              <BufferGraph buffer_endpoint={buffers_endpoint} />
            </SettingsGroup>
          </div>
          <SaveFileSettingsGroup control_endpoint={control_endpoint} />
        </div>
      </div>
    </div>
  );
}

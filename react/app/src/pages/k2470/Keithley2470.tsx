import { hasData } from "@/lib/types";
import { useAdapterEndpoint } from "@dssg/odin-react";
import { SourceSettingsCard } from "./settings/SourceSettingsCard";
import type { Buffer, Config } from "@/lib/ParamTreeType";
import { SaveFileSettingsCard } from "./settings/SaveFileSettingsCard";
import { SenseSettingsCard } from "./settings/SenseSettingsCard";
import { OutputSettingsCard } from "./settings/OutputSettingsCard";
import { useErrorLog } from "@/lib/useErrorLog";
import { AcquisitionsCard } from "./acquisitions/AcquisitionsCard";

export const Keithley2470 = ({ name }: { name: string }) => {
  const config_endpoint = useAdapterEndpoint<Config>(`visa/devices/${name}/config`, import.meta.env.VITE_ENDPOINT_URL, 100);
  const buffers_endpoint = useAdapterEndpoint<Buffer>(`visa/devices/${name}/buffer`, import.meta.env.VITE_ENDPOINT_URL, 100);
  useErrorLog(name);

  if (!hasData(config_endpoint)) return <h1>Loading</h1>;
  if (!hasData(buffer_endpoint)) return <h1>Loading</h1>;

  const acquiring = config_endpoint.data.acquisition.acquiring

  return (
    <div className="container-fluid p-2 d-flex flex-column">
      <div className="row">
        <div className="col-lg">
          <div className="container-fluid p-3">
            <div className="row row-cols-1 gy-3">
              <div className="col">
                <SourceSettingsCard disabled={acquiring} config_endpoint={config_endpoint} />
              </div>
              <div className="col">
                <SenseSettingsCard disabled={acquiring} config_endpoint={config_endpoint} />
              </div>
              <div className="col">
                <OutputSettingsCard disabled={acquiring} config_endpoint={config_endpoint} />
              </div>
            </div>
          </div>
        </div>
        <div className="col-lg p-3">
          <div className="mb-3">
            <AcquisitionsCard acquiring={acquiring} config_endpoint={config_endpoint} buffer_endpoint={buffer_endpoint} />
          </div>
          <SaveFileSettingsCard disabled={acquiring} config_endpoint={config_endpoint} />
        </div>
      </div>
    </div>
  );
}

import { hasData } from "@/lib/types";
import { type AdapterEndpoint, useAdapterEndpoint, EndpointCheckbox, OdinGraph } from "@dssg/odin-react";
import { useEffect, useRef } from "react";
import { SourceSettingsGroup } from "./settings/SourceSettingsGroup";
import type { Buffers, Config } from "@/lib/ParamTreeType";
import { BufferPoll } from "@/lib/bufferPoll";
import { SaveFileSettingsGroup } from "./settings/SaveFileSettingsGroup";
import { SenseSettingsGroup } from "./settings/SenseSettingsGroup";
import { BufferGraph } from "./BufferGraph";
import { SettingsGroup } from "./settings/SettingsGroup";

export const Keithley2470 = ({ name }: { name: string }) => {
  const control_endpoint = useAdapterEndpoint<Config>(`visa/devices/${name}/config`, import.meta.env.VITE_ENDPOINT_URL, 1000);
  const buffers_endpoint = useAdapterEndpoint<Buffers>(`visa/devices/${name}/buffer`, import.meta.env.VITE_ENDPOINT_URL, 1000);
  // const eventLog = control_endpoint.data?.event_log;
  // const [errorCount, setErrorCount] = useState(eventLog?.count ?? 0);

  // const { setError } = useError();
  // useEffect(() => {
  //   if (eventLog && errorCount != eventLog.count) {
  //     setError(new Error(eventLog.last_event.message));
  //     setErrorCount(eventLog.count);
  //   }
  // }, [setError, errorCount, eventLog]);

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
                <SaveFileSettingsGroup control_endpoint={control_endpoint} />
              </div>
            </div>
          </div>
        </div>
        <div className="col-lg p-3">
          <SettingsGroup title="Acquisition">
            <EndpointCheckbox
              endpoint={control_endpoint}
              fullpath="acquisition/acquiring"
              label="Acquiring"
            />
            <BufferGraph buffer_endpoint={buffers_endpoint} />
          </SettingsGroup>
        </div>
      </div>
    </div>
  );
}

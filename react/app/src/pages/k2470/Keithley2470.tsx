import { hasData } from "@/lib/types";
import { type AdapterEndpoint, useAdapterEndpoint } from "@dssg/odin-react";
import { useEffect, useRef } from "react";
import { SourceSettingsGroup } from "./settings/SourceSettingsGroup";
import { AcquisitionsGroup } from "./acquisitions/AcquisitionsGroup";
import type { Buffers, Config } from "@/lib/ParamTreeType";
import { BufferPoll } from "@/lib/bufferPoll";
import { SaveFileSettingsGroup } from "./settings/SaveFileSettingsGroup";

export const Keithley2470 = ({ name }: { name: string }) => {
  const control_endpoint = useAdapterEndpoint<Config>(`visa/devices/${name}/config`, import.meta.env.VITE_ENDPOINT_URL, 1000);
  const buffers_endpoint = useAdapterEndpoint<Buffers>(`visa/devices/${name}/buffers`, import.meta.env.VITE_ENDPOINT_URL);
  // const eventLog = control_endpoint.data?.event_log;
  // const [errorCount, setErrorCount] = useState(eventLog?.count ?? 0);

  const buffersEndpointRef = useRef<Pick<AdapterEndpoint, "get" | "put">>({
    get: buffers_endpoint.get,
    put: buffers_endpoint.put,
  });
  buffersEndpointRef.current = {
    get: buffers_endpoint.get,
    put: buffers_endpoint.put,
  };

  const bufferPollRef = useRef<BufferPoll | null>(null);
  if (!bufferPollRef.current) {
    bufferPollRef.current = new BufferPoll({
      get: (...args) => buffersEndpointRef.current.get(...args),
      put: (...args) => buffersEndpointRef.current.put(...args),
    });
  }

  // const { setError } = useError();
  // useEffect(() => {
  //   if (eventLog && errorCount != eventLog.count) {
  //     setError(new Error(eventLog.last_event.message));
  //     setErrorCount(eventLog.count);
  //   }
  // }, [setError, errorCount, eventLog]);

  useEffect(() => {
    const bufferPoll = bufferPollRef.current;
    if (!bufferPoll) return;

    bufferPoll.start();

    return () => {
      bufferPoll.stop();
    }
  }, [])

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
                <SaveFileSettingsGroup control_endpoint={control_endpoint} />
              </div>
            </div>
          </div>
        </div>
        <div className="col-lg">
          {/* <AcquisitionsGroup buffers_endpoint={buffers_endpoint} control_endpoint={control_endpoint} /> */}
        </div>
      </div>
    </div>
  );
}

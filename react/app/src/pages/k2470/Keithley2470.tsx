import type { Keithley2470Props } from "@/lib/types";
import { useError } from "@dssg/odin-react";
import { useEffect, useState } from "react";
import { SourceSettingsGroup } from "./settings/SourceSettingsGroup";
import { AcquisitionsGroup } from "./acquisitions/AcquisitionsGroup";

export const Keithley2470 = ({ bundle }: Keithley2470Props) => {
  const eventLog = bundle.device.event_log;
  const [errorCount, setErrorCount] = useState(eventLog.count ?? 0);
  const { setError } = useError();

  useEffect(() => {
    if (errorCount != eventLog.count) {
      setError(new Error(eventLog.last_event.message));
      setErrorCount(eventLog.count);
    }
  }, [setError, errorCount, eventLog]);

  return (
    <div className="container-fluid p-2 d-flex flex-column">
      <div className="row">
        <div className="col-lg-3 col">
          <div className="container-fluid p-3">
            <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">
              Device Config
            </h3>
            <div className="row">
              <SourceSettingsGroup bundle={bundle} />
            </div>
          </div>
        </div>
        <div className="col-auto d-none d-xl-flex px-2">
          <div className="vr" />
        </div>
        <div className="col">
          <AcquisitionsGroup bundle={bundle} />
        </div>
      </div>
    </div>
  );
}

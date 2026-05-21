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
    <div className="d-flex flex-md-row flex-column-reverse flex-grow-1 overflow-hidden p-2 gap-4">
      <div className="d-flex flex-column col-md-4 gap-4 overflow-y-auto pe-2" style={{ minHeight: 0 }}>
        <h3 className="text-muted text-uppercase fs-4 fw-bold mb-2">Device Config</h3>
        <SourceSettingsGroup bundle={bundle} />
        {/*
        <GeneralSettingsGroup bundle={bundle} />
        <MeasurementSettingsGroup bundle={bundle} />
        <BufferSettingsGroup bundle={bundle} />
        */}
      </div>
      <div className="flex-grow-1 overflow-hidden">
        <AcquisitionsGroup bundle={bundle} />
      </div>
      {/*<div className="flex-grow-1 overflow-hidden">
        <BufferGraph
          title={device.trigger.buffer_name}
          data={device.trigger.buffer}
          currentModel={device.trigger.current_model}
        />
      </div>
      */}
    </div>
  );
}

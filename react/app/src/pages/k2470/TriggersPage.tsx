import { GeneralSettingsGroup } from "./settings/GeneralSettingsGroup";
import { SourceSettingsGroup } from "./settings/SourceSettingsGroup";
import { MeasurementSettingsGroup } from "./settings/MeasurementSettingsGroup";
import { SimpleLoopSettingsGroup } from "./settings/SimpleLoopSettingsGroup";
import { DurationLoopSettingsGroup } from "./settings/DurationLoopSettingsGroup";
import { LinearSweepSettingsGroup } from "./settings/LinearSweepOptions";
import { BufferSettingsGroup } from "./settings/BufferSettingsGroup";
import { BufferGraph } from "./settings/components/BufferGraph";
import { useError, type AdapterEndpoint } from "@dssg/odin-react";
import type { ParamTreeTypes } from "@/lib/ParamTreeType";
import { useEffect, useState } from "react";

export const TriggersPage = ({ endpoint }: { endpoint: AdapterEndpoint<ParamTreeTypes> }) => {
  const device = Object.values(endpoint.data.devices).find((d) => d.type);
  const [errorCount, setErrorCount] = useState(device?.error_count ?? 0);
  const { setError } = useError();

  useEffect(() => {
    if (device && errorCount != device.error_count) {
      setError(new Error(device?.last_error));
      setErrorCount(device.error_count);
    }
  }, [setError, device, errorCount]);

  if (!device) {
    return <h1>No device found</h1>;
  }

  return (
    <div className="d-flex flex-row flex-grow-1 overflow-hidden p-2 gap-4">
      <div className="d-flex flex-column col-4 gap-4 overflow-y-auto pe-2" style={{ minHeight: 0 }}>
        <GeneralSettingsGroup endpoint={endpoint} device={device} />
        <SourceSettingsGroup endpoint={endpoint} device={device} />
        <MeasurementSettingsGroup endpoint={endpoint} device={device} />
        <BufferSettingsGroup endpoint={endpoint} device={device} />

        {device.trigger.current_model === "SimpleLoop" && (
          <SimpleLoopSettingsGroup endpoint={endpoint} device={device} />
        )}

        {device.trigger.current_model === "DurationLoop" && (
          <DurationLoopSettingsGroup endpoint={endpoint} device={device} />
        )}

        {device.trigger.current_model === "LinearSweep" && (
          <LinearSweepSettingsGroup endpoint={endpoint} device={device} />
        )}
      </div>
      <div className="flex-grow-1 overflow-hidden">
        <BufferGraph
          title={device.trigger.buffer_name}
          data={device.trigger.buffer}
          currentModel={device.trigger.current_model}
        />
      </div>
    </div>
  );
};

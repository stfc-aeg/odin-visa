import { AveragingGroup } from "./components/AveragingGroup";
import type { K2470ComponentProps } from "@/lib/types";
import { SettingsGroup } from "@/pages/triggers/settings/SettingsGroup";
import { FunctionSelect } from "@/pages/triggers/settings/components/FunctionSelect";
import { SetButtonInput } from "@/pages/triggers/settings/components/SetButtonInput";

export const MeasurementSettingsGroup = ({ endpoint, device }: K2470ComponentProps) => {
  return (
    <SettingsGroup title="Measurement Settings">
      <FunctionSelect endpoint={endpoint} device={device} mode="sense" />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="NPLC per Measurement"
        value={device.sense.num_plcs}
        setFullpath="devices/K2470/sense/num_plcs"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Measurement Range"
        value={device.sense.range}
        setFullpath="devices/K2470/sense/range"
        unitPrefix={device.sense.function}
        toggleButton={{
          value: device.sense.auto_range,
          fullpath: "devices/K2470/sense/auto_range",
          disableInput: true,
          on: "Auto",
          off: "Fixed",
        }}
      />
      <SetButtonInput
        title="Measurement Count"
        value={device.sense.measurement_count}
        setFullpath="devices/K2470/sense/measurement_count"
        endpoint={endpoint}
        device={device}
      />
      <AveragingGroup
        averagingEnable={device.sense.averaging_enable}
        avgCount={device.sense.averaging_count}
        avgType={device.sense.averaging_type}
        endpoint={endpoint}
        originalAvgCount={device.sense.averaging_count}
      />
    </SettingsGroup>
  );
};

import { SettingsGroup } from "@/pages/triggers/settings/SettingsGroup";
import { SetButtonInput } from "@/pages/triggers/settings/components/SetButtonInput";
import type { K2470ComponentProps } from "@/lib/types";

export const DurationLoopSettingsGroup = ({ endpoint, device }: K2470ComponentProps) => {
  return (
    <SettingsGroup title="DurationLoop Settings">
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Duration"
        inputType="number"
        value={device.trigger.duration_loop.duration}
        setFullpath="devices/K2470/trigger/duration_loop/duration"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Measurement Delay (s)"
        value={device.trigger.duration_loop.delay}
        setFullpath="devices/K2470/trigger/duration_loop/delay"
      />
    </SettingsGroup>
  );
};

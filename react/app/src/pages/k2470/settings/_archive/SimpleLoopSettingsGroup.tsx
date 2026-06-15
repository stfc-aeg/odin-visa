import { SettingsGroup } from "@/pages/triggers/settings/SettingsGroup";
import { SetButtonInput } from "@/pages/triggers/settings/components/SetButtonInput";
import type { K2470ComponentProps } from "@/lib/types";

export const SimpleLoopSettingsGroup = ({ endpoint, device }: K2470ComponentProps) => {
  return (
    <SettingsGroup title="SimpleLoop Settings">
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Measurement Count"
        inputType="number"
        value={device.trigger.simple_loop.count}
        setFullpath="devices/K2470/trigger/buffer_name"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Measurement Delay (s)"
        value={device.trigger.simple_loop.delay}
        setFullpath="devices/K2470/trigger/simple_loop/delay"
      />
    </SettingsGroup>
  );
};

import { EndpointButton } from "@dssg/odin-react";
import { SetButtonInput } from "./components/SetButtonInput";
import { InputGroup } from "react-bootstrap";
import type { K2470ComponentProps } from "@/lib/types";
import { SettingsGroup } from "@/pages/triggers/settings/SettingsGroup";

export const LinearSweepSettingsGroup = ({ endpoint, device }: K2470ComponentProps) => {
  const rangeMode = device.trigger.linear_sweep.range_mode;

  return (
    <SettingsGroup title="LinearSweep Settings">
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Start"
        unitPrefix={device.source.function}
        value={device.trigger.linear_sweep.start}
        setFullpath="devices/K2470/trigger/linear_sweep/start"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Stop"
        unitPrefix={device.source.function}
        value={device.trigger.linear_sweep.stop}
        setFullpath="devices/K2470/trigger/linear_sweep/stop"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Count"
        value={device.trigger.linear_sweep.count}
        setFullpath="devices/K2470/trigger/linear_sweep/count"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Delay"
        value={device.trigger.linear_sweep.delay}
        setFullpath="devices/K2470/trigger/linear_sweep/delay"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Sweep Count"
        value={device.trigger.linear_sweep.sweep_count}
        setFullpath="devices/K2470/trigger/linear_sweep/sweep_count"
      />
      <InputGroup size="sm" className="flex-nowrap">
        <InputGroup.Text className="text-nowrap">Range Mode</InputGroup.Text>
        {["BEST", "FIXED", "AUTO"].map((mode) => (
          <EndpointButton
            key={mode}
            endpoint={endpoint}
            fullpath="devices/K2470/trigger/linear_sweep/range_mode"
            value={mode}
            variant={rangeMode === mode ? "primary" : "outline-primary"}
            size="sm"
            className="flex-fill"
          >
            {mode}
          </EndpointButton>
        ))}
      </InputGroup>
      <InputGroup size="sm" className="flex-nowrap">
        <InputGroup.Text className="text-nowrap">Dual Measure</InputGroup.Text>
        <EndpointButton
          endpoint={endpoint}
          fullpath="devices/K2470/trigger/linear_sweep/dual_measurement"
          value={!device.trigger.linear_sweep.dual_measurement}
          variant={device.trigger.linear_sweep.dual_measurement ? "success" : "danger"}
          size="sm"
          className="flex-fill"
        >
          {device.trigger.linear_sweep.dual_measurement ? "ON" : "OFF"}
        </EndpointButton>
      </InputGroup>
      <InputGroup size="sm" className="flex-nowrap">
        <InputGroup.Text className="text-nowrap">Fail Abort</InputGroup.Text>
        <EndpointButton
          endpoint={endpoint}
          fullpath="devices/K2470/trigger/linear_sweep/fail_abort"
          value={!device.trigger.linear_sweep.fail_abort}
          variant={device.trigger.linear_sweep.fail_abort ? "success" : "danger"}
          size="sm"
          className="flex-fill"
        >
          {device.trigger.linear_sweep.fail_abort ? "ON" : "OFF"}
        </EndpointButton>
      </InputGroup>
    </SettingsGroup>
  );
};

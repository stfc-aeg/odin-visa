import type { Keithley2470Props } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointDropdown, EndpointRangeInput } from "@/lib/componentWithBundle";
import { DropdownItem } from "react-bootstrap";

export const SourceSettingsGroup = ({ bundle }: Keithley2470Props) => {
  const source = bundle.device.config.source;
  const functionName = source.function === "VOLT" ? "Voltage" : "Current";
  const inverseFunctionName = source.function === "VOLT" ? "Current" : "Voltage";

  const voltageRanges = {
    nV: 1e-9,
    uV: 1e-6,
    mV: 1e-3,
    V: 1,
  };
  const currentRanges = {
    nA: 1e-9,
    uA: 1e-6,
    mA: 1e-3,
    A: 1,
  };

  return (
    <SettingsGroup title="Source Settings">
      <EndpointDropdown bundle={bundle} path="config/source/function">
        <DropdownItem eventKey={"VOLT"}>Voltage</DropdownItem>
        <DropdownItem eventKey={"CURR"}>Current</DropdownItem>
      </EndpointDropdown>
      <EndpointRangeInput
        bundle={bundle}
        path="config/source/level"
        defaultRange={functionName === "Voltage" ? "V" : "A"}
        ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
        title="Level"
      />
      <EndpointRangeInput
        bundle={bundle}
        path="config/source/limit"
        defaultRange={inverseFunctionName === "Voltage" ? "V" : "A"}
        ranges={inverseFunctionName === "Voltage" ? voltageRanges : currentRanges}
        title="Limit"
      />
    </SettingsGroup>
  );
};

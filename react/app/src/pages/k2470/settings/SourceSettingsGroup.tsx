import { PROTECTION_MODES, SOURCE_FUNCTIONS } from "@/lib/ParamTreeType";
import type { ConfigEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointCheckbox, EndpointDropdown, EndpointInput, EndpointRangeInput } from "@dssg/odin-react";
import { clsx } from "clsx";
import { DropdownItem, InputGroup } from "react-bootstrap";

export const SourceSettingsGroup = ({ disabled, config_endpoint }: ConfigEndpointProp) => {
  const source = config_endpoint.data.source;
  const functionName = source.function === "VOLTAGE" ? "Voltage" : "Current";
  const inverseFunctionName = source.function === "VOLTAGE" ? "Current" : "Voltage";

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
    <SettingsGroup disabled={disabled} title="Source Settings">
      <div className="row row-cols-1 align-items-center gy-2">
        <div className="col">
          <div className="row align-items-center gx-2">
            <div className="col">
              <InputGroup>
                <InputGroup.Text className={clsx(disabled && "text-secondary")}>
                  Source Function
                </InputGroup.Text>
                <EndpointDropdown
                  disabled={disabled}
                  endpoint={config_endpoint}
                  fullpath="source/function"
                >
                  {SOURCE_FUNCTIONS.map((mode) => (
                    <DropdownItem key={mode} eventKey={mode}>{mode}</DropdownItem>
                  ))}
                </EndpointDropdown>
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                disabled={disabled}
                endpoint={config_endpoint}
                fullpath="source/read_back"
                label="Source Read Back"
              />
            </div>
          </div>
        </div>
        <div className="col">
          <div className="row align-items-center gx-2">
            <div className="col">
              <InputGroup>
                <InputGroup.Text className={clsx(disabled && "text-secondary")}>
                  Protection Mode
                </InputGroup.Text>
                <EndpointDropdown
                  disabled={disabled}
                  id="protection-mode-dropdown"
                  aria-labelledby="protection-mode-label"
                  endpoint={config_endpoint}
                  fullpath="source/protection"
                >
                  {PROTECTION_MODES.map((mode) => (
                    <DropdownItem key={mode} eventKey={mode}>{mode}</DropdownItem>
                  ))}
                </EndpointDropdown>
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                disabled={disabled}
                endpoint={config_endpoint}
                fullpath="source/high_capacitance"
                label="High Capacitance Mode"
              />
            </div>
          </div>
        </div>
        <div className="col">
          <EndpointRangeInput
            disabled={disabled}
            endpoint={config_endpoint}
            fullpath="source/level"
            defaultRange={functionName === "Voltage" ? "V" : "A"}
            ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
            title="Level"
          />
        </div>
        <div className="col">
          <EndpointRangeInput
            disabled={disabled}
            endpoint={config_endpoint}
            fullpath="source/limit"
            defaultRange={inverseFunctionName === "Voltage" ? "V" : "A"}
            ranges={inverseFunctionName === "Voltage" ? voltageRanges : currentRanges}
            title="Limit"
          />
        </div>
        <div className="col">
          <div className="row align-items-center gx-2">
            <div className="col">
              <InputGroup>
                <EndpointRangeInput
                  endpoint={config_endpoint}
                  fullpath="source/range"
                  defaultRange={functionName === "Voltage" ? "V" : "A"}
                  ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
                  disabled={config_endpoint.data.source.auto_range || disabled}
                  title="Range"
                />
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                disabled={disabled}
                endpoint={config_endpoint}
                fullpath="source/auto_range"
                label="Auto"
              />
            </div>
          </div>
        </div>
        <div className="col">
          <div className="row align-items-center gx-2">
            <div className="col">
              <InputGroup>
                <InputGroup.Text className={clsx(disabled && "text-secondary")}>
                  Delay
                </InputGroup.Text>
                <EndpointInput
                  endpoint={config_endpoint}
                  fullpath="source/delay"
                  disabled={config_endpoint.data.source.auto_delay || disabled}
                />
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                disabled={disabled}
                endpoint={config_endpoint}
                fullpath="source/auto_delay"
                label="Auto"
              />
            </div>
          </div>
        </div>
      </div>
    </SettingsGroup>
  );
};

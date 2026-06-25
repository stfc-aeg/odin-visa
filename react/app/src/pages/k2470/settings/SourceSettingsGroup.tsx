import { PROTECTION_MODES, SOURCE_FUNCTIONS } from "@/lib/ParamTreeType";
import type { ControlEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointCheckbox, EndpointDropdown, EndpointInput, EndpointRangeInput } from "@dssg/odin-react";
import { DropdownItem, InputGroup } from "react-bootstrap";

export const SourceSettingsGroup = ({ control_endpoint }: ControlEndpointProp) => {
  const source = control_endpoint.data.source;
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
      <div className="row row-cols-1 align-items-center gy-2">
        <div className="col">
          <div className="row align-items-center gx-2">
            <div className="col">
              <InputGroup>
                <InputGroup.Text>
                  Source Function
                </InputGroup.Text>
                <EndpointDropdown endpoint={control_endpoint} fullpath="source/function">
                  {SOURCE_FUNCTIONS.map((mode) => (
                    <DropdownItem key={mode} eventKey={mode}>{mode}</DropdownItem>
                  ))}
                </EndpointDropdown>
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                endpoint={control_endpoint}
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
                <InputGroup.Text>
                  Protection Mode
                </InputGroup.Text>
                <EndpointDropdown
                  id="protection-mode-dropdown"
                  aria-labelledby="protection-mode-label"
                  endpoint={control_endpoint}
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
                endpoint={control_endpoint}
                fullpath="source/high_capacitance"
                label="High Capacitance Mode"
              />
            </div>
          </div>
        </div>
        <div className="col">
          <EndpointRangeInput
            endpoint={control_endpoint}
            fullpath="source/level"
            defaultRange={functionName === "Voltage" ? "V" : "A"}
            ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
            title="Level"
          />
        </div>
        <div className="col">
          <EndpointRangeInput
            endpoint={control_endpoint}
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
                  endpoint={control_endpoint}
                  fullpath="source/range"
                  defaultRange={functionName === "Voltage" ? "V" : "A"}
                  ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
                  disabled={control_endpoint.data.source.auto_range}
                  title="Range"
                />
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                endpoint={control_endpoint}
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
                <InputGroup.Text>
                  Delay
                </InputGroup.Text>
                <EndpointInput
                  endpoint={control_endpoint}
                  fullpath="source/delay"
                  disabled={control_endpoint.data.source.auto_delay}
                />
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                endpoint={control_endpoint}
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

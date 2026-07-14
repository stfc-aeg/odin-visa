import { AVERAGING_MODES, SENSE_FUNCTIONS } from "@/lib/ParamTreeType";
import type { ConfigEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointButton, EndpointCheckbox, EndpointDropdown, EndpointInput, EndpointRangeInput } from "@dssg/odin-react";
import { DropdownItem, InputGroup } from "react-bootstrap";

export const SenseSettingsGroup = ({ config_endpoint }: ConfigEndpointProp) => {
  const sense = config_endpoint.data.sense;
  const functionName = sense.function === "VOLTAGE" ? "Voltage" : "Current";

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
    <SettingsGroup title="Sense Settings">
      <div className="row row-cols-1 align-items-center gy-2">
        <div className="col">
          <div className="row align-items-center gy-2">
            <div className="col">
              <InputGroup>
                <InputGroup.Text>
                  Sense Function
                </InputGroup.Text>
                <EndpointDropdown endpoint={config_endpoint} fullpath="sense/function">
                  {SENSE_FUNCTIONS.map((func) => (
                    <DropdownItem key={func} eventKey={func}>{func}</DropdownItem>
                  ))}
                </EndpointDropdown>
              </InputGroup>
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                endpoint={config_endpoint}
                fullpath="sense/auto_zero"
                label="Auto Zero"
              />
            </div>
            <div className="col-auto">
              <EndpointButton
                endpoint={config_endpoint}
                fullpath="sense/zero"
                disabled={sense.auto_zero}
              >
                Zero
              </EndpointButton>
            </div>
          </div>
        </div>
        <div className="col">
          <EndpointCheckbox
            endpoint={config_endpoint}
            fullpath="sense/averaging"
            label="Averaging Enable"
          />
        </div>
        <div className="col">
          <div className="row row-cols-2 align-items-center gy-2">
            <div className="col">
              <InputGroup>
                <InputGroup.Text>
                  Averaging Count
                </InputGroup.Text>
                <EndpointInput
                  endpoint={config_endpoint}
                  fullpath="sense/averaging_count"
                  disabled={!sense.averaging}
                />
              </InputGroup>
            </div>
            <div className="col">
              <InputGroup>
                <InputGroup.Text>
                  Averaging Filter
                </InputGroup.Text>
                <EndpointDropdown endpoint={config_endpoint} fullpath="sense/averaging_filter" disabled={!sense.averaging}>
                  {AVERAGING_MODES.map((filter) => (
                    <DropdownItem key={filter} eventKey={filter}>{filter}</DropdownItem>
                  ))}
                </EndpointDropdown>
              </InputGroup>
            </div>
          </div>
        </div>
        <div className="col">
          <EndpointCheckbox
            endpoint={config_endpoint}
            fullpath="sense/offset_compensation"
            label="Offset Compensation"
          />
        </div>
        <div className="col">
          <div className="row row-cols-2 align-items-center gy-2">
            <div className="col-auto">
              <EndpointCheckbox
                endpoint={config_endpoint}
                fullpath="sense/auto_range"
                label="Enable Auto Range"
              />
            </div>
            <div className="col-auto">
              <EndpointCheckbox
                endpoint={config_endpoint}
                fullpath="sense/auto_range_rebound"
                label="Auto Range Rebound"
                disabled={!sense.auto_range}
              />
            </div>
          </div>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Auto Range Lower Limit
            </InputGroup.Text>
            <EndpointInput
              endpoint={config_endpoint}
              fullpath="sense/auto_range_lower_limit"
              disabled={!sense.auto_range}
            />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Auto Range Upper Limit
            </InputGroup.Text>
            <EndpointInput
              endpoint={config_endpoint}
              fullpath="sense/auto_range_upper_limit"
              disabled={true}
            />
          </InputGroup>
        </div>
        <div className="col">
          <EndpointRangeInput
            endpoint={config_endpoint}
            fullpath="sense/range"
            defaultRange={functionName === "Voltage" ? "V" : "A"}
            ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
            title="Range"
            disabled={sense.auto_range}
          />
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              NPLCs
            </InputGroup.Text>
            <EndpointInput
              endpoint={config_endpoint}
              fullpath="sense/nplcs"
            />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Measurement Count
            </InputGroup.Text>
            <EndpointInput
              endpoint={config_endpoint}
              fullpath="sense/count"
            />
          </InputGroup>
        </div>
        <div className="col">
          <EndpointCheckbox
            endpoint={config_endpoint}
            fullpath="sense/relative_offset"
            label="Enable Relative Offset"
          />
        </div>
        <div className="col">
          <div className="row align-items-center">
            <div className="col">
              <EndpointRangeInput
                endpoint={config_endpoint}
                fullpath="sense/relative_offset_level"
                defaultRange={functionName === "Voltage" ? "V" : "A"}
                ranges={functionName === "Voltage" ? voltageRanges : currentRanges}
                title="Relative Offset Level"
                disabled={!sense.relative_offset}
              />
            </div>
            <div className="col-auto">
              <EndpointButton
                endpoint={config_endpoint}
                fullpath="sense/acquire_relative_offset"
                disabled={!sense.relative_offset}
              >
                Set As Current Level
              </EndpointButton>
            </div>
          </div>
        </div>
        <div className="col">
          <EndpointCheckbox
            endpoint={config_endpoint}
            fullpath="sense/remote_sensing"
            label="Enable Remote Sensing"
          />
        </div>
      </div>
    </SettingsGroup >
  );
};

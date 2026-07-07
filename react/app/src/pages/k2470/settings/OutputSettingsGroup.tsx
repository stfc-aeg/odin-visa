import type { ControlEndpointProp } from "@/lib/types"
import { SettingsGroup } from "./SettingsGroup"
import { DropdownItem, InputGroup } from "react-bootstrap";
import { EndpointCheckbox, EndpointDropdown } from "@dssg/odin-react";
import { SOURCE_MODES, TERMINALS } from "@/lib/ParamTreeType";

export const OutputSettingsGroup = ({ control_endpoint }: ControlEndpointProp) => {
  return (
    <SettingsGroup title="Output Settings">
      <div className="row row-cols-1 align-items-center gy-2">
        <div className="col">
          <EndpointCheckbox
            endpoint={control_endpoint}
            fullpath="output/enabled"
            label="Enable Output"
          />
        </div>
        <div className="col">
          <div className="row row-cols-2">
            <div className="col">
              <EndpointCheckbox
                endpoint={control_endpoint}
                fullpath="output/interlock"
                label="Enable Interlock"
              />
            </div>
            <div className="col">
              <EndpointCheckbox
                endpoint={control_endpoint}
                fullpath="output/interlock_tripped"
                className="disabled"
                label="Interlock Tripped"
              />
            </div>
          </div>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Disabled Output Source Mode
            </InputGroup.Text>
            <EndpointDropdown endpoint={control_endpoint} fullpath="output/smode">
              {SOURCE_MODES.map((func) => (
                <DropdownItem key={func} eventKey={func}>{func}</DropdownItem>
              ))}
            </EndpointDropdown>
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Terminals
            </InputGroup.Text>
            <EndpointDropdown endpoint={control_endpoint} fullpath="output/terminals">
              {TERMINALS.map((func) => (
                <DropdownItem key={func} eventKey={func}>{func}</DropdownItem>
              ))}
            </EndpointDropdown>
          </InputGroup>
        </div>
      </div>
    </SettingsGroup >
  );
}

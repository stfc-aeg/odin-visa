import type { ConfigEndpointProp } from "@/lib/types"
import { TitleCard } from "@/components/TitleCard";
import { DropdownItem, InputGroup } from "react-bootstrap";
import { EndpointCheckbox, EndpointDropdown } from "@dssg/odin-react";
import { SOURCE_MODES, TERMINALS } from "@/lib/ParamTreeType";
import { clsx } from "clsx";

export const OutputSettingsCard = ({ disabled, config_endpoint }: ConfigEndpointProp) => {
  return (
    <TitleCard disabled={disabled} title="Output Settings">
      <div className="row row-cols-1 align-items-center gy-2">
        <div className="col">
          <EndpointCheckbox
            disabled={disabled}
            endpoint={config_endpoint}
            fullpath="output/enabled"
            label="Enable Output"
          />
        </div>
        <div className="col">
          <div className="row row-cols-2">
            <div className="col">
              <EndpointCheckbox
                disabled={disabled}
                endpoint={config_endpoint}
                fullpath="output/interlock"
                label="Enable Interlock"
              />
            </div>
            <div className="col">
              <EndpointCheckbox
                disabled={disabled}
                endpoint={config_endpoint}
                fullpath="output/interlock_tripped"
                className="disabled"
                label="Interlock Tripped"
              />
            </div>
          </div>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx(disabled && "text-secondary")}>
              Disabled Output Source Mode
            </InputGroup.Text>
            <EndpointDropdown
              disabled={disabled}
              endpoint={config_endpoint}
              fullpath="output/smode"
            >
              {SOURCE_MODES.map((func) => (
                <DropdownItem key={func} eventKey={func}>{func}</DropdownItem>
              ))}
            </EndpointDropdown>
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx(disabled && "text-secondary")}>
              Terminals
            </InputGroup.Text>
            <EndpointDropdown
              disabled={disabled}
              endpoint={config_endpoint}
              fullpath="output/terminals"
            >
              {TERMINALS.map((func) => (
                <DropdownItem key={func} eventKey={func}>{func}</DropdownItem>
              ))}
            </EndpointDropdown>
          </InputGroup>
        </div>
      </div>
    </TitleCard >
  );
}

import type { ConfigEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointButton, EndpointCheckbox, EndpointInput } from "@dssg/odin-react";
import { clsx } from "clsx";
import { InputGroup } from "react-bootstrap";

export const SaveFileSettingsGroup = ({ disabled, config_endpoint }: ConfigEndpointProp) => {
  return (
    <SettingsGroup disabled={disabled} title="Save File Settings">
      <div className="row row-cols-1 gy-2">
        <div className="col">
          <EndpointCheckbox
            disabled={disabled}
            label="Enable"
            endpoint={config_endpoint}
            fullpath="savefile/enable"
          />
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx((disabled || !config_endpoint.data.savefile.enable) && "text-secondary")}>
              File
            </InputGroup.Text>
            <EndpointInput
              disabled={disabled || !config_endpoint.data.savefile.enable}
              title="File"
              endpoint={config_endpoint}
              fullpath="savefile/file"
            />
            <EndpointButton
              disabled={disabled || !config_endpoint.data.savefile.enable}
              endpoint={config_endpoint}
              fullpath="savefile/set_file_from_timestamp"
            >
              Set From Current Time
            </EndpointButton>
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx((disabled || !config_endpoint.data.savefile.enable) && "text-secondary")}>
              Subfolder
            </InputGroup.Text>
            <EndpointInput
              disabled={disabled || !config_endpoint.data.savefile.enable}
              title="Folder"
              endpoint={config_endpoint}
              fullpath="savefile/subfolder"
            />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx((disabled || !config_endpoint.data.savefile.enable) && "text-secondary")}>
              Output Path
            </InputGroup.Text>
            <EndpointInput
              disabled
              title="Folder"
              endpoint={config_endpoint}
              fullpath="savefile/full_path"
            />
          </InputGroup>
        </div>
      </div>
    </SettingsGroup >
  );
};

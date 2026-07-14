import type { ConfigEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointInput } from "@dssg/odin-react";
import { clsx } from "clsx";
import { InputGroup } from "react-bootstrap";

export const SaveFileSettingsGroup = ({ disabled, config_endpoint }: ConfigEndpointProp) => {
  return (
    <SettingsGroup disabled={disabled} title="Save File Settings">
      <div className="row row-cols-1 gy-2">
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx(disabled && "text-secondary")}>
              File
            </InputGroup.Text>
            <EndpointInput
              disabled={disabled}
              title="File"
              endpoint={config_endpoint}
              fullpath="savefile/file"
            />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx(disabled && "text-secondary")}>
              Subfolder
            </InputGroup.Text>
            <EndpointInput
              disabled={disabled}
              title="Folder"
              endpoint={config_endpoint}
              fullpath="savefile/subfolder"
            />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text className={clsx(disabled && "text-secondary")}>
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

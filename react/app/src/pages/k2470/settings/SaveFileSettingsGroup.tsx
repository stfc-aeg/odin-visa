import type { ConfigEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointInput } from "@dssg/odin-react";
import { InputGroup } from "react-bootstrap";

export const SaveFileSettingsGroup = ({ config_endpoint }: ConfigEndpointProp) => {
  return (
    <SettingsGroup title="Save File Settings">
      <div className="row row-cols-1 gy-2">
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              File
            </InputGroup.Text>
            <EndpointInput title="File" endpoint={config_endpoint} fullpath="savefile/file" />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Subfolder
            </InputGroup.Text>
            <EndpointInput title="Folder" endpoint={config_endpoint} fullpath="savefile/subfolder" />
          </InputGroup>
        </div>
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Output Path
            </InputGroup.Text>
            <EndpointInput disabled title="Folder" endpoint={config_endpoint} fullpath="savefile/full_path" />
          </InputGroup>
        </div>
      </div>
    </SettingsGroup >
  );
};

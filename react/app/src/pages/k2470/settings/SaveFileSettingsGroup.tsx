import type { ControlEndpointProp } from "@/lib/types";
import { SettingsGroup } from "@/pages/k2470/settings/SettingsGroup";
import { EndpointInput } from "@dssg/odin-react";
import { InputGroup } from "react-bootstrap";

export const SaveFileSettingsGroup = ({ control_endpoint }: ControlEndpointProp) => {
  return (
    <SettingsGroup title="Save File Settings">
      <div className="row gy-2">
        <div className="col-sm" style={{ minWidth: "250px" }}>
          <InputGroup>
            <InputGroup.Text>
              File
            </InputGroup.Text>
            <EndpointInput title="File" endpoint={control_endpoint} fullpath="config/savefile/file" />
          </InputGroup>
        </div>
        <div className="col-sm" style={{ minWidth: "250px" }}>
          <InputGroup>
            <InputGroup.Text>
              Subfolder
            </InputGroup.Text>
            <EndpointInput title="Folder" endpoint={control_endpoint} fullpath="config/savefile/subfolder" />
          </InputGroup>
        </div>
      </div>
      <div className="row mt-2">
        <div className="col">
          <InputGroup>
            <InputGroup.Text>
              Output Path
            </InputGroup.Text>
            <EndpointInput disabled title="Folder" endpoint={control_endpoint} fullpath="config/savefile/path" />
          </InputGroup>
        </div>
      </div>
    </SettingsGroup >
  );
};

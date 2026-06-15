import { ModeSelect } from "@/pages/triggers/settings/components/ModeSelect";
import type { K2470ComponentProps } from "@/lib/types";
import { SettingsGroup } from "@/pages/triggers/settings/SettingsGroup";
import { EndpointButton } from "@dssg/odin-react";
import { InputGroup, Form, OverlayTrigger, Tooltip, Button } from "react-bootstrap";

export const GeneralSettingsGroup = ({ endpoint, device }: K2470ComponentProps) => {
  return (
    <SettingsGroup>
      <InputGroup size="sm" className="flex-fill">
        <InputGroup.Text>Trigger Status</InputGroup.Text>
        <Form.Control className="font-monospace" disabled value={device.trigger.status} />
      </InputGroup>
      <ModeSelect endpoint={endpoint} device={device} />
      <div className="d-flex gap-2">
        <EndpointButton
          className="flex-fill"
          endpoint={endpoint}
          fullpath="devices/K2470/trigger/initiate"
          variant="danger"
          size="sm"
          value={{}}
        >
          Trigger
        </EndpointButton>
        <EndpointButton
          className="flex-fill"
          endpoint={endpoint}
          fullpath="devices/K2470/trigger/clear_buffer"
          variant="secondary"
          size="sm"
          value={{}}
        >
          Clear Buffer
        </EndpointButton>
      </div>
    </SettingsGroup>
  );
};

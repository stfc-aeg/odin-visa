import { SettingsGroup } from "@/pages/triggers/settings/SettingsGroup";
import { SetButtonInput } from "@/pages/triggers/settings/components/SetButtonInput";
import type { K2470ComponentProps } from "@/lib/types";
import { Col, Form, Row } from "react-bootstrap";
import { EndpointCheckbox } from "@dssg/odin-react";

export const BufferSettingsGroup = ({ endpoint, device }: K2470ComponentProps) => {
  return (
    <SettingsGroup title="Buffer Settings">
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Name"
        inputType="text"
        value={device.trigger.buffer_name}
        setFullpath="devices/K2470/trigger/buffer_name"
      />
      <SetButtonInput
        endpoint={endpoint}
        device={device}
        title="Max Size"
        value={device.trigger.max_buffer_size}
        setFullpath="devices/K2470/trigger/max_buffer_size"
      />
      <Form>
        <Row>
          <Col className="d-flex align-items-center">
            <p>Full Buffer Write Behavior</p>
          </Col>
          <Col>
            <EndpointCheckbox
              endpoint={endpoint}
              fullpath="devices/K2470/trigger/buffer_fill_mode"
              label="Stop"
              type="radio"
              value="CONT"
            />
            <EndpointCheckbox
              endpoint={endpoint}
              fullpath="devices/K2470/trigger/buffer_fill_mode"
              label="Overwrite Oldest Data"
              type="radio"
              value="CONT"
            />
          </Col>
        </Row>
      </Form>
    </SettingsGroup >
  );
};

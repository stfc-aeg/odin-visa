import type { K2470ComponentProps } from "@/lib/types";
import { OverlayTrigger, Dropdown, InputGroup, Tooltip } from "react-bootstrap";

const MODES = [
  { label: "Empty", fullpath: "devices/K2470/trigger/reset_model" },
  { label: "SimpleLoop", fullpath: "devices/K2470/trigger/simple_loop/load" },
  { label: "DurationLoop", fullpath: "devices/K2470/trigger/duration_loop/load" },
  { label: "LinearSweep", fullpath: "devices/K2470/trigger/linear_sweep/load" },
] as { label: "SimpleLoop" | "LinearSweep", fullpath: string }[];

export const ModeSelect = ({ endpoint, device }: K2470ComponentProps) => {
  const onSelectHandler = async (eventKey: string | null) => {
    if (!eventKey) return;
    await endpoint.put({}, eventKey);
  };

  const tooltip = (props) => (
    <Tooltip id="mode-tooltip" {...props}>
      Set the acquisition mode.
    </Tooltip>
  );

  return (
    <InputGroup size="sm" className="w-100">
      <OverlayTrigger overlay={tooltip}>
        <InputGroup.Text>Mode</InputGroup.Text>
      </OverlayTrigger>
      <Dropdown onSelect={onSelectHandler}>
        <Dropdown.Toggle variant="white" size="sm" className="border flex-fill d-flex justify-content-between align-items-center">
          {device.trigger.current_model}
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {MODES.map((m) => (
            <Dropdown.Item key={m.label} eventKey={m.fullpath}>{m.label}</Dropdown.Item>
          ))}
        </Dropdown.Menu>
      </Dropdown>
    </InputGroup>
  )
}

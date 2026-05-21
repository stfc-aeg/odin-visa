import { EndpointDropdown, type AdapterEndpoint } from "@dssg/odin-react";
import { Dropdown } from "react-bootstrap";

export interface BasicEndpointDropdownProps {
  endpoint: AdapterEndpoint;
  fullpath: string;
  value: string;
  variant?: string;
  items: string[];
}

export const BasicEndpointDropdown = (props: BasicEndpointDropdownProps) => {
  const { endpoint, fullpath, value, items, variant } = props;

  return (
    <EndpointDropdown
      endpoint={endpoint}
      fullpath={fullpath}
      title={value}
      event_type="select"
      variant={variant ?? "primary"}
    >
      {items.map((item) => (
        <Dropdown.Item key={item} eventKey={item}>
          {item}
        </Dropdown.Item>
      ))}
    </EndpointDropdown>
  )
}

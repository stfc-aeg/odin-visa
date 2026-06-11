import { DropdownButton, Dropdown, Form, InputGroup, Container, Row, Col } from "react-bootstrap";

export const SelectedBufferDropdown = () => {
  return (
    <Dropdown>
      <Dropdown.Toggle className="w-100">
        {selectedBufferName}
      </Dropdown.Toggle>
      <Dropdown.Menu>
        {Object.keys(buffers).map((name) =>
          <Dropdown.Item key={name} onClick={() => {
            setSelectedBufferName(name);
          }}>{name}</Dropdown.Item>
        )}
      </Dropdown.Menu>
    </Dropdown>
  );
}

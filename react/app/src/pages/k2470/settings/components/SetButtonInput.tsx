import { EndpointButton } from "@dssg/odin-react";
import { Form, InputGroup } from "react-bootstrap";
import { convertUnits, SIPrefixDropdown, type SIPrefix } from "./SIPrefixDropdown";
import { useEffect, useState } from "react";
import type { K2470ComponentProps } from "@/lib/types";
import { floatEquality } from "@/lib/util";

interface ToggleButtonConfig {
  fullpath: string;
  value: boolean;
  disableInput?: boolean;
  on?: string;
  off?: string;
}

interface SetButtonInputProps extends K2470ComponentProps {
  title: string;
  inputType?: "text" | "number";
  value: number | string;
  unitPrefix?: string;
  setFullpath: string;
  toggleButton?: ToggleButtonConfig;
}

// TODO: Rounding floating point errors?
export const SetButtonInput = ({
  endpoint,
  title,
  inputType = "number",
  value,
  unitPrefix = undefined,
  setFullpath,
  toggleButton,
}: SetButtonInputProps) => {
  const unit = unitPrefix === "VOLT" ? "V" : "A";
  const [prefix, setPrefix] = useState<SIPrefix>("");

  const [uiValue, setUIValue] = useState(value);
  useEffect(() => {
    setUIValue(
      unitPrefix && typeof value === "number"
        ? convertUnits(value, "", prefix)
        : value
    );
  }, [value, prefix, unitPrefix])

  const [normalisedUIValue, setNormalisedUIValue] = useState(value);
  useEffect(() => {
    setNormalisedUIValue(
      unitPrefix && typeof uiValue === "number"
        ? convertUnits(uiValue, prefix, "")
        : uiValue
    )
  }, [uiValue, prefix, unitPrefix])

  return (
    <InputGroup size="sm" className="flex-nowrap w-100">
      <InputGroup.Text className="text-nowrap">{title}</InputGroup.Text>

      <Form.Control
        size="sm"
        type={inputType}
        value={uiValue}
        onChange={(event) =>
          setUIValue(inputType === "number" ? Number(event.target.value) : event.target.value)
        }
        className="flex-fill"
        disabled={toggleButton?.disableInput && toggleButton.value}
      />

      {unitPrefix && (
        <SIPrefixDropdown unit={unit} value={prefix} onChange={(prefix) => setPrefix(prefix)} />
      )}

      <EndpointButton
        endpoint={endpoint}
        fullpath={setFullpath}
        value={normalisedUIValue}
        variant="primary"
        size="sm"
        disabled={floatEquality(normalisedUIValue, value)}
      >
        Set
      </EndpointButton>

      {toggleButton && (
        <EndpointButton
          endpoint={endpoint}
          fullpath={toggleButton.fullpath}
          value={!toggleButton.value}
          variant={toggleButton.value ? "success" : "danger"}
          size="sm"
        >
          {toggleButton.value
            ? toggleButton.on ?? "ON"
            : toggleButton.off ?? "OFF"}
        </EndpointButton>
      )}
    </InputGroup>
  );
};

import { Dropdown, DropdownButton } from "react-bootstrap";

export type SIPrefix = "n" | "µ" | "m" | "" | "K";

export const SI_PREFIXES: Map<SIPrefix, number> = new Map([
  ["n", 1e-9],
  ["µ", 1e-6],
  ["m", 1e-3],
  ["", 1],
]);

export interface SIPrefixDropdownProps {
  unit: string;
  value: SIPrefix;
  onChange: (prefix: SIPrefix) => void;
}

// eslint-disable-next-line react-refresh/only-export-components
export const convertUnits = (value: number, from: SIPrefix, to: SIPrefix) => {
  return (value * (SI_PREFIXES.get(from) ?? 1)) / (SI_PREFIXES.get(to) ?? 1)
}

export const SIPrefixDropdown = (props: SIPrefixDropdownProps) => {
  const { unit, value, onChange } = props;

  return (
    <DropdownButton
      title={`${value}${unit}`}
      variant="secondary"
      as={Dropdown}
    >
      {Array.from(SI_PREFIXES.keys()).map((prefix) => (
        <Dropdown.Item key={prefix} onClick={() => onChange(prefix)}>
          {prefix}{unit}
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
};

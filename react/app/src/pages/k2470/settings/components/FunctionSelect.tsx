import { EndpointButton } from "@dssg/odin-react";
import { InputGroup } from "react-bootstrap";
import type { Keithley2470Props } from "@/lib/types";

type FunctionMode = "source" | "sense";

export interface FunctionSelectProps extends Keithley2470Props {
  mode: FunctionMode;
}

const AllowedFunctions = {
  "VOLT": { label: "Voltage" },
  "CURR": { label: "Current" },
};

export const FunctionSelect = ({ bundle, mode }: FunctionSelectProps) => {
  const currentFunction = bundle.device[mode].function;

  return (
  );
};

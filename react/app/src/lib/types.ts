import type { Buffers, Control } from "@/lib/ParamTreeType";
import type { AdapterEndpoint, ParamTree } from "@dssg/odin-react";

type WithRequired<T, K extends keyof T> = T & Required<Pick<T, K>>;

export const hasData = <T extends Record<string, ParamTree>>(endpoint: AdapterEndpoint<T>): endpoint is WithRequired<AdapterEndpoint<T>, "data"> => {
  return endpoint.data !== undefined;
}

export interface Keithley2470Props {
  control_endpoint: WithRequired<AdapterEndpoint<Control>, "data">
  buffers_endpoint?: WithRequired<AdapterEndpoint<Buffers>, "data">
}

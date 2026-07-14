import type { Buffer, Config } from "@/lib/ParamTreeType";
import type { AdapterEndpoint, ParamTree } from "@dssg/odin-react";

type WithRequired<T, K extends keyof T> = T & Required<Pick<T, K>>;

export const hasData = <T extends Record<string, ParamTree>>(endpoint: AdapterEndpoint<T>): endpoint is WithRequired<AdapterEndpoint<T>, "data"> => {
  return endpoint.data !== undefined;
}

export interface ConfigEndpointProp {
  disabled?: boolean;
  config_endpoint: WithRequired<AdapterEndpoint<Config>, "data">;
}

export interface BuffersEndpointProp {
  buffers_endpoint: WithRequired<AdapterEndpoint<Buffer>, "data">;
}

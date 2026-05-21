import type { Device, K2470 } from "@/lib/ParamTreeType";
import type { AdapterEndpoint } from "@dssg/odin-react";

export interface DeviceBundle<T extends Device> {
  endpoint: AdapterEndpoint,
  device: T,
  path: string,
}

export interface Keithley2470Props {
  bundle: DeviceBundle<K2470>
}

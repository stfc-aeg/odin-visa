import type { ParamNode } from "@dssg/odin-react";

export interface OdinVisaParamTree extends ParamNode {
  poll_interval: number;
  num_devices: number;
  devices: Record<string, Device>;
}

export interface K2470 extends ParamNode {
  device: DeviceDetails,
  buffers: Buffers,
  config: Config,
}

export interface DeviceDetails extends ParamNode {
  type: "K2470";
  ident: string;
  address: string;
}

export interface DeviceTypeMap {
  K2470: K2470
}

export type DeviceType = keyof DeviceTypeMap;
export type Device = DeviceTypeMap[DeviceType];

export interface EventLog extends ParamNode {
  count: number;
  last_event: Event;
  log: Event[];
}

export interface Event extends ParamNode {
  code: number;
  message: string;
  type: number;
  timestamp_ms: number;
  context: string;
}

export interface Config extends ParamNode {
  savefile: SaveFileConfig;
  source: SourceConfig;
  poll_freq: number;
}

export interface SaveFileConfig extends ParamNode {
  file: string,
  subfolder: string,
  full_path: string,
}

export interface SenseConfig extends ParamNode {
  auto_range: boolean;
  averaging: AveragingConfig;
  count: number;
  function: string;
  nplcs: number;
  range: number;
}

export interface AveragingConfig extends ParamNode {
  count: number;
  enable: false;
  type: string;
}

export interface SourceConfig extends ParamNode {
  function: string;
  level: number;
  limit: number;
}

export interface Acquisitions extends ParamNode {
  type: string;
  status: Status;
  output: boolean;
  start: null;
  stop: null;
  paused: boolean;
}

export type StatusType = "IDLE" | "RUNNING" | "WAITING" | "PAUSED" | "EMPTY" | "BUILDING" | "FAILED" | "ABORTING" | "ABORTED";

export interface Status extends ParamNode {
  block: number;
  state: StatusType;
  second_state: StatusType;
}

export interface Buffers extends ParamNode {
  buffers: Record<string, BufferItem[]>,
  read_from: number,
}

export type BufferItem = [timestamp: number, source: number, sense: number];

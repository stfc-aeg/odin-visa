import type { ParamNode } from "@dssg/odin-react";

export interface OdinVisaParamTree extends ParamNode {
  poll_interval: number;
  num_devices: number;
  devices: Record<string, Device>;
}

export interface K2470 extends ParamNode {
  control: Control,
  buffers: Buffers,
}

export interface Control extends ParamNode {
  type: "K2470";
  ident: string;
  address: string;

  event_log: EventLog;
  config: Config;
  acquisitions: Acquisitions;
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
  buffer: BufferConfig;
  mode: ModeConfig;
  savefile: SaveFileConfig;
  sense: SenseConfig;
  source: SourceConfig;
}

export interface BufferConfig extends ParamNode {
  clear: null;
  name: string;
  size: number;
}

export interface ModeConfig extends ParamNode {
  loop_until_trigger: LoopUntilTriggerConfig;
}

export interface LoopUntilTriggerConfig extends ParamNode {
  delay: number;
  post_trigger_reading_percentage: number;
}

export interface SaveFileConfig extends ParamNode {
  dataset_name: string;
  filename: string;
  filepath: string;
  write_period: number;
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
  start_from: StartFrom,
}

export type BufferItem = [timestamp: number, source: number, sense: number];

export interface StartFrom extends ParamNode {
  timestamp: number;
}

import type { ParamNode } from "@dssg/odin-react";

export interface OdinVisaParamTree extends ParamNode {
  poll_interval: number;
  num_devices: number;
  devices: Record<string, Device>;
}

export interface K2470 extends ParamNode {
  device: DeviceDetails,
  buffer: Buffer,
  config: Config,
  event_log: EventLog
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
  events: Event[];
}

export interface Event extends ParamNode {
  code: number;
  message: string;
  type: number;
  datetime: number;
}

export interface Config extends ParamNode {
  savefile: SaveFileConfig;
  source: SourceConfig;
  sense: SenseConfig;
  acquisition: Acquisition;
  poll_freq: number;
}

export interface SaveFileConfig extends ParamNode {
  enable: boolean,
  file: string,
  subfolder: string,
  full_path: string,
  exists: boolean,
}

export const AVERAGING_MODES = [
  "REPEAT",
  "MOVING"
] as const;

export type AveragingFilter = (typeof AVERAGING_MODES)[number];

export const SENSE_FUNCTIONS = [
  "VOLTAGE",
  "CURRENT",
] as const;

export type SenseFunction = (typeof SENSE_FUNCTIONS)[number];

export interface SenseConfig extends ParamNode {
  averaging_count: number;
  averaging: boolean;
  averaging_filter: AveragingFilter;
  auto_zero: boolean;
  nplcs: number;
  offset_compensation: boolean;
  auto_range: boolean;
  auto_range_lower_limit: number;
  auto_range_rebound: boolean;
  auto_range_upper_limit: number;
  range: number;
  relative_offset_level: number
  relative_offset: boolean;
  remote_sensing: boolean;
  count: number;
  function: SenseFunction;
}

export const PROTECTION_MODES = [
  "PROT20",
  "PROT40",
  "PROT100",
  "PROT200",
  "PROT300",
  "PROT400",
  "PROT500",
  "NONE",
] as const;

export type ProtectionMode = (typeof PROTECTION_MODES)[number];

export const SOURCE_FUNCTIONS = [
  "VOLTAGE",
  "CURRENT",
] as const;

export type SourceFunction = (typeof SOURCE_FUNCTIONS)[number];

export interface SourceConfig extends ParamNode {
  function: string;
  level: number;
  limit: number;
  delay: number;
  auto_delay: boolean;
  high_capacitance: number;
  protection: ProtectionMode;
  range: number;
  auto_range: boolean;
  read_back: boolean;
}

export const SOURCE_MODES = [
  "NORMAL",
  "HIMPEDANCE",
  "ZERO",
  "GUARD"
] as const;

export type SMode = (typeof SOURCE_MODES)[number];

export const TERMINALS = [
  "FRONT",
  "REAR"
] as const;

export type Terminal = (typeof TERMINALS)[number];

export interface OutputConfig extends ParamNode {
  smode: SMode;
  interlock: boolean;
  interlock_tripped: boolean;
  enabled: boolean
  terminals: Terminal;
}

export interface Acquisition extends ParamNode {
  acquiring: boolean;
}

export type StatusType = "IDLE" | "RUNNING" | "WAITING" | "PAUSED" | "EMPTY" | "BUILDING" | "FAILED" | "ABORTING" | "ABORTED";

export interface Status extends ParamNode {
  block: number;
  state: StatusType;
  second_state: StatusType;
}

export const DOWNSAMPLE_METHODS = [
  "Full",
  "Mean",
  "Median",
  "Min",
  "Max",
  "First",
] as const;

export type DownsampleMethod = (typeof DOWNSAMPLE_METHODS)[number];

export interface Buffer extends ParamNode {
  buffer: BufferItem[],
  range: number,
  downsample: DownsampleMethod,
  bin_size: string,
}

export type BufferItem = [timestamp: number, source: number, sense: number];

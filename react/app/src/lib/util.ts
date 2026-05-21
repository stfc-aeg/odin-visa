import { type ComponentProps, type FC } from "react";
import type { DeviceBundle } from "./types";

export function floatEquality(a: any, b: any): boolean {
  if (typeof a !== "number" || typeof b !== "number") return a === b;
  return Math.abs(a - b) < Number.EPSILON;
}


export function floatEquality(a: any, b: any): boolean {
  if (typeof a !== "number" || typeof b !== "number") return a === b;
  return Math.abs(a - b) < Number.EPSILON;
}


import type { Keithley2470Props } from "@/lib/types";
import { OdinGraph } from "@dssg/odin-react";

export const BufferGraph = ({ bundle }: Keithley2470Props) => {
  const plotlyData = Object.entries(bundle.device.acquisition.buffers).map(([name, buffer]) => {
    const offsets: number[] = [];
    const sources: number[] = [];
    const senses: number[] = [];
    const resistances: number[] = [];

    for (const [offset, source, sense] of buffer.buffer) {
      offsets.push(offset);
      sources.push(source);
      senses.push(sense);
      resistances.push(source / sense);
    }

    return { x: offsets, y: resistances, name: name };
  });

  return (
    <OdinGraph data={plotlyData} />
  )
}

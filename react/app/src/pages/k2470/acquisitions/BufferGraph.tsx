import type { Keithley2470Props } from "@/lib/types";
import { OdinGraph } from "@dssg/odin-react";

const WINDOW_US = 10_000_000;

function makeLayout(latestTs) {
  return {
    xaxis: {
      type: "linear",
      range: [
        latestTs - WINDOW_US,
        latestTs,
      ],
    },
  };
}

export const BufferGraph = ({ bundle }: Keithley2470Props) => {
  const timestamps: number[] = [];
  const sources: number[] = [];
  const senses: number[] = [];
  const resistances: number[] = [];
  const plotlyData = Object.entries(bundle.device.acquisition.buffers).map(([name, buffer]) => {
    for (const [timestamp, source, sense] of buffer.buffer) {
      timestamps.push(timestamp);
      sources.push(source);
      senses.push(sense);
      resistances.push(source / sense);
    }

    return { x: timestamps, y: senses, name: name, };
  });

  return (
    <OdinGraph data={plotlyData} layout={makeLayout(timestamps[timestamps.length - 1])} />
  )
}

import { OdinGraph } from "@dssg/odin-react";
import { Button } from "react-bootstrap";

interface BufferItem {
  reading: number;
  source: number;
}

export interface BufferGraphProps {
  title: string;
  data: BufferItem[];
  currentModel: string;
}

export const BufferGraph = ({ title, data, currentModel }: BufferGraphProps) => {
  if (data.length === 0) {
    return <h1>Empty buffer</h1>;
  }

  const plotData = currentModel === "LinearSweep"
    ? [
      {
        x: data.map((item) => item.source),
        y: data.map((item) => item.reading),
        type: "scatter" as const,
        mode: "lines",
      },
    ]
    : data.map((item) => item.reading);

  const layout = {
    xaxis: { title: currentModel === "LinearSweep" ? { text: "Source" } : undefined, autorange: true },
    yaxis: { autorange: true, automargin: true },
    title: title ? { text: title } : undefined,
    autosize: true,
    uirevision: "true" as const,
  };

  return (
    <div>
      <Button onClick={() => console.error('test')}>Refresh</Button>
      <OdinGraph data={plotData} layout={layout} />
    </div >
  );
};

import { DOWNSAMPLE_METHODS, type BufferItem, type Buffer } from "@/lib/ParamTreeType";
import type { WithRequired } from "@/lib/types";
import { type AdapterEndpoint, OdinGraph, EndpointInput, EndpointDropdown } from "@dssg/odin-react";
import type { Layout } from "plotly.js";
import { DropdownItem, InputGroup } from "react-bootstrap";

const col = (arr: BufferItem[], index: number) => arr.map((row) => row[index]);

export const BufferGraph = ({ buffer_endpoint }: { buffer_endpoint: WithRequired<AdapterEndpoint<Buffer>, "data"> }) => {
  const data = buffer_endpoint.data.buffer;
  const graph_data = [{
    x: col(data, 0),
    y: col(data, 1)
  }];

  const layout: Partial<Layout> = {
    xaxis: {
      ticks: '',
      showticklabels: false
    },
  }

  return (
    <div className="row row-cols-1 gy-2">
      <div className="col">
        <OdinGraph data={graph_data} layout={layout} />
      </div>
      <div className="col">
        <InputGroup>
          <InputGroup.Text>
            History (seconds)
          </InputGroup.Text>
          <EndpointInput
            endpoint={buffer_endpoint}
            fullpath="range"
          />
        </InputGroup>
      </div>
      <div className="col">
        <InputGroup>
          <InputGroup.Text>
            Downsample Method
          </InputGroup.Text>
          <EndpointDropdown endpoint={buffer_endpoint} fullpath="downsample">
            {DOWNSAMPLE_METHODS.map((func) => (
              <DropdownItem key={func} eventKey={func}>{func}</DropdownItem>
            ))}
          </EndpointDropdown>
        </InputGroup>
      </div>
      <div className="col">
        <InputGroup>
          <InputGroup.Text>
            Bin Size
          </InputGroup.Text>
          <EndpointInput
            endpoint={buffer_endpoint}
            fullpath="bin_size"
          />
        </InputGroup>
      </div>
    </div>
  )
}

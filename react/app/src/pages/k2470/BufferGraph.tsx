import { type AdapterEndpoint, OdinGraph, EndpointInput } from "@dssg/odin-react";
import { InputGroup } from "react-bootstrap";

const col = (arr, index) => arr.map((row) => row[index]);

export const BufferGraph = ( { config_endpoint, buffer_endpoint } : { config_endpoint: AdapterEndpoint, buffer_endpoint: AdapterEndpoint }) => {
  const data = buffer_endpoint?.data.buffer;
  const graph_data = [{
    x: col(data, 0),
    y: col(data, 1)
  }];

  const layout = {
    xaxis: {
      ticks: '',
      showticklabels: false
    },
  }

  return (
    <div className="row row-cols-1">
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
    </div>
  )
}

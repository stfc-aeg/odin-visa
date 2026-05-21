import { EndpointButton, type AdapterEndpoint } from "@dssg/odin-react";
import { Form, InputGroup } from "react-bootstrap";
import { useState } from "react";

export interface AveragingGroupProps {
  averagingEnable: boolean;
  avgCount: number;
  avgType: string;
  endpoint: AdapterEndpoint;
  originalAvgCount: number;
}

export const AveragingGroup = ({
  averagingEnable,
  avgCount,
  avgType,
  endpoint,
  originalAvgCount,
}: AveragingGroupProps) => {
  const [count, setCount] = useState(avgCount);

  return (
    <div className="d-flex flex-column gap-2">
      <InputGroup size="sm" className="flex-nowrap w-100">
        <InputGroup.Text className="text-nowrap">Avg Count</InputGroup.Text>
        <EndpointButton
          endpoint={endpoint}
          fullpath="devices/K2470/sense/averaging_enable"
          value={!averagingEnable}
          variant={averagingEnable ? "success" : "danger"}
          size="sm"
        >
          {averagingEnable ? "ON" : "OFF"}
        </EndpointButton>
        <Form.Control
          size="sm"
          type="number"
          value={count}
          disabled={!averagingEnable}
          className="flex-fill"
          onChange={(e) => setCount(Number(e.target.value))}
        />
        <EndpointButton
          endpoint={endpoint}
          fullpath="devices/K2470/sense/averaging_count"
          value={count}
          variant="primary"
          size="sm"
          disabled={!averagingEnable || count === originalAvgCount}
        >
          Set
        </EndpointButton>
      </InputGroup>
      <InputGroup size="sm" className="flex-nowrap w-100">
        <InputGroup.Text className="text-nowrap">Avg Type</InputGroup.Text>
        {["REP", "MOV"].map((t) => (
          <EndpointButton
            key={t}
            endpoint={endpoint}
            fullpath="devices/K2470/sense/averaging_type"
            value={t}
            variant={avgType === t ? "primary" : "outline-primary"}
            size="sm"
            disabled={!averagingEnable}
            className="flex-fill"
          >
            {t}
          </EndpointButton>
        ))}
      </InputGroup>
    </div>
  );
};

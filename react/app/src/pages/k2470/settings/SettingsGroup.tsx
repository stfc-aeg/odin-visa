import type { PropsWithChildren } from "react";
import { Card } from "react-bootstrap";

export interface SettingsGroupProps extends PropsWithChildren {
  title?: string;
};

export const SettingsGroup = ({ title, children }: SettingsGroupProps) => {
  return (
    <Card className="p-0">
      <Card.Header
        className="px-3 py-2 border-bottom fw-semibold"
        style={{ backgroundColor: '#f5f5f5' }}
      >
        {title}
      </Card.Header>
      <div className="container-fluid py-2">
        {children}
      </div>
    </Card>
  );
};

import { clsx } from "clsx";
import type { PropsWithChildren } from "react";
import { Card } from "react-bootstrap";

export interface TitleCardProps extends PropsWithChildren {
  disabled?: boolean;
  title?: string;
};

export const TitleCard = ({ disabled, title, children }: TitleCardProps) => {
  return (
    <Card className="p-0">
      <Card.Header
        className={"px-3 py-2 border-bottom fw-semibold bg-body-secondary"}
      >
        {title}
      </Card.Header>
      <div className={clsx(disabled && "bg-light", "container-fluid py-2")}>
        {children}
      </div>
    </Card>
  );
};

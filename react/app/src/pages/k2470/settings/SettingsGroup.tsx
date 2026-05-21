import type { PropsWithChildren } from "react";

export interface SettingsGroupProps extends PropsWithChildren {
  title?: string;
};

export const SettingsGroup = ({ title, children }: SettingsGroupProps) => {
  return (
    <div className="d-flex flex-column gap-2">
      {title &&
        <h3 className="text-muted text-uppercase fs-6 fw-bold mb-2">{title}</h3>
      }
      {children}
    </div>
  );
};

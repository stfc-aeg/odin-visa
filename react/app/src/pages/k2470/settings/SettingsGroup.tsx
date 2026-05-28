import type { PropsWithChildren } from "react";

export interface SettingsGroupProps extends PropsWithChildren {
  title?: string;
};

export const SettingsGroup = ({ title, children }: SettingsGroupProps) => {
  return (
    <div className="container-fluid p-2">
      <div className="row">
        {title &&
          <h3 className="text-muted text-uppercase fs-6 fw-bold mb-2">{title}</h3>
        }
      </div>
      {children}
    </div>
  );
};

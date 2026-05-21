import { WithEndpoint } from "@dssg/odin-react";
import type { ReactNode } from "react";

export const EndpointSelect = WithEndpoint(
  (props: React.HTMLAttributes<HTMLSelectElement>) => (
    <select {...props}>{props.children as ReactNode}</select>
  )
);

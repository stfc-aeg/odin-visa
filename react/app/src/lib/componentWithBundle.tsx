import type { ComponentType, PropsWithChildren } from "react"
import type { DeviceBundle } from "./types"
import type { Device } from "./ParamTreeType"
import { EndpointButton as EndpointButtonInner, EndpointInput as EndpointInputInner, EndpointRangeInput as EndpointRangeInputInner, EndpointCheckbox as EndpointCheckboxInner, EndpointDropdown as EndpointDropdownInner } from "@dssg/odin-react"

export interface ComponentWithBundleProps {
  bundle: DeviceBundle<Device>,
  path: string,
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any, react-refresh/only-export-components
export const withBundle = (EndpointComponent: ComponentType<any>) => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const componentWithBundle = ({ bundle, path, ...props }: ComponentWithBundleProps & PropsWithChildren<any>) => {
    return <EndpointComponent endpoint={bundle.endpoint} fullpath={`${bundle.path}/${path}`} {...props} />;
  }

  return componentWithBundle;
}

export const EndpointButton = withBundle(EndpointButtonInner);
export const EndpointInput = withBundle(EndpointInputInner);
export const EndpointRangeInput = withBundle(EndpointRangeInputInner);
export const EndpointDropdown = withBundle(EndpointDropdownInner);
export const EndpointCheckbox = withBundle(EndpointCheckboxInner);

import 'bootstrap/dist/css/bootstrap.min.css';

import { OdinApp, useAdapterEndpoint } from '@dssg/odin-react';
import type { OdinVisaParamTree } from './lib/ParamTreeType';
import { Keithley2470 } from './pages/k2470/Keithley2470';

export const App = () => {
  const endpoint = useAdapterEndpoint<OdinVisaParamTree>("visa", import.meta.env.VITE_ENDPOINT_URL, 1000);
  const devices = endpoint.data?.devices;

  if (!devices) {
    return <h1>Loading devices</h1>;
  }

  return (
    <OdinApp title='Odin Visa' navLinks={Object.keys(devices)}>
      {Object.entries(devices).map(([name, device]) => {
        const bundle = {
          endpoint: endpoint,
          device: device,
          path: `devices/${name}`,
        };
        switch (device.type) {
          case "K2470":
            return <Keithley2470 bundle={bundle} />
          default:
            console.error(`Unsupported device type '${device}'`);
            return <h1>Unsupported Device Type</h1>
        }
      })}
    </OdinApp >
  );
};

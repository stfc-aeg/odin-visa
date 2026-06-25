import 'bootstrap/dist/css/bootstrap.min.css';

import { OdinApp, useAdapterEndpoint } from '@dssg/odin-react';
import type { OdinVisaParamTree } from './lib/ParamTreeType';
import { Keithley2470 } from './pages/k2470/Keithley2470';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export const App = () => {
  const endpoint = useAdapterEndpoint<OdinVisaParamTree>("visa", import.meta.env.VITE_ENDPOINT_URL);

  if (!endpoint.data?.devices) {
    return <h1>Loading devices</h1>;
  }

  const devices = endpoint.data.devices

  return (
    <QueryClientProvider client={queryClient}>
      <OdinApp title='Odin Visa' navLinks={Object.keys(devices)}>
        {Object.entries(devices).map(([name, device]) => {
          switch (device.device.type) {
            case "K2470":
              return <Keithley2470 name={name} />
            default:
              console.error(`Unsupported device type '${device}'`);
              return <h1>Unsupported Device Type</h1>
          }
        })}
      </OdinApp >
    </QueryClientProvider>
  );
};

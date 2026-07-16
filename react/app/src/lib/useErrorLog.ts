import type { EventLog } from "@/lib/ParamTreeType";
import { useAdapterEndpoint, useError } from "@dssg/odin-react";
import { useEffect, useRef } from "react";

export const useErrorLog = (name: string): void => {
  const endpoint = useAdapterEndpoint<EventLog>(`visa/devices/${name}/event_log`, import.meta.env.VITE_ENDPOINT_URL, Number(import.meta.env.VITE_EVENT_LOG_POLL_TIME) || 1000);
  const { setError } = useError();
  const previousEvents = useRef<{ name: string; count: number } | null>(null);

  useEffect(() => {
    const events = endpoint.data?.events;

    if (!events) return;

    const previous = previousEvents.current;
    if (previous === null || previous.name !== name) {
      previousEvents.current = { name, count: events.length };
      return;
    }

    const firstNewEvent = Math.min(previous.count, events.length);
    const newEvents = events.slice(firstNewEvent);

    previousEvents.current = { name, count: events.length };

    newEvents.forEach((event) => {
      if (event.code != 1) return;
      const code = event.code.toString().padStart(4, "0");
      setError(
        new Error(
          `ERR${code}: ${event.message} (generated at ${event.datetime})`,
        ),
      );
    });
  }, [endpoint.data?.events, name, setError]);
};

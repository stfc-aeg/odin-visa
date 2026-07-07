import { type AdapterEndpoint } from "@dssg/odin-react";
import { useBufferStore } from "./buffersStore";
import { sleep } from "./util";

export class BufferPoll {
  private running = false;
  private endpoint: Pick<AdapterEndpoint, "get" | "put">;

  constructor(endpoint: Pick<AdapterEndpoint, "get" | "put">) {
    this.endpoint = endpoint;
  }

  public async start() {
    await sleep(0); // invalidate initial call in react StrictMode
    return;
    if (this.running) return;
    this.running = true;


    const { fetchBuffers } = useBufferStore.getState();

    while (this.running) {
      const start = performance.now();
      try {
        await fetchBuffers(this.endpoint);
      } catch (err) {
        console.error(err);
      }
      const end = performance.now();

      const refreshTime = Math.max(0, useBufferStore.getState().refreshTime - (end - start));
      await sleep(refreshTime);
    }
  }

  public async stop() {
    this.running = false;
  }
}

import { create } from "zustand";
import type { BufferItem } from "./ParamTreeType"
import type { AdapterEndpoint } from "@dssg/odin-react";
import Denque from "denque";

interface BufferLevel {
  buffer: Denque<BufferItem>;
  index: Denque<number>;
}

interface BufferStore {
  buffers: Record<string, BufferLevel>;
  cursor: number;
  appendBuffers: (incoming: Record<string, BufferItem[]>) => void;
  fetchBuffers: (endpoint: Pick<AdapterEndpoint, "get" | "put">) => Promise<void>;
}

export const useBufferStore = create<BufferStore>((set, get) => ({
  buffers: {},
  cursor: 0,
  appendBuffers: (incoming) => {
    set((state) => {
      const buffers = { ...state.buffers };
      let sharedCursor = state.cursor;

      for (const [name, newData] of Object.entries(incoming)) {
        if (newData.length === 0) continue;

        const current = buffers[name];

        if (!current || current == undefined) {
          const newTimestamp = newData[newData.length - 1][0];

          buffers[name] = {
            buffer: new Denque(newData),
            index: new Denque([newData.length]),
          };

          sharedCursor = Math.max(sharedCursor, newTimestamp);
        } else {
          for (let i = 0; i < newData.length; i++) {
            current.buffer.push(newData[i]);
          }
          current.index.push(newData.length);
          const newTimestamp = newData[newData.length - 1][0];
          sharedCursor = Math.max(sharedCursor, newTimestamp);

          // TODO: Customisable retention
          if (current.index.length > 5) {
            const toRemove = current.index.shift()!;
            current.buffer.remove(0, toRemove);
          }
        }

      }

      return {
        buffers,
        cursor: sharedCursor,
      }
    })
  },
  fetchBuffers: async (endpoint) => {
    const { cursor, appendBuffers } = get();
    await endpoint.put({ timestamp: cursor + 1 }, "start_from");
    const buffers = await endpoint.get<Record<string, BufferItem[]>>("buffers");
    appendBuffers(buffers);
  },
}));

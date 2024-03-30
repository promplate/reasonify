import ask from "./ask";
import python from "./python";

export interface Tool {
  id: string;
  name: string;
  usage: string;
  schema: string;
  instruction?: string;
  run: (options: Record<string, unknown>) => unknown;
}

export default [python, ask] as Tool[];

export { ask, python };

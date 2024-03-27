export interface Input {
  source: string;
}

export interface Output {
  "stdout/stderr": string; // if you print something, it will be here
  "global values": Record<string, unknown>; // any values you create will be here
  "return"?: unknown; // the return value of the last line if it is an expression
}

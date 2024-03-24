export interface Input {
  source: string;
}

export interface Output {
  "stdout/stderr": string; // if you print something, it will be here
  "values": Record<string, unknown>; // any values you create will be here
}

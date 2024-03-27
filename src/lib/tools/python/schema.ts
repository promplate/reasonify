export interface Input {
  requirements?: string[]; // list of packages to pip install before running the code
  source: string;
}

// If you need to use some third-party libraries, you must fill the `requirements` field.

export interface Output {
  "stdout/stderr": string; // if you print something, it will be here
  "global values": Record<string, unknown>; // any values you create will be here
  "return"?: unknown; // the return value of the last line if it is an expression
}

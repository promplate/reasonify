export type Output =
  | {
    response: string;
  }
  | {
    tools: string[]; // the id of your tools
  };

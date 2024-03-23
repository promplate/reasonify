export interface Output {
  plan: string;
  tools: string[]; // tool ids, not tool names. This should not be empty!
}

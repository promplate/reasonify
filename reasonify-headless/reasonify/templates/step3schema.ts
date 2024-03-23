interface Action {
  purpose: string;
  tool_id: string;
  payload: object; // must be fit with the tool's `schema`!
}

export interface Output {
  note: string; // say something about the actions you are gonna invoke
  actions: Action[]; // only call the tools you can use
}

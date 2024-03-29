interface Action {
  purpose: string; // what this action is for (this field should use the user's language)
  tool_id: string;
  payload: object; // must be fit with the tool's `schema`!
}

export interface Output {
  note: string; // say something about the actions you are gonna invoke (this field should use the user's language)
  actions: Action[]; // only call the tools you can use
}

/*
The `note` must be different from the `purpose` of any action in the `actions` array!
`note` shows your complete plan, while `purpose` shows the purpose of each action.
*/

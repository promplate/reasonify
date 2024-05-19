import { writable } from "svelte/store";

const pyodideReady = writable(false);
const reasonifyReady = writable(false);

export { pyodideReady, reasonifyReady };

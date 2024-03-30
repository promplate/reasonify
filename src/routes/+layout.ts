import { inject } from "@vercel/analytics";
import { dev } from "$app/environment";

inject({ mode: dev ? "development" : "production" });

export const prerender = true;

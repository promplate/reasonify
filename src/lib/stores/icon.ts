import { writable } from "svelte/store";

export const emoji = writable<string | null>(null);

const moons = ["full-moon", "waning-gibbous-moon", "last-quarter-moon", "waning-crescent-moon", "new-moon", "waxing-crescent-moon", "first-quarter-moon", "waxing-gibbous-moon"];

let i = 0;

let animating = false;

function animateIcon() {
  if (!animating)
    return;

  emoji.set(moons[i]);
  i = (i + 1) % moons.length;

  setTimeout(animateIcon, 300);
}

export function startIconAnimation() {
  animating = true;
  animateIcon();
}

export function stopIconAnimation() {
  animating = false;
  emoji.set(null);
}

import { chromium } from "playwright";
import { mkdirSync, writeFileSync } from "fs";
import { execFileSync } from "child_process";
import path from "path";
import { pathToFileURL } from "url";

const base = process.env.APP_URL || "http://127.0.0.1:3010";
const root = path.join(process.cwd(), "..");
const frames = path.join(root, "evidence", "frames");
const slides = path.join(root, "evidence", "slides");
mkdirSync(frames, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  channel: process.env.PW_CHANNEL || "chrome",
});
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
const shot = (name) => page.screenshot({ path: path.join(frames, name), type: "png" });

for (const [i, file] of ["01-problem.html", "02-who.html", "03-why.html"].entries()) {
  await page.goto(pathToFileURL(path.join(slides, file)).href, { waitUntil: "networkidle" });
  await shot(`s${String(i + 1).padStart(2, "0")}.png`);
}

await page.goto(base, { waitUntil: "networkidle" });
await page.waitForTimeout(800);
await shot("p01-home.png");

const [res] = await Promise.all([
  page.waitForResponse((r) => r.url().includes("/shifts/demo") && r.request().method() === "POST"),
  page.getByRole("button", { name: /Run Harbor Auto overnight/i }).click(),
]);
const shift = await res.json();
await page.waitForURL(/\/shift\//, { timeout: 30000 });
await page.waitForTimeout(1200);
await shot("p02-board.png");
await page.mouse.wheel(0, 900);
await page.waitForTimeout(600);
await shot("p03-cases.png");
await page.mouse.wheel(0, 1100);
await page.waitForTimeout(600);
await shot("p04-log.png");

await page.goto(`${base}/how`, { waitUntil: "networkidle" });
await page.waitForTimeout(800);
await shot("p05-how.png");

await page.goto(pathToFileURL(path.join(slides, "04-close.html")).href, { waitUntil: "networkidle" });
await shot("s04-close.png");

await browser.close();

const list = path.join(frames, "concat.txt");
const clips = [
  ["s01.png", 5],
  ["s02.png", 4],
  ["s03.png", 4],
  ["p01-home.png", 4],
  ["p02-board.png", 7],
  ["p03-cases.png", 6],
  ["p04-log.png", 4],
  ["p05-how.png", 5],
  ["s04-close.png", 4],
];
writeFileSync(
  list,
  clips.map(([f, t]) => `file '${f}'\nduration ${t}`).join("\n") + `\nfile '${clips.at(-1)[0]}'\n`,
);

const mp4 = path.join(root, "app", "public", "demo.mp4");
mkdirSync(path.dirname(mp4), { recursive: true });
execFileSync(
  "ffmpeg",
  [
    "-y",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    list,
    "-vf",
    "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
    "-pix_fmt",
    "yuv420p",
    "-r",
    "30",
    mp4,
  ],
  { cwd: frames, stdio: "inherit" },
);

const png = path.join(root, "docs", "architecture.png");
execFileSync("ffmpeg", ["-y", "-i", path.join(frames, "p05-how.png"), png], { stdio: "inherit" });
console.log("wrote", mp4, "shift", shift?.id || "");

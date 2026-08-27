import { chromium } from "playwright";
import { mkdirSync } from "fs";
import path from "path";

const base = process.env.APP_URL || "http://127.0.0.1:3010";
const outDir = path.join(process.cwd(), "..", "evidence", "video");
mkdirSync(outDir, { recursive: true });

const launch = { headless: true, channel: process.env.PW_CHANNEL || "chrome" };
const browser = await chromium.launch(launch);
const context = await browser.newContext({
  viewport: { width: 1280, height: 720 },
  recordVideo: { dir: outDir, size: { width: 1280, height: 720 } },
});
const page = await context.newPage();
const linger = (ms) => page.waitForTimeout(ms);

await page.goto(base, { waitUntil: "networkidle" });
await linger(2500);

const [res] = await Promise.all([
  page.waitForResponse((r) => r.url().includes("/shifts/demo") && r.request().method() === "POST"),
  page.getByRole("button", { name: /Run Harbor Auto overnight/i }).click(),
]);
const shift = await res.json();
await page.waitForURL(/\/shift\//, { timeout: 30000 });
await linger(3000);
await page.mouse.wheel(0, 700);
await linger(2500);
await page.mouse.wheel(0, 900);
await linger(2500);

await page.goto(`${base}/how`, { waitUntil: "networkidle" });
await linger(3500);

if (shift?.id) {
  await page.goto(`${base}/shift/${shift.id}`, { waitUntil: "networkidle" });
  await linger(2000);
}

await context.close();
await browser.close();
console.log("recorded", outDir, shift?.id || "");

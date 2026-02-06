import { test, expect } from "@playwright/test";

test("en dashboard route responds", async ({ page }) => {
  await page.goto("/en");
  await expect(page.locator("h1")).toBeVisible();
});

test("fr dashboard route responds", async ({ page }) => {
  await page.goto("/fr");
  await expect(page.locator("h1")).toBeVisible();
});

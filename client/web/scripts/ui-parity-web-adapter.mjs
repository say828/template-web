import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const screens = JSON.parse(
  fs.readFileSync(path.resolve(scriptDir, "../src/lib/specScreens.json"), "utf8"),
);
const routes = JSON.parse(
  fs.readFileSync(path.resolve(scriptDir, "../src/lib/specRouteCatalog.json"), "utf8"),
);

const routeMap = new Map(routes.map((entry) => [entry.id, entry.route]));

export default {
  service: "templates-web",
  targetBaseUrl: "http://127.0.0.1:4301",
  viewport: {
    width: 1440,
    height: 1024,
  },
  screens: screens.map((screen) => ({
    id: screen.id,
    title: screen.title,
    route: routeMap.get(screen.id) ?? "/",
    referenceImage: `sdd/03_verify/10_test/ui_parity/reference/${screen.id}.png`,
    readySelector: "body",
    readyTimeoutMs: 10000,
    tags: ["template", "web"],
  })),
  async preparePage(page, { route }) {
    await page.route("**/auth/me", async (routeRequest) => {
      await routeRequest.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: "tmpl-web",
          name: "Template Web User",
          email: "operator@example.com",
          role: "member",
        }),
      });
    });
    await page.addInitScript(() => {
      window.localStorage.setItem(
        "web.auth.token",
        JSON.stringify({
          access_token: "template-access-token",
          token_type: "bearer",
          user_id: "tmpl-web",
        }),
      );
    });
    if (route === "/login") {
      await page.addInitScript(() => {
        window.localStorage.removeItem("web.auth.token");
      });
    }
  },
  async waitForReady(page) {
    await page.waitForLoadState("networkidle");
  },
  async resolveMaskRects() {
    return [];
  },
};

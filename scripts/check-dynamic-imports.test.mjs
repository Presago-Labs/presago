import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { findMissingVendorImports } from "./check-dynamic-imports.mjs";

test("checks vendor dynamic-import targets relative to the importing file", (t) => {
  const frontend = mkdtempSync(join(tmpdir(), "presago-imports-"));
  t.after(() => rmSync(frontend, { recursive: true, force: true }));
  mkdirSync(join(frontend, "pages", "vendor"), { recursive: true });
  writeFileSync(join(frontend, "pages", "wallet.js"),
    'const LOCAL_API_PATH = "./vendor/freighter-api.js"; import(LOCAL_API_PATH);');
  writeFileSync(join(frontend, "pages", "vendor", "freighter-api.js"), "export {};");
  assert.deepEqual(findMissingVendorImports(frontend), []);
  rmSync(join(frontend, "pages", "vendor", "freighter-api.js"));
  assert.match(findMissingVendorImports(frontend).join("\n"), /pages[/\\]wallet\.js: missing dynamic import target/);
});

test("checks both required vendor bundles", (t) => {
  const frontend = mkdtempSync(join(tmpdir(), "presago-imports-"));
  t.after(() => rmSync(frontend, { recursive: true, force: true }));
  writeFileSync(join(frontend, "soroban.js"), 'const LOCAL_SDK_PATH = "./vendor/stellar-sdk.js";');
  writeFileSync(join(frontend, "wallet.js"), "const LOCAL_API_PATH = './vendor/freighter-api.js';");
  assert.equal(findMissingVendorImports(frontend).length, 2);
  mkdirSync(join(frontend, "vendor"));
  writeFileSync(join(frontend, "vendor", "stellar-sdk.js"), "");
  writeFileSync(join(frontend, "vendor", "freighter-api.js"), "");
  assert.deepEqual(findMissingVendorImports(frontend), []);
});

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// Exercise the actual validator and its reported failures, not a copied regex.
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const validator = path.resolve(__dirname, '../scripts/validate-frontend.mjs');
const cases = [
  ['unique IDs', '<div id="one"></div><span id="two"></span>', []],
  ['repeated ID', '<div id="same"></div><span id="same"></span>', ['same']],
  ['case-sensitive values', '<div id="Name"></div><span id="name"></span>', []],
  ['no preceding whitespace', '<divid="one"></div><span id="one"></span>', []],
  ['comment content is currently scanned', '<!-- id="note" --><div id="note"></div>', ['note']],
  ['newline and tab are whitespace', '<div\n\tid="line"></div><span id="line"></span>', ['line']],
  ['attribute names are case-insensitive', '<div ID="cap"></div><span id="cap"></span>', ['cap']],
  ['single quotes and multiple duplicates', "<i id='b'></i><i id='a'></i><i id='b'></i><i id='a'></i><i id='b'></i>", ['b', 'a']],
];
for (const [name, body, duplicates] of cases) {
  test(name, (t) => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'validator-ids-'));
    t.after(() => fs.rmSync(root, { recursive: true, force: true }));
    fs.mkdirSync(path.join(root, 'scripts'));
    fs.mkdirSync(path.join(root, 'frontend'));
    // Keep sibling helper modules when the validator gains imports.
    for (const name of fs.readdirSync(path.dirname(validator))) {
      if (name.endsWith('.mjs')) fs.copyFileSync(path.join(path.dirname(validator), name), path.join(root, 'scripts', name));
    }
    fs.writeFileSync(path.join(root, 'frontend/index.html'),
      '<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Fixture</title></head><body>' + body + '</body></html>');
    const run = spawnSync(process.execPath, [path.join(root, 'scripts/validate-frontend.mjs')], {
      cwd: root, encoding: 'utf8', timeout: 5000,
    });
    assert.ifError(run.error);
    assert.equal(run.status, duplicates.length ? 1 : 0, run.stderr);
    const failures = run.stderr.split(/\r?\n/).filter((line) => line.startsWith('- '));
    assert.deepEqual(failures, duplicates.map((id) => `- frontend/index.html: contains duplicate id '${id}'`));
    if (!duplicates.length) assert.match(run.stdout, /Validated 1 HTML pages/);
  });
}

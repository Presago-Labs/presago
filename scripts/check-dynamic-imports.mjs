import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, extname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export function findMissingVendorImports(frontendRoot) {
  const missing = [];
  const visit = (directory) => {
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      if (entry.name === "vendor") continue;
      const path = join(directory, entry.name);
      if (entry.isDirectory()) {
        visit(path);
      } else if (entry.isFile() && extname(path) === ".js") {
        const source = readFileSync(path, "utf8");
        // Covers string constants used by import() without executing frontend code.
        for (const match of source.matchAll(/(["'])(\.\/vendor\/[^"'\r\n]+)\1/g)) {
          const target = resolve(dirname(path), match[2]);
          if (!existsSync(target) || !statSync(target).isFile()) {
            missing.push(`${relative(frontendRoot, path)}: missing dynamic import target '${match[2]}'`);
          }
        }
      }
    }
  };
  visit(frontendRoot);
  return missing;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const frontendRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../frontend");
  const missing = findMissingVendorImports(frontendRoot);
  if (missing.length) {
    console.error("Missing frontend vendor import targets:\n" + missing.join("\n"));
    process.exitCode = 1;
  } else {
    console.log("All frontend vendor import targets exist.");
  }
}

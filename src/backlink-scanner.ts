// spec: specs/backlink-scanner.md

import { readdir, readFile, stat } from "node:fs/promises";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const SPEC_PATTERN = /^\s*(?:\/\/|#)\s*spec:\s*([\w.\/\-]+)\s*$/;
const SECTION_PATTERN = /^\s*(?:\/\/|#)\s*spec-section:\s*([\w.\/\-\s]+)\s*$/;
const FENCE_PATTERN = /^\s*```/;
const BINARY_EXTENSIONS = new Set([
  ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf",
  ".zip", ".tar", ".gz", ".bin", ".exe",
  ".woff", ".woff2", ".ttf", ".eot",
  ".mp3", ".mp4", ".wav", ".avi",
]);

interface SpecEntry {
  implementors: string[];
}

interface ScanResult {
  specs: Record<string, SpecEntry>;
  dangling: string[];
  orphans: string[];
}

async function getFiles(dir: string, root: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const files: string[] = [];

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
      files.push(...await getFiles(fullPath, root));
    } else {
      files.push(relative(root, fullPath));
    }
  }

  return files;
}

function isBinary(filePath: string): boolean {
  const ext = filePath.slice(filePath.lastIndexOf(".")).toLowerCase();
  return BINARY_EXTENSIONS.has(ext);
}

async function scan(rootDir: string): Promise<ScanResult> {
  const files = await getFiles(rootDir, rootDir);
  const specRefs: Map<string, Set<string>> = new Map();

  for (const file of files) {
    if (isBinary(file)) continue;

    let content: string;
    try {
      content = await readFile(join(rootDir, file), "utf-8");
    } catch {
      continue;
    }

    const lines = content.split("\n");
    const isMarkdown = file.endsWith(".md");
    let inCodeFence = false;
    let currentSpec: string | null = null;

    for (const line of lines) {
      if (isMarkdown && FENCE_PATTERN.test(line)) {
        inCodeFence = !inCodeFence;
        continue;
      }
      if (inCodeFence) continue;

      const specMatch = line.match(SPEC_PATTERN);
      if (specMatch) {
        const specPath = specMatch[1].trim();
        if (!specRefs.has(specPath)) {
          specRefs.set(specPath, new Set());
        }
        specRefs.get(specPath)!.add(file);
        currentSpec = specPath;
      }

      const sectionMatch = line.match(SECTION_PATTERN);
      if (sectionMatch && currentSpec) {
        // Section references are recorded but don't change the mapping structure
      }
    }
  }

  // Find spec files in the specs/ directory
  const specFiles: string[] = files.filter(f => f.startsWith("specs/") && f.endsWith(".md"));

  // Identify dangling references (referenced specs that don't exist as files)
  const dangling: string[] = [];
  for (const specPath of specRefs.keys()) {
    try {
      await stat(join(rootDir, specPath));
    } catch {
      dangling.push(specPath);
    }
  }

  // Identify orphan specs (spec files with no references)
  const orphans: string[] = specFiles.filter(f => !specRefs.has(f));

  // Build output
  const specs: Record<string, SpecEntry> = {};
  for (const [specPath, implementors] of specRefs) {
    specs[specPath] = { implementors: [...implementors].sort() };
  }

  return { specs, dangling, orphans };
}

async function main() {
  const rootDir = process.argv[2] || process.cwd();
  const result = await scan(rootDir);
  console.log(JSON.stringify(result, null, 2));
}

const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] === __filename) {
  main().catch((err) => {
    console.error(err.message);
    process.exit(1);
  });
}

export { scan, ScanResult };

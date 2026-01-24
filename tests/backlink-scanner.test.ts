// spec: specs/backlink-scanner.md

import { describe, it, beforeEach, afterEach } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, rm, mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { scan } from "../src/backlink-scanner.ts";

let testDir: string;

beforeEach(async () => {
  testDir = await mkdtemp(join(tmpdir(), "backlink-test-"));
});

afterEach(async () => {
  await rm(testDir, { recursive: true });
});

describe("backlink scanner", () => {
  describe("scanning for backlinks", () => {
    it("finds // spec: annotations", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/auth.md"), "# Auth");
      await writeFile(join(testDir, "src.ts"), '// spec: specs/auth.md\nconst x = 1;');

      const result = await scan(testDir);

      assert.deepEqual(result.specs["specs/auth.md"].implementors, ["src.ts"]);
    });

    it("finds # spec: annotations", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/auth.md"), "# Auth");
      await writeFile(join(testDir, "script.py"), '# spec: specs/auth.md\nx = 1');

      const result = await scan(testDir);

      assert.deepEqual(result.specs["specs/auth.md"].implementors, ["script.py"]);
    });

    it("records multiple implementors for one spec", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/auth.md"), "# Auth");
      await writeFile(join(testDir, "a.ts"), "// spec: specs/auth.md");
      await writeFile(join(testDir, "b.ts"), "// spec: specs/auth.md");

      const result = await scan(testDir);

      assert.deepEqual(result.specs["specs/auth.md"].implementors, ["a.ts", "b.ts"]);
    });

    it("records multiple spec references from one file", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/auth.md"), "# Auth");
      await writeFile(join(testDir, "specs/rate.md"), "# Rate");
      await writeFile(join(testDir, "src.ts"), "// spec: specs/auth.md\n// spec: specs/rate.md");

      const result = await scan(testDir);

      assert.deepEqual(result.specs["specs/auth.md"].implementors, ["src.ts"]);
      assert.deepEqual(result.specs["specs/rate.md"].implementors, ["src.ts"]);
    });
  });

  describe("dangling references", () => {
    it("reports annotations referencing nonexistent specs", async () => {
      await writeFile(join(testDir, "src.ts"), "// spec: specs/nonexistent.md");

      const result = await scan(testDir);

      assert.ok(result.dangling.includes("specs/nonexistent.md"));
    });
  });

  describe("orphan specs", () => {
    it("reports spec files with no references", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/orphan.md"), "# Orphan");
      await writeFile(join(testDir, "src.ts"), "const x = 1;");

      const result = await scan(testDir);

      assert.ok(result.orphans.includes("specs/orphan.md"));
    });

    it("does not report specs that have references", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/used.md"), "# Used");
      await writeFile(join(testDir, "src.ts"), "// spec: specs/used.md");

      const result = await scan(testDir);

      assert.deepEqual(result.orphans, []);
    });
  });

  describe("edge cases", () => {
    it("skips binary files", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/auth.md"), "# Auth");
      await writeFile(join(testDir, "image.png"), "// spec: specs/auth.md");

      const result = await scan(testDir);

      assert.deepEqual(result.specs, {});
    });

    it("skips dotfiles and node_modules", async () => {
      await mkdir(join(testDir, ".git"), { recursive: true });
      await mkdir(join(testDir, "node_modules/dep"), { recursive: true });
      await writeFile(join(testDir, ".git/config"), "// spec: specs/auth.md");
      await writeFile(join(testDir, "node_modules/dep/index.js"), "// spec: specs/auth.md");

      const result = await scan(testDir);

      assert.deepEqual(result.specs, {});
    });

    it("handles empty directories", async () => {
      await mkdir(join(testDir, "empty"), { recursive: true });

      const result = await scan(testDir);

      assert.deepEqual(result.specs, {});
      assert.deepEqual(result.dangling, []);
      assert.deepEqual(result.orphans, []);
    });

    it("returns sorted implementors", async () => {
      await mkdir(join(testDir, "specs"), { recursive: true });
      await writeFile(join(testDir, "specs/auth.md"), "# Auth");
      await writeFile(join(testDir, "z.ts"), "// spec: specs/auth.md");
      await writeFile(join(testDir, "a.ts"), "// spec: specs/auth.md");
      await writeFile(join(testDir, "m.ts"), "// spec: specs/auth.md");

      const result = await scan(testDir);

      assert.deepEqual(result.specs["specs/auth.md"].implementors, ["a.ts", "m.ts", "z.ts"]);
    });
  });
});

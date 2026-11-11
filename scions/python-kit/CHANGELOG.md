# Changelog

python-kit (formerly python-starter) is two things, and each entry says which one changed:

- **Template**: what `copier copy` / `copier update` puts in a generated project.
- **Exported docs**: what a repo that grafts python-kit gets in `scions/python-kit/`
  (`.gitattributes`: `docs/architecture`, `docs/decisions`, `docs/guides`, `docs/reference`, the
  `src/` and `tests/` they cite, `copier.yml`, `pyproject.toml.jinja`, and this file).

Generated projects with `graft_docs` pin python-kit to the commit they came from, so
`copier update`, not graft's weekly PR, moves them between these versions.

## v2.0.1 - 2026-11-11

### Template

- `TEMPLATE_STATUS.md` names the template's canonical URL as its repository (it showed Copier's temporary clone
  directory, which changed on every update and caused a conflict), and says "generated from **python-kit**".

## v2.0.0 - 2026-11-11

**Renamed:** python-starter is now **python-kit**: a kit you generate a project from and keep upgrading, with
`copier update` for the structure and graft for the pattern docs, moving together. Old GitHub URLs redirect;
the old Forgejo SSH URL does not.

### Template

- `.copier-answers.yml` records `_src_path: https://github.com/danielnaab/python-kit` whatever path the project
  was generated from, so `copier update` works from any checkout (a `.graft/…` or `../` path only resolved where
  it was first run).
- With `graft_docs`: the flake grafts `python-kit` (was `python-starter`) and knowledge-base-kit v2.0.0 (was
  meta-knowledge-base v1.0.1) into `scions/`, uses graft v2.9.0's `mkFlake` (was v2.4.1's `mkGraft` with `deps`),
  and carries graft v2.9.0's two workflows. Links in README, TEMPLATE_STATUS and `docs/` follow the new paths.
- The generated README's install step says `cd <your-project>` (it said `cd python-starter`).

### Exported docs

- The project's own name throughout; links to the conventions point at knowledge-base-kit v2.0.0.

### Migration

In a generated project:

1. `.copier-answers.yml`: set `_src_path: https://github.com/danielnaab/python-kit` (by hand, this once).
2. `copier update --vcs-ref v2.0.0` and resolve conflicts. With `graft_docs`, the update rewrites `flake.nix`;
   then `nix run .#graft` (`scions/python-starter/` becomes `scions/python-kit/`, `scions/meta-knowledge-base/`
   becomes `scions/knowledge-base-kit/`) and commit `flake.nix`, `flake.lock`, `scions/` and the workflows.
3. Your own files that link into `scions/python-starter/` or `scions/meta-knowledge-base/` (the update doesn't
   touch files it skips, such as README.md and docs/agents.md): change the paths.

In a repo that grafts python-starter's docs (not generated from it): rename the input to
`python-kit = { url = "github:danielnaab/python-kit/v2.0.0"; flake = false; };`, `nix run .#graft`, and update
links from `scions/python-starter/` to `scions/python-kit/`.

### Also in this release (unreleased since v1.3.0)

#### Added
- CHANGELOG.md, covering every tag from v1.0.0. It is exported (graft's scions get it) and
  excluded from generated projects (`copier.yml` `_exclude`).

#### Changed
- Template: `TEMPLATE_STATUS.md`'s "Before updating" step links this file instead of "the
  changelog (if available)".

#### Fixed
- Template: with `graft_docs`, generating a project runs `nix run .#graft` before the first
  commit. That commit used to have no `scions/`, so its README and docs links were broken; a
  link-checking commit hook rejected it, and Copier then deleted the new project.

## v1.3.0 - 2026-11-04

### Changed
- Template: the rendered `flake.nix` pins graft to the tag `v2.4.1` instead of the `v2` branch.
  graft-upgrade leaves an input pinned to a branch alone, so the old pin never moved; a tag pin
  lets the weekly PR move graft itself to newer tags in its major.
- Template: `.forgejo/workflows/graft-check.yaml` and `graft-upgrade.yaml` are graft v2.4.1's.
  Both start with `# managed by graft`, and graft-upgrade replaces a workflow carrying that line
  with the copy each new graft version ships; delete the line to keep local edits. Their steps
  are now `nix run .#graft-ci -- check`, `-- upgrade` and `-- pr` at the pinned graft version.
  `graft-upgrade.yaml` is two jobs: `upgrade` (job token only) and `pr` (opens or updates the PR
  from the default branch's graft, with `GRAFT_PR_TOKEN`).
- Template: `TEMPLATE_STATUS.md` says the weekly PR covers graft as well as meta-knowledge-base,
  stays within a major, is gated by the whole `nix flake check`, and quotes the provider's
  CHANGELOG; and what the `# managed by graft` line does.
- Exported docs: unchanged.

### Upgrading

In a project generated with `graft_docs`: `copier update --trust`, then `nix flake lock` (the
`graft` input's URL changed from `v2` to `v2.4.1`), `nix flake check`, and commit `flake.nix`,
`flake.lock` and `.forgejo/workflows/`. A workflow you want to keep edited needs its
`# managed by graft` line deleted, or the next graft upgrade replaces it.

## v1.2.0 - 2026-11-03

### Changed
- Template: `graft-upgrade.yaml` is graft v2.2.2's. It opens the PR with the Actions secret
  `GRAFT_PR_TOKEN`, falling back to the job token, which Forgejo refuses for opening a PR on a
  private repo. If opening the PR fails, the run fails with the HTTP status and a compare link
  for the pushed `graft/upgrade` branch (and, on a 404, names the missing secret).
- Template: `TEMPLATE_STATUS.md` says to set `GRAFT_PR_TOKEN` (a `write:repository` token for a
  bot user), and that a user-level secret covers every repo you own.
- Exported docs: unchanged.

### Upgrading

`copier update --trust`. On a private Forgejo repo, set the `GRAFT_PR_TOKEN` Actions secret
(user-level or repo-level) or the weekly run will push `graft/upgrade` but fail to open the PR.

## v1.1.0 - 2026-11-03

### Added
- Template: with `graft_docs`, generated projects get graft's workflows (from graft v2.2.1) in
  `.forgejo/workflows/`: `graft-check.yaml` checks on every PR and push to `main` that
  `scions/` matches `flake.lock`; `graft-upgrade.yaml` runs weekly (Mondays 06:23 UTC) and opens
  a PR from `graft/upgrade` when a tag-pinned scion has a newer tag.
- Template: `TEMPLATE_STATUS.md` has a "Keeping the grafted docs current" section on the two
  workflows and the manual `nix run .#graft-outdated` / `nix run .#graft-upgrade`.

### Changed
- Template: new projects pin meta-knowledge-base `v1.0.1` (was `v1.0.0`).
- Exported docs: unchanged.

## v1.0.1 - 2026-11-03

### Changed
- Template: grafted copies live in `scions/` instead of `vendor/` (graft v2.1's directory):
  the generated README, `TEMPLATE_STATUS.md`, `docs/README.md`, `docs/agents.md`, `flake.nix`
  comments and the `graft_docs` question all say `scions/`.
- `docs/copier/dependency-pattern.md` (the template's own doc, not exported) says `scions/`.
- Exported docs: only `copier.yml`'s `graft_docs` help text (`vendor/` to `scions/`).

### Upgrading

In a project generated from v1.0.0 with `graft_docs`: `copier update --trust`, then
`nix flake update graft` (scions/ needs graft 2.1 or later), `git mv vendor scions`,
`nix run .#graft`, and commit. `README.md` and `docs/agents.md` are
`_skip_if_exists`, so copier leaves them as they are: replace `vendor/` with `scions/` in their
links yourself. Done when `grep -rn 'vendor/' README.md docs/` finds nothing and `nix flake check`
passes.

## v1.0.0 - 2026-11-02

The first tagged release, and the first that is a graft v2 provider. Before it, the template
was used from untagged commits.

### Added
- Exported docs: `.gitattributes` exports the pattern docs (`docs/architecture`,
  `docs/decisions`, `docs/guides`, `docs/reference`), the `src/` and `tests/` they cite,
  `copier.yml` and `pyproject.toml.jinja`. The rest of the repo is export-ignored.
- Template: a `graft_docs` question (default yes; needs Nix). With it, a generated project gets a
  `flake.nix` that grafts meta-knowledge-base `v1.0.0` and python-starter at the exact commit the
  project was generated from (`_copier_conf.vcs_ref_hash`) into `vendor/`, so the docs match the
  code. With it off, the same links point at GitHub at that commit.

### Changed
- Template: generated docs link into the grafted copies (or GitHub). Before, `docs/agents.md`
  and `docs/README.md` linked a sibling `../python-starter` checkout,
  `../.graft/meta-knowledge-base/AGENTS.md` and an ungenerated `knowledge-base.yaml`, and the
  generated README linked `docs/decisions/`, `docs/guides/` and the like, which copier never
  generates (12 broken links per project).
- `docs/copier/dependency-pattern.md` describes the graft-based pattern instead of
  knowledge-base imports from a sibling checkout.

### Removed
- graft v1: `graft.yaml`, `graft.lock`, `.gitmodules` and the `.graft/meta-knowledge-base`
  submodule.
- `docs/knowledge-base.yaml` no longer imports `.graft/meta-knowledge-base`.

### Upgrading

From a project generated from an earlier, untagged commit:

1. Commit your work, then `copier update --trust` and answer `graft_docs` (yes needs Nix).
2. With `graft_docs`: `nix run .#graft`, then commit `flake.nix`, `flake.lock` and the grafted
   directory (`vendor/` at v1.0.0, `scions/` from v1.0.1; update straight to the newest tag
   and take `scions/`).
3. `README.md` and `docs/agents.md` are `_skip_if_exists`, so copier doesn't touch them. Fix
   their links by hand, using the freshly generated `docs/README.md` as the model:
   `../python-starter/docs/` becomes `../scions/python-starter/docs/` in `docs/`;
   `docs/decisions/`, `docs/guides/`, `docs/architecture/`, `docs/reference/` in `README.md`
   become `scions/python-starter/docs/...`; links to `../.graft/meta-knowledge-base/AGENTS.md`
   become `../scions/meta-knowledge-base/README.md`; drop links to `knowledge-base.yaml`.
   Without `graft_docs`, point them at
   `https://github.com/danielnaab/python-starter/blob/<_commit>/docs/...` instead (`_commit` is
   in `.copier-answers.yml`).
4. If the project carries graft v1 files from the template (`graft.yaml`, `graft.lock`, a
   `.gitmodules` entry or directory for `.graft/meta-knowledge-base`), remove them.

Done when `grep -rn -e '\.\./python-starter' -e '\.graft/' -e 'knowledge-base.yaml' README.md docs/`
finds nothing and, with `graft_docs`, `nix flake check` passes.

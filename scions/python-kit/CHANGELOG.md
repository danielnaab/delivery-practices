# Changelog

python-kit (formerly python-starter) is two things, and each entry says which one changed:

- **Template**: what `copier copy` / `copier update` puts in a generated project.
- **Exported docs**: what a repo that grafts python-kit gets in `scions/python-kit/`
  (`.gitattributes`: `docs/architecture`, `docs/decisions`, `docs/guides`, `docs/reference`, the
  `src/` and `tests/` they cite, `copier.yml`, `pyproject.toml.jinja`, and this file).

Generated projects with `graft_docs` pin python-kit to the commit they came from, in their `flake.nix`. From
v2.2.0 the python-kit-upgrade PR moves that pin with each `copier update` (before, the update's merge did);
graft's weekly PR doesn't.

## v2.2.0 - 2026-11-11

### Template

- `flake.nix` is the project's: it is in `_skip_if_exists`, so `copier update` no longer rewrites it (an update
  that moved the python-kit pin conflicted in every project whose `flake.nix` had changed, as graft-upgrade
  changes it). python-kit-upgrade moves the python-kit input, and nothing else in the file, to the commit of
  the tag it updated to (a `url = "github:danielnaab/python-kit/..."` line, whatever its layout; the run fails
  if there isn't exactly one), then runs `nix run .#graft` as before. graft-upgrade still moves graft and the
  other pins. The PR job is unchanged: it runs none of the branch's code.
- `docs/agents.md` is generated once: `_exclude` lists it during an update (`_copier_operation == 'update'`),
  so an update neither changes it nor recreates it after you delete it. It stays in `_skip_if_exists` too, so
  `copier recopy` (which runs as a copy) doesn't overwrite it.
- `_min_copier_version` is 9.10.3. Older copier doesn't apply the new template's `_exclude` to its render of
  the old one, so a file this release newly excludes looks removed from the template and the update deletes
  it: with 9.10.2, a v2.1.0 to v2.2.0 update deletes `docs/agents.md`, `tests/conftest.py` and
  `tests/fakes/fake_repository.py`.
- python-kit-upgrade counts pytest's exit 5 ("no tests ran") as passing, so a project without example code
  and without tests of its own no longer gets every PR titled `[checks failing]`.
- With `include_example_code: false`, the example code is not generated at all. Before, its files rendered as
  docstring-only stubs (`domain/entity.py`, `errors.py`, `repository.py`, `adapters/in_memory_repository.py`,
  `services/example_service.py`, `cli/commands/example.py`, `tests/conftest.py`, `tests/fakes/fake_repository.py`,
  `tests/unit/test_entity.py`, `test_example_service.py`, `tests/integration/test_in_memory_repository.py`), and
  being in `_skip_if_exists`, which only protects files that exist, every `copier update` recreated the ones a
  project had deleted, as did the weekly python-kit-upgrade PR. `copier.yml` `_exclude` now lists them under
  `{% if not include_example_code %}`, and the example entries of `_skip_if_exists` (including `tests/unit/*.py`
  and `tests/integration/*.py`) apply only with example code, so without it an update respects deleted files
  such as `tests/unit/__init__.py`. Nothing imported the stubs: the `__init__.py` exports, `services/context.py`
  and `cli/main.py` are unchanged and keep their skeleton comments.
- `TEMPLATE_STATUS.md` lists the example files as protected only with example code, and says what happens
  without it.
- The generated `docs/README.md` drops its `**Version**: <commit>` line (`TEMPLATE_STATUS.md` and
  `.copier-answers.yml` record the version): it changed with every release, so every update conflicted in a
  project that had rewritten `docs/README.md` (copier 9.10.3 marks the conflict; later copier keeps your file).

### Exported docs

- The example templates in `src/` and `tests/` lose their `{% else %}` stub branches.

### Migration

`copier update --trust --vcs-ref v2.2.0` (copier 9.10.3 or later: an older one deletes `docs/agents.md` and,
without example code, `tests/conftest.py` and `tests/fakes/fake_repository.py`). The update leaves `flake.nix` alone, and
its v2.2.0 migration moves the python-kit pin to v2.2.0's commit (the python-kit-upgrade workflow running this
update is still v2.1.0's, which doesn't); if it finds no single python-kit `url` line it stops and says so,
and you set the pin by hand. Then `nix run .#graft`, `nix flake check`, and commit `flake.nix`, `flake.lock`,
`scions/` and `.forgejo/workflows/python-kit-upgrade.yaml`. The weekly PR does this too, except that it
changes a workflow, so it is pushed for you to open.

By hand: the comment above `flake.nix`'s python-kit input says `copier update` moves it. Now python-kit-upgrade
(or, this once, the v2.2.0 migration) moves it, and the update never touches `flake.nix` again, so edit that
comment to say so.

With a copier older than 9.15.1 (seen with 9.10.3), a project that rewrote `docs/README.md` gets one conflict there: v2.1.0's render
still has the `**Version**` line this release drops. Keep your version. Copier 9.15.1 or later keeps it without a
conflict. It happens only on this update.

Nothing is deleted: stub example files a project without example code still has stay, and are yours to
delete; an update won't bring them back, or `docs/agents.md`.

## v2.1.0 - 2026-11-11

### Template

- With `graft_docs`: a `.forgejo/workflows/python-kit-upgrade.yaml` workflow, modeled on graft-upgrade. Weekly
  (Mondays 06:41 UTC) it runs `copier update` to python-kit's newest tag in the project's major, then
  `nix run .#graft`, `nix flake check` and the tests, pushes the result to `python-kit/upgrade` and opens a PR
  quoting this CHANGELOG. Conflicts and failing checks are pushed and named in the PR's title; a new major is
  not taken (the run warns). The update runs in a job with only the job token; the PR job, with the
  `GRAFT_PR_TOKEN` secret, runs none of the branch's code, and leaves a branch that changes `.forgejo/` or
  `.github/` workflows for you to open. copier, uv and Python come from nixpkgs `nixos-26.05`.
- `copier.yml` `_migrations` are real: the v2.0.0 migration renames `scions/python-starter/` to
  `scions/python-kit/` and `scions/meta-knowledge-base/` to `scions/knowledge-base-kit/` in the project's own
  tracked files (not `scions/` or CHANGELOG.md), the step v2.0.0's Migration left by hand; the v2.1.0
  migration makes this release's ruff fixes in the example files the update skips, where they still read as
  generated. The placeholder v0.2.0 migration is gone. `_min_copier_version` is 9.3.0, for the
  `command`/`when` form.
- `TEMPLATE_STATUS.md`: after `copier update`, `nix run .#graft`; and what the weekly update PR does.
  `docs/copier/template-design.md` (the template's own docs): `graft_docs`' files, migrations, the workflow.
- graft's workflows (`.forgejo/workflows/graft-check.yaml`, `graft-upgrade.yaml`) are in `_skip_if_exists`:
  a new project still gets them, and from then on graft-upgrade alone moves them with graft's pin, so a
  python-kit update neither conflicts with nor reverts them (and its PR is refused only when
  `python-kit-upgrade.yaml` itself changes).
- The generated code is `ruff check` clean: `entity.id` for `getattr(entity, "id")` (B009), `T | None` for
  `Optional[T]` (UP045), and `raise typer.Exit(code=1) from e` in the example CLI commands (B904). `tests`
  imports are an isort block of their own (`known-local-folder`): a package named after "tests"
  alphabetically got I001. With `graft_docs`, ruff skips `scions/` (graft output; it reported
  knowledge-base-kit's import order).

### Exported docs

- `docs/architecture/architecture.md` and `docs/decisions/003-protocol-di.md`: the `Repository` protocol
  examples use `T | None`.

### Migration

In a generated project: `copier update --trust --vcs-ref v2.1.0` (from v1.x, first set `_src_path` as in
v2.0.0's Migration). With `graft_docs`: `nix run .#graft`, `nix flake check`, and commit `flake.nix`,
`flake.lock`, `scions/` and `.forgejo/workflows/python-kit-upgrade.yaml`. From then on the weekly PR does
this; on a private Forgejo repo it needs the `GRAFT_PR_TOKEN` secret, as graft-upgrade does.

The update and its v2.1.0 migration make the ruff fixes; in example code you have changed, `ruff check`
shows what is left (`--fix` takes B009 and UP045; B904 needs `from e` by hand).

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

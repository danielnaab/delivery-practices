# Presentations

Temporal slide decks for specific meetings or events. These are **ephemeral artifacts** — date-prefixed and tied to specific occasions.

## Building Decks

Slide decks use [Marp](https://marp.app/) (Markdown Presentation Ecosystem).

### Prerequisites

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli
```

### Generate HTML

```bash
# From repo root
marp notes/presentations/2026-01-30-usai-practice-lab-intro.md -o notes/presentations/2026-01-30-usai-practice-lab-intro.html
```

### Generate PDF

```bash
# Requires Chrome/Chromium
marp notes/presentations/2026-01-30-usai-practice-lab-intro.md --pdf -o notes/presentations/2026-01-30-usai-practice-lab-intro.pdf
```

### Preview with Live Reload

```bash
marp -s notes/presentations/
# Opens browser at http://localhost:8080
```

## Conventions

- **Naming**: `YYYY-MM-DD-<event-or-meeting>.md`
- **Location**: Always in `notes/presentations/` (not `docs/`)
- **Generated files**: Add `.html` and `.pdf` to `.gitignore` or commit as needed for sharing
- **Planning notes**: Keep facilitation details in parent `notes/` directory, link to deck

## Decks

| Date | Deck | Planning Note |
|------|------|---------------|
| 2026-01-30 | [USAi Practice Lab Intro](2026-01-30-usai-practice-lab-intro.md) | [Planning](../2026-01-30-usai-practice-lab-intro.md) |

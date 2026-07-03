Use CodeGraph for codebase-structure tasks whenever it is available.

Prefer these CodeGraph calls before broad file scans:
- `codegraph query <symbol>`
- `codegraph callers <symbol>`
- `codegraph callees <symbol>`
- `codegraph impact <symbol>`
- `codegraph context "<task>"`

For a repository that is not yet indexed:
- create or update `AGENTS.md` in the repo root
- run `codegraph init -i`
- verify with `codegraph status`

For ongoing edits:
- use `codegraph sync`

For a stale or heavily changed repo:
- use `codegraph index`

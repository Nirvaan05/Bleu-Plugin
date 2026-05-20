# Changelog

All notable changes to the Bleu Claude Code plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`.
- README badges and explicit "Claude Code plugin" positioning.
- Discoverability metadata: expanded `tags` in `marketplace.json` and `keywords` in `plugin.json` covering `claude-code`, `claude-code-plugin`, `claude-code-skill`, `agent-skills`, `subagents`, `spec-driven-development`.

### Changed
- README H1 from `Bleu` to `Bleu - a Claude Code plugin for living blueprints`.
- Top-level description in both manifests now leads with "Claude Code plugin".

### Fixed
- kb-linter tool whitelist now includes `Write` (it authors files in `.reflection/proposals/`; previously listed read-only tools only).
- Stale rule-file references updated from `schema/rules.md` to the authoritative `.claude/rules/blueprint-schema.md` (the historical migration note is preserved intentionally).
- Corrected the raw/ ingestion hook from `PostToolUse` to `FileChanged` in the advanced-architecture ingest pipeline and the SKILL summary, since `PostToolUse` does not fire for MCP servers or external scripts writing to `raw/`.
- Auditor agent-hook tool scope: documented consistently as Read/Grep/Glob plus `Write` confined to `.reflection/` (it records verdicts and escalations), resolving a "read-only but writes verdicts" contradiction across `advanced-architecture.md` and `claude-code-integration.md`.
- Removed the non-existent `kb-auditor` from the `Agent(...)` allowlist in `claude-code-integration.md` (the Auditor is an `agent` hook on `SubagentStop`, not a separate agent file).
- `SessionStart` resume hook matcher changed from `resume` to `startup|resume` in `session-persistence.md` so blueprint state also loads on a fresh session start (e.g. after `/clear`), matching the rest of the skill.
- Clarified that the Researcher stages raw captures in `raw/research/` while the Curator promotes synthesized findings to `research/` (episodic vs semantic), reconciling the two documented paths.
- Aligned the dependency-graph path in `action-point-template.md` to `blueprint/action-points/README.md` (matched the file's own prefix convention).
- Spec Kit constitution handoff now provides a fallback `cp` command from `blueprint/plan/00-vision.md` for the case where `.claude/rules/blueprint-schema.md` is not used (the previous single command would fail).

## [1.0.0] - 2025-05-04

### Added
- Initial release of the Bleu Claude Code plugin.
- Eight-phase blueprint workflow (Phase 0 Intake → Phase 7 Sign-off & Handoff) plus Phase R (Resume / Persist).
- Session-persistence layer: `SESSION.md`, `NEXT.md`, `journal.md`, `index.md`, MADR-style `decisions/`.
- Action-point template with dependency graph and granularity guidance (3–5 APs for small tasks, ~38 for greenfield).
- Adversarial linting (proposer-validator separation).
- Continuous-research-with-citations pattern.
- Eight reference files lazily loaded by the skill.
- Handoff artifacts for GSD, Superpowers, raw Claude Code, and a flat AP list.
- Optional Claude Code integrations: hooks, KB Curator subagent, git auto-commits, MCP servers.
- Advanced architecture capabilities (reflection loop, schema-as-code, observability, agent team, knowledge graph, multimodal ingest, external integrations).

[Unreleased]: https://github.com/Nirvaan05/Bleu-plugin/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Nirvaan05/Bleu-plugin/releases/tag/v1.0.0

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

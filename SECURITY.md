# Security Policy

## Supported versions

Bleu follows the latest published version on the `main` branch. Only the most recent minor release receives fixes.

| Version | Supported |
|---|---|
| 1.0.x   | Yes |
| < 1.0   | No  |

## Reporting a vulnerability

If you discover a security issue in the Bleu Claude Code plugin - for example, a prompt-injection path through `blueprint/` files, a hook that escalates permissions, or any way the plugin can be coerced into writing outside its declared workspace - please **do not open a public issue**.

Instead, email the maintainer:

- **Nirvaan Lagishetty** - open a private security advisory via [GitHub Security Advisories](https://github.com/Nirvaan05/Bleu-plugin/security/advisories/new), or DM [@Nirvaan05](https://github.com/Nirvaan05).

Include:

1. A clear description of the issue and its impact.
2. Steps to reproduce, ideally with a minimal Claude Code session transcript.
3. The Bleu version (`plugins/bleu/.claude-plugin/plugin.json` → `version`).
4. The Claude Code version you observed it on.

You can expect an acknowledgement within 72 hours and a status update within 7 days. Fixes for confirmed issues will be released as a patch version with credit in the changelog (unless you ask to remain anonymous).

## Scope

In scope:

- The Bleu skill itself (`plugins/bleu/skills/bleu/`).
- The plugin manifest and marketplace manifest.
- Any hooks or integrations described in `references/claude-code-integration.md`.

Out of scope:

- Vulnerabilities in Claude Code itself - report those to Anthropic.
- Vulnerabilities in third-party executors (GSD, Superpowers) - report to those projects.
- Social-engineering scenarios that require the user to manually paste a malicious blueprint.

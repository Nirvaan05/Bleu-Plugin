# Privacy Policy

_Last updated: 2026-05-19._

The Bleu Claude Code plugin (the "plugin") is designed to run entirely inside your local Claude Code environment. This document explains what data the plugin handles.

## What the plugin does with your data

- **All blueprints, plans, research notes, and ADRs are written locally** to a `blueprint/` directory in your working directory. They never leave your machine via the plugin itself.
- **No telemetry.** The plugin does not phone home, ping a remote server, send analytics, or report usage of any kind.
- **No account, login, or registration** is required to use the plugin.
- **No cookies, tracking pixels, fingerprinting, or third-party scripts** are involved; the plugin has no web surface.

## What runs through Claude Code and Anthropic

Bleu runs inside Claude Code as a skill. When you use the plugin, your prompts and the resulting workspace contents pass through Claude Code and Anthropic's APIs the same way any other Claude Code session would. That traffic is governed by:

- [Anthropic's Privacy Policy](https://www.anthropic.com/legal/privacy)
- [Anthropic's Consumer Terms](https://www.anthropic.com/legal/consumer-terms) or commercial agreement, whichever applies to your account
- [Claude Code's documentation on data handling](https://docs.claude.com/en/docs/claude-code/security)

Bleu does not change, intercept, or duplicate that data flow.

## Third-party services invoked from the plugin

When you ask Bleu to do continuous research, it uses **your** Claude Code web tooling (WebFetch, WebSearch, MCP servers you have configured). Any requests to third-party sites are made by Claude Code on your behalf using your credentials and your network. Bleu does not introduce its own third-party services.

## Source code

The plugin is open source under the MIT License. You can audit every file in this repository to verify the claims above.

## Contact

For questions about this privacy policy, open a [GitHub Security Advisory](https://github.com/Nirvaan05/Bleu-plugin/security/advisories/new) or DM [@Nirvaan05](https://github.com/Nirvaan05).

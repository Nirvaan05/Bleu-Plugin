# Contributing to Bleu

Thanks for considering a contribution to the Bleu Claude Code plugin.

## Ways to help

- **Report bugs** - open an issue with a minimal repro: what you asked Bleu to do, what it produced, what you expected.
- **Suggest improvements** - open an issue tagged `enhancement` describing the workflow you want.
- **Improve docs** - typos, clarifications, missing examples, better mermaid diagrams. PRs welcome.
- **Add a reference file** - `plugins/bleu/skills/bleu/references/` holds the lazily-loaded reference material. New references should be self-contained and citation-rich.
- **Share blueprints** - if you've used Bleu on a real project and want to share the resulting `blueprint/` as a worked example, open a PR adding it under `examples/`.

## Pull request checklist

1. Version bumps go in **both** `.claude-plugin/marketplace.json` and `plugins/bleu/.claude-plugin/plugin.json` - they must agree.
2. If you change the skill behaviour, update `plugins/bleu/skills/bleu/SKILL.md` and any affected reference file.
3. Keep PRs scoped. One concern per PR.
4. Run `/plugin marketplace add .` locally and confirm `/plugin install bleu@bleu` still works end-to-end.
5. Update `CHANGELOG.md` under `## [Unreleased]`.

## Local development

```bash
git clone https://github.com/Nirvaan05/Bleu-plugin.git
cd Bleu-plugin
# Inside Claude Code:
/plugin marketplace add .
/plugin install bleu@bleu
```

Restart your Claude Code session after install.

## Code of conduct

This project follows the [Contributor Covenant](./CODE_OF_CONDUCT.md). By participating you agree to abide by it.

## License

Contributions are licensed under MIT, matching the project [LICENSE](./LICENSE).

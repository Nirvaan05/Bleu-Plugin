<!-- Thanks for contributing to Bleu. Keep PRs scoped to one concern. -->

## What does this PR do?

<!-- Brief description. Link any related issue with "Closes #N". -->

## Checklist

- [ ] Version bumps (if any) are in **both** `.claude-plugin/marketplace.json` and `plugins/bleu/.claude-plugin/plugin.json`, and they agree (CI enforces this).
- [ ] If skill behaviour changed, `plugins/bleu/skills/bleu/SKILL.md` and any affected reference file are updated.
- [ ] PR is scoped to a single concern.
- [ ] Verified locally: `/plugin marketplace add .` then `/plugin install bleu@bleu` still works end to end.
- [ ] `CHANGELOG.md` updated under `## [Unreleased]`.
- [ ] New prose uses hyphens, not em dashes (repo style).

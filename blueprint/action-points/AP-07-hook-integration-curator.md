# AP-07: Hook Integration (Curator)

## Title
Wire the Sanitizer and Graph Engine into the Curator loop.

## Depends on
AP-02, AP-05

## Files involved
- `.claude/settings.json`: Modify
- `.claude/hooks/on-file-changed.sh`: Create

## Code flow
1. Create a shell script that acts as the `FileChanged` handler.
2. If the changed file is in `raw/`, invoke `sanitizer.py`.
3. If the changed file is in `plan/`, invoke `graph_engine.py` to rebuild the index.
4. Update `.claude/settings.json` to register these hooks.

## Interfaces touched
- Claude Code Hook configuration.

## Verification
- Edit a component file.
- Verify that `graph.json` is automatically updated.

## Complexity
M - Infrastructure integration.

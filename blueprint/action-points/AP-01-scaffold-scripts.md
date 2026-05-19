# AP-01: Scaffold Deterministic Scripts

## Title
Create the infrastructure for non-LLM orchestration tools.

## Depends on
None

## Files involved
- `scripts/bleu/graph_engine.py`: Create
- `scripts/bleu/dag_validator.py`: Create
- `scripts/bleu/sanitizer.py`: Create
- `scripts/bleu/utils.py`: Create

## Code flow
1. Create a dedicated `scripts/bleu/` directory in the project root.
2. Initialize `utils.py` with common file I/O and JSON handling for `blueprint/` paths.
3. Stub the main entry points for the three core tools.
4. Ensure all scripts follow a standard CLI interface (input path, output path, verbose flag).

## Interfaces touched
- CLI entry points for orchestration tools.

## Verification
- Run `python scripts/bleu/graph_engine.py --help` and verify no errors.
- Run `python scripts/bleu/sanitizer.py --help` and verify no errors.

## Complexity
S - Boilerplate setup.

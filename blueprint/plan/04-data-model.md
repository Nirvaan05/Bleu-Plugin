# Data Model: Orchestration Metadata

## Orchestration Schema (`blueprint/.graph/graph.json`)
The primary data structure for blast-radius analysis.

```json
{
  "version": "1.0.0",
  "nodes": [
    {
      "id": "node_id",
      "type": "component | ap | adr | pipeline",
      "path": "plan/03-components/...",
      "metadata": {
        "status": "active | blocked | waiting",
        "hash": "content_hash"
      }
    }
  ],
  "edges": [
    {
      "from": "node_a",
      "to": "node_b",
      "type": "depends_on | implements | informs"
    }
  ]
}
```

## Reflection Counters (`blueprint/.reflection/counters.json`)
Tracks loop counts for the Circuit Breaker.

```json
{
  "proposals": {
    "proposal_id_hash": {
      "rejection_count": 0,
      "last_verdict": "REJECT",
      "timestamp": "ISO-8601"
    }
  }
}
```

## Sanitization Rules (`.claude/bleu/sanitizer-config.json`)
Deterministic regex patterns for input hardening.

```json
{
  "patterns": [
    {
      "id": "S-01",
      "name": "Shell Directive",
      "regex": "(rm -rf|curl.*\\|.*bash|sudo )",
      "action": "STRIP",
      "message": "Removed potential executable directive."
    },
    {
      "id": "S-02",
      "name": "Instruction Override",
      "regex": "(ignore previous instructions|new system role)",
      "action": "BLOCK_AND_TAG",
      "message": "Detected potential prompt injection."
    }
  ]
}
```

# USDJPY GA Factory

USDJPY GA Factory is the operator-facing P4-4 view for Strategy JSON GA productionization. It connects the existing USDJPY GA trace with Case Memory candidates and shows whether the next generation should use elite-guided mutation, crossover, or wider exploration.

## Operator View

The Evolution workspace shows:

- candidate count;
- elite archive count;
- strategy graveyard count;
- lineage node and edge counts;
- next generation production status;
- safety boundary.

The panel is read-only. It calls backend API routes and does not read local runtime files directly.

## What It Answers

```text
Which candidates became elite?
Which candidates are blocked and should not be retried unchanged?
Which blocker reasons dominate the graveyard?
Which lineage path produced the best seed?
Should the next generation use elite-guided mutation or expand search?
```

## Safety

This layer only organizes research evidence. The current product has no Live Lane:

```text
executionLaneExists=false
existingEaOwnsExecution=false
```

GA Factory output can support Shadow and tester work only. It cannot approve, indirectly prepare, or create broker execution.

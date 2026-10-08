# VIO OpenVINS task packet — 2026-10-07

Approved scope: the user's five-section OpenVINS public-baseline and IMU
preparation plan. No flight, ExternalNav, M3C port, mainline push/merge or Vault
write. Evidence is scoped to the dedicated Linux research worktree.

Use a lean packet because the pose contract and architecture were already
decided in the approved plan. No Vault templates or files accessed. Detailed
runtime/audit findings belong in the three VIO reports, not duplicated here.

## Decision and isolation

The host's existing ROS2 Jazzy remains untouched. The user chose Docker ROS1
Noetic for the upstream serial EuRoC entry point instead of introducing ROS2 bag
conversion into the first baseline. Worktree is a sibling directory to avoid
editing the main checkout's ignore file. Only the explicitly requested merge
was committed; subsequent implementation is reviewable working-tree state.

## References

- `task-brief.md`: objective and constraints.
- `evidence-map.md`: provenance and dependency gates.
- `validation-report.md`: commands and observed results.
- Root `HANDOFF.md`: actual work, blockers and resume boundary.

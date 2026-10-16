# RM27 SLAM research boundaries

- This is the independent MaixCAM2 monocular SLAM research repository, not the active PX4/VIO worktree.
- Read README.md, docs/STATUS.md and HANDOFF.md before continuing.
- Reuse the existing adapters, evaluator and benchmark. Keep historical imported files byte-identical;
  if a change is needed, first update its provenance/test scope intentionally, not its recorded history.
- Software/synthetic tests are not physical SLAM, timing, calibration, flight or hardware-health qualification.
- Preserve unknown clock semantics and arbitrary monocular scale. Do not fabricate metrics or loosen gates.
- Do not access devices, change firmware/drivers/parameters, run old capture scripts or publish raw/private data
  merely because a helper exists. Physical actions require current task authorization.
- Keep recordings, SDKs, build products and credentials outside Git. Never commit tokens/passwords/private keys.
- The raw-inclusive historical manifests/reports are not a promise that a fresh clone includes all experiments.
- HANDOFF.md is reviewable project transfer; VAULT_UPDATE.md is only a proposal. Do not access/write the Vault by default.
- Work in small attributable changes, test relevant code, preserve unrelated work, and push only when requested.

## Common engineering standard

Apply `.agents/docs/engineering.md` for the shared engineering process. This
file remains the SLAM-specific adapter: dataset, camera calibration, timestamp
and scale limits, provenance of imported files, and the offline-versus-device
qualification boundary stay local to this repository. Do not move SLAM rules
into the common file or treat software replay as hardware qualification.

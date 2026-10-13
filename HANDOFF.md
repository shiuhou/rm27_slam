# Engineering Handoff

## Repository state

- Project: RM27 independent MaixCAM2 monocular SLAM research starter.
- Repository: https://github.com/shiuhou/rm27_slam
- Branch: main.
- Commit: see this clone's `git rev-parse HEAD`; publication contains the imported source state below.
- Source commit: `rm27_slam-vio` `74d44b09c65e2a839b74d834756f0d178207d679`.
- Preparation workspace: `C:/Users/USER/OneDrive/RM27/rm27_slam_maixcam2`.
- Source workspace was dirty before preparation and remains preserved; this is a separate repository.

## Task objective

Provide visual-team colleagues a cloneable SLAM/board-testing starting point, reusing existing work.
Publish only curated source, small historical measurements, calibration reference and instructions.

## Actual changes

- Imported 77 original files with recorded byte hashes: old SLAM starter/plan, VSL reports,
  Stella/ORB adapters, online observation tools, evaluator, schema and focused software tests.
- Preserved the shared localization package without refactoring; optional VIO interfaces remain
  dependencies/research hooks, not a delivered ROS2 or board VIO system.
- Added historical MaixCAM2 C++/Python KLT source and saved 2026-10-07 measurement JSON/reports.
- Added the original OS04A10 geometry fit/protocol as a limited reference, not a default calibration.
- Added portable `prepare_gray.py`, synthetic tests and no-overwrite/INCOMPLETE handling.
- Added MaixCAM2 start guide, provenance/status/validation, Git ignores and exact-byte attributes.
- Did not remove original SLAM content from `rm27_slam-vio`, alter its remote, or stage its dirty files.
- Did not bundle camera recordings, upstream binaries/libraries, SDKs, credentials or flight helpers.

## Verification commands and observed results

From this new repository:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
py -3 -B -m pytest tests -q
py -3 -B tools/maixcam2/prepare_gray.py --help
py -3 -B -m rm27.perception.vision.localization.experiments.runner --help
```

176 passed / zero skips in the final local run; pytest exit 0. Both CLI help commands exit 0.
Import SHA256/size preservation is part of the suite. Details and publication checks:
[docs/VALIDATION.md](docs/VALIDATION.md).

## Failed attempts

Expected test-first result: before the new portable wrapper, 10 tests failed for absent module/CLI,
while 2 import preservation tests passed. This is development evidence, not a hardware failure.
One source search used a PowerShell glob in rg and was corrected to directory/file arguments;
no files were changed by that command. Empty remote clone warned that no commits existed, as expected.
Initial Git whitespace inspection used a default incompatible with byte-preserved CRLF;
cr-at-eol isolated two new-test EOF blank lines, removed without touching imported history.

## Decisions and rationale

Keep original package paths and source bytes to reuse known adapters/tests, avoiding a duplicate framework.
Keep camera driver/capture tooling as a pinned external project link rather than copying an entire unrelated
target-guidance project. Prioritize fixed-input board replay to separate image-path and estimator costs.
Keep raw video outside the public repository; transfer original evidence separately if requested.
Do not rewrite historical reports' dated status or imply all of their linked artifacts are published.

## Verified facts

Historical pinned Stella passed the host/public-data path; stock ORB crashed at shutdown and the recorded
patched version passed host execution. Original short board KLT measurements were about 29.33/10.09 FPS,
not complete SLAM. Current software preservation/test evidence is described above, not new hardware evidence.

## Assumptions and open questions

Colleague's exact board image, camera, focus, usable memory and SDK/ABI are not known.
Full aarch64 Stella/ORB dependencies/build and live input integration remain unqualified.
Original ORB shutdown patch/build-recipe files were not available in this local publication inventory;
the reports point to external historical artifacts. Retrieve them before claiming exact patched reproduction.
The actual source recordings/frames are not in a clone. Calibration provenance has remaining UNKNOWN fields.

## Risks

Historical helpers contain old absolute paths and are not recommended direct launchers.
Foreign intrinsics, rescaled/cropped pixels, unverified timestamps and arbitrary scale must not be mislabeled.
Do not execute old capture/driver programs or modify shared-board apps under publication authority.
Public software tests do not prove SLAM accuracy, hardware health, VIO or flight readiness.

## Next actions

Read [docs/MAIXCAM2_START.md](docs/MAIXCAM2_START.md). Collect the colleague's environment,
obtain original input or capture their own under a separate approved workflow, replay KLT, then qualify
one headless full SLAM backend on fixed data before connecting a live camera.
No PX4 connection is needed for the pure monocular experiment.

## Rollback point

Original `rm27_slam-vio` and its dirty work remain untouched.
This is additive publication into an initially empty repository; use a normal future revert for changes,
not destructive cleanup or force-push. Local artifacts are not discarded or moved out of the source workspace.

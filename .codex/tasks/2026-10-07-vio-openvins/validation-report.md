# Validation report

## 2026-10-08 native repeatability experiment

Completed `repeat_native.py --freeze --count 10` and separate
`repeat_native.py --variant cvserial --start 1 --count 3` under the external
experiment root `/home/shiuhou/Projects/rm27-vio-20261007`. All 13 summaries
exist; all 39 native/player/recorder exits are zero. Final `repeat_native.verify()`
returned zero. `analyze_repeats.py` completed and saved `analysis-13.json` with
13 run records and 48 within-group pairs. Baseline ATE range 5.432--7.653 cm,
15/45 pair differences >1 cm; control range 5.551--6.604 cm, 1/3 >1 cm.
All runs 2800 raw/2780 evaluated poses. No scale correction, no gate/code/data
change. See `NATIVE_REPEATABILITY.md` for complete tables and causal limits.
Experiment execution verified; determinism NOT achieved; root cause unresolved;
VIO-P remains PARTIAL. Regression numbers below are prior-task evidence, not
fresh tests from this documentation/experiment-only continuation.

## Latest runtime adapter validation

Full adapter03 playback clean: native/player/recorder/observer exit0; all 2912
images and 29120 raw IMU SI values/timestamps/order equal ASL. 2800 visual poses
and 27980 propagated states exact against independent MCAP. Full coverage and
same-run native/adapter fixed-SE3 metrics PASS. Historical ATE consistency FAIL:
0.0127292168 m difference >0.01 m tolerance. Overall VIO-P remains PARTIAL.
Run03 metrics, raw evidence and failures retained; no thresholds loosened.
Additional native-only control03: 2800 poses, clean exits, ATE0.0624031978 m;
1s RPE0.0449588172 m /0.477944980 deg. This confirms some native execution
variation, not its cause or an exemption from historical-baseline acceptance.

226 regression pass/1 skip; sourced ROS2 7/7. Logs: external evidence root
`adapter-final-regression.log`, `adapter-final-ros2.log`; expected test-first
failures in `adapter-runtime-red.log` and later validation/review red logs.
Independent postfailure check: 17 immutable artifact hashes PASS, all exits0.
See `OPENVINS_ADAPTER.md` for exact commands, source conventions and limitations.

## Latest native SE3 and initial adapter projection

`NATIVE_SE3_EVALUATION.md` records policies, exact commands and evidence paths.
11 evaluator tests and 7 projection tests were observed failing before code.
Clean run02 evaluation: 2780 GT-overlap poses, ATE 0.0701139912 m, 1s RPE
0.0452377799 m / 0.477985477 deg; fixed scale 1. Independent SciPy cross-check
PASS. Initial real-data adapter projection: 2800 messages exactly preserved;
no runtime adapter replay claim. All records remain incomplete on missing state.
Fresh regression 208 passed/1 skip in unsourced venv; separate sourced system
Python ROS2 suite 7/7. Combined ROS/venv attempt failed on imports; no code/test
weakening used to resolve it. First real evaluation rejected GT norms; explicit
reference-only normalization and its measured 20.526ppm bound are documented.
No hardware, Sim3, new dataset, commit or push. Broader VIO-P remains PARTIAL.

## Latest native ROS2 lifecycle validation

See `rm27/perception/vision/docs/ROS2_LIFECYCLE_FIX.md` for the scoped PASS,
exact source patch and gdb evidence. The earlier tests below are historical.
Current external evidence root is `/home/shiuhou/Projects/rm27-vio-20261007`.

- Gdb before: thread 1 aborts in global visualizer/publisher destruction after
  DDS factory static destruction. Gdb after: reversed, correct order, exit 0.
- Real no-data regression: before 2/2 failures, after 10/10 exit 0, with image
  publisher thread on/off. `lifecycle-debug/before|after/summary.json`.
- Full sequence `native-ros2-run02-lifecycle`: 2,912 update logs, 2,800 online
  states and 2,800 recorded visual poses, all three process exit codes 0.
- Current whole repository suite: 190 pass, 1 ROS-only skip. ROS2-specific
  suite separately: 7/7 pass including that skipped case.
- All three algorithm-library hashes unchanged; entry executable only changed.
- No ASan/UBSan run; direct destructor-order evidence and native counterfactual
  tests were sufficient for this bounded fix. No estimator math modified.

No adapter, SE3 accuracy evaluation, physical IMU qualification, port or push.

Worktree: `/home/shiuhou/Projects/rm27_slam_vio_openvins`.
Command (from worktree):

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/shiuhou/venvs/mujoco/bin/python -m pytest tests -q
```

- Merge baseline: 163 passed, `baseline-tests.log`.
- Initial sequence/noise tests before implementation: 18 failed due to missing
  functions, `imu-tests-red.log`.
- Initial implementation: 18 passed, `imu-tests-green.log`.
- Receipt-clock regression before correction: 1 failed / 20 passed,
  `imu-tests-red2.log` (expected failure: receipt time incorrectly accepted).
- After acquisition-time prerequisite and CLI/jitter tests: 184 passed,
  `tests-after-imu.log`.

Logs are under `/home/shiuhou/rm27-vio-20261007`. Tests are synthetic fixtures,
not physical IMU measurements or a real VIO backend run. No ATE/RPE, runtime
resource result, or hardware-rate claim can be derived from these tests.

`git diff --check` initially exposed Windows CRLF in the transferred modified
file; LF formatting was restored and the check rerun without errors. Main
checkouts and old gate status files remain untouched.

## 2026-10-08 PX4 export/timestamp/transport read-only addendum

Executed on Windows, both commands exit0, shell ownership released and port closed:

```text
py -3 .maixpy/s0-audit-20261008/px4_console_readonly.py "logger status" "param show SDLOG_PROFILE" "param show SDLOG_MODE" "param show SDLOG_BOOT_BAT" "ls /fs/microsd/etc/logging" "cat /fs/microsd/etc/logging/logger_topics.txt"
py -3 .maixpy/s0-audit-20261008/px4_console_readonly.py "ls /fs" "ls /fs/microsd"
```

Logger mode all,142 subscriptions, Not logging; profile1/mode0/boot_bat0.
Custom logging path absent (Not a directory), but microSD itself readable.
Known shell sysinit warning preserved. No settings/wiring changes or capture.
Upstream read-only gh API inspection at runtime-reported4817c061 confirms
logger interval_ms/default instance, raw FIFO scaling/order, integrated
HIGHRES/SCALED data, TIMESYNC and ULog download/streaming source capabilities.
No deployed streaming throughput, ADC timing, camera exposure or synchronized
dataset qualification claimed. No regression rerun: docs/diagnostic allowlist
only, no adapter/estimator/schema change. VIO-P remains PARTIAL.

## 2026-10-08 authorized disarmed offline ULog experiment

User explicitly approved logging-only config/capture/restoration and confirmed
props removed. Evidence under
/home/shiuhou/Projects/rm27-vio-20261007/imu-offline-20261008, with Windows source
.maixpy/imu-offline-20261008. See PX4_IMU_OFFLINE_VALIDATION.md for full report.

Commands (Windows, cwd rm27_slam):
- `py -3 .maixpy/imu-offline-20261008/bench_io.py capture` exit0. Configuration
  prepared by exact-path FTP mkdir/put and byte-identical readback first. Only
  logger on/off/stop/start and temporary topic-file operations; no param changes.
- Two `bench_io.py get /fs/microsd/log/sess100/log100.ulg <distinct-local-file>`
  operations succeeded; each6896444bytes, equal SHA256
  d94a142c5a474e7a755bffd534a41cf3255081d87d4868dabf63493a5146f46d.
- `.maixpy/imu-offline-20261008/venv/Scripts/python.exe .maixpy/imu-offline-20261008/analyze_ulog.py .maixpy/imu-offline-20261008/bmi270-disarmed-01.ulg`
  exit0; pyulog1.2.4, file_corruption false,391dropouts; correct FIFO instance1/
  device3604506; gyro12648/accel11933samples. No complete-data PASS.
- `py -3 .maixpy/imu-offline-20261008/test_capture_guard.py`:5pass after observed
  missing-function/interface failures. Analysis test script:3pass after missing
  implementation failures; synthetic tests only, not new physical qualification.
- Fresh post-restoration shell readback: original `logger start -b 64 -t`, idle,
  all seven SDLOG values unchanged, custom path absent, commander Disarmed.
  Subscription count147 versus preflight142 explicitly recorded, not equated
  with identical runtime state. Log-start perf_reset_all is source-supported.

Failure evidence retained: helper missing FTP master source attrs, Unix default
tempfile path on Windows, generic remote-CRC failure. No capture before successful
config readback. Two independent file downloads used instead of a remote-CRC
claim. No algorithm/main regression suite rerun because only research helpers,
docs and status changed. VIO-P PARTIAL unchanged; VIO-S0 PARTIAL for lossy capture
and unresolved sensor/camera timing. No push/commit/Vault write.

# RM27 SLAM research

Standalone camera calibration and visual localization workspace for RM27.
The Python import path stays `rm27.perception.vision.localization` so results
can be integrated with the main `rm27_drones` repository later.

This repository was extracted from `shiuhou/rm27_drones`, branch
`research/slam-integration`, commit
`96b72c28036aa9ea395f1b45cb7a58e450995abf`. It contains localization
code, the M3C/OS04A10 experiment starter, VSL reports and focused tests.
It does not contain the flight stack, device-side target-recognition submodule,
raw camera recordings, public datasets, third-party SLAM binaries or generated
artifacts.

## Continue RM27 VIO / PX4–M3C work

Read [HANDOFF.md](HANDOFF.md), then
[PX4–M3C wiring and verified link state](rm27/perception/vision/docs/PX4_M3C_CONNECTION.md)
and [Codex resume guide](rm27/perception/vision/docs/CODEX_RESUME.md).
The plan is [new_plan.md](new_plan.md); selected bench/offline code and reports
are indexed in [.maixpy/README.md](.maixpy/README.md).
Stage A/B is preserved PASS; real high-rate IMU input remains PARTIAL and full
Stage C has not started. Raw captures/datasets and credentials are not published.

## Start on the camera computer

Use Python 3 with NumPy, OpenCV and pytest. From the repository root:

```bash
python -m pip install -r requirements.txt
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests -q
```

The calibration and dataset procedures are in
`rm27/perception/vision/docs/VSL-2_CALIBRATION_PROCEDURE.md` and
`rm27/perception/vision/docs/VSL-3_EXPERIMENT_HARNESS.md`. The physical
camera/board geometry and timing must be recorded and validated before a
trajectory is treated as metric or sent to a controller.

The current physical calibration target is `RM27-DOT-7X7-30MM-01`: a
symmetric 7 × 7 circular grid with nominal 30 mm center spacing. Its target
definition is in `rm27/perception/vision/localization/target_definition.template.json`.
Measure the printed center spacing and record the result in the capture session;
the nominal spacing is not a substitute for measurement.

Current status: public-dataset backend qualification is partial; RM27 camera
calibration capture and real VSL-3 evaluation have not passed. See
`rm27/perception/vision/docs/VSL-2_GATE_STATUS.json` and
`rm27/perception/vision/docs/VSL-3P_STATUS.json`.

When integrating changes back into `rm27_drones`, compare against the source
commit above and copy or merge the reviewed `rm27/perception/vision/` files and
matching tests. This repository is independent; a push here does not update the
main repository automatically.

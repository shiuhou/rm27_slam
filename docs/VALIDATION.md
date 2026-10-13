# Publication validation — 2026-10-13

## Artifact and scope

New repository: `https://github.com/shiuhou/rm27_slam`, branch `main`.
Source: `rm27_slam-vio` HEAD `74d44b09c65e2a839b74d834756f0d178207d679`
plus explicitly listed local historical artifacts in [import-manifest.json](import-manifest.json).
77 imported files were compared by byte size and SHA256 before testing.
The original source working tree's dirty reports, tasks and unrelated files were preserved.

Observed environment: Windows Python 3.12, OpenCV 4.13.0, NumPy 2.5.3, pytest 9.1.1.
No dependency install, SSH, physical capture, new board build or hardware operation occurred.

## Test-first portable wrapper

Before `tools/maixcam2/prepare_gray.py` existed:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
py -3 -B -m pytest tests/test_prepare_gray.py tests/test_publication.py -q
```

Observed exit 1: 10 expected failures (missing new module/CLI), 2 preservation tests passed.
The implementation reuses the historical resize/BGR2GRAY algorithm, adds explicit CLI paths,
no-overwrite behavior, bounded prefix size, hash metadata and retained INCOMPLETE prefixes.

Fresh complete suite after implementation and start-guide edits:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
py -3 -B -m pytest tests -q
py -3 -B tools/maixcam2/prepare_gray.py --help
py -3 -B -m rm27.perception.vision.localization.experiments.runner --help
```

Observed: **175 passed / zero skips**, pytest exit 0 (22.11 s on the later run).
Both help commands exited 0. Tests include imported adapters, schema/calibration gates,
canonical data, online observations, evaluation, synthetic videos and import byte preservation.
The new media fixtures are synthetic and are never labeled real camera evidence.
After adding an entry-document link check and resolving whitespace inspection, the complete suite
was rerun: **176 passed / zero skips**, exit 0 (42.51 s). This adds one publication check, not a hardware gate.

## Publication checks

- Import parity test verifies all 77 sizes/SHA256 values from within the new repository.
- Example calibration SHA256 matches its retained original:
  `1ef473ffb4dbf024ff682b41907e6f499397199168fa49dc82fd9890365191f8`.
- Scope check rejects raw `.ulg/.h264/.px4`, controller helpers and credential paths in imports.
- Pattern scan for GitHub tokens, private-key headers and API-key forms had no matches
  (rg exit 1). This is a scoped automated check, not an exhaustive security certification.
- GitHub API confirmed target `shiuhou/rm27_slam` is public and the active account is `shiuhou`.
- Repository-local author/committer: `shiuhou <uhshi371@connect.hkust-gz.edu.cn>`;
  global identity and shared history are not changed.
- Remote was empty at initial clone and rechecked before preparing publication.
- Final staging review, clean-clone test and remote-tip equality are required before reporting publication complete.
- Initial plain Git whitespace check treated the byte-preserved CRLF as trailing whitespace.
  Repeating with cr-at-eol isolated two extra EOF blank lines in NEW test files; those were removed.
  The archived source/report bytes were not normalized. The attribute makes this check explicit.

## Not verified here

C++ rebuild, complete Stella/ORB on aarch64, board runtime/temperature/memory, live camera,
exposure timestamps, real-data accuracy, Camera–IMU synchronization and flight readiness.
Historical board measurements retain their original limited scope; software PASS is not SLAM PASS.

# Evidence map

- Source baseline: Linux `acc70e34ed08f5bbc315391f5c5f2d08d7628a48` and Windows
  `b8e7299cf090f5150f9f262ebd3b232a824cc526`, shared ancestor `bd25acf`.
- Authorized merge: `13c7a77bbe0fd256e6765efd4459fbca3426e0b7`.
- External evidence: `/home/shiuhou/rm27-vio-20261007/` (logs, input snapshots,
  official source archive and extracted source; not vendored into Git).
- Input snapshot hashes: `inputs/SHA256SUMS.txt`. Original local uncommitted files
  were not added to the research branch. Only selected reports/instructions copied.
- Official source research used the pinned OpenVINS archive to establish the
  native entry point, GT initialization hazard, timestamp distinctions and JPL
  convention. Source inspection is not runtime validation.
- IMU candidate hardware source, hashes and observation limits are in
  `rm27/perception/vision/docs/IMU_SOURCE_AUDIT.md`.
- No evidence currently establishes real IMU acquisition timing, camera–IMU
  calibration, OpenVINS native/adapter parity, or M3C VIO throughput.

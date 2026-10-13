# Board C++ sparse tracking benchmark, 2026-10-07

Built with installed g++ 11.4.0, `-O3 -DNDEBUG -std=c++17`, installed OpenCV
C++ 4.11.0 headers/libs, no dependency installation. Source retained locally
in `.maixpy/frontend_bench.cpp` and device `/root/slam-bench-20261007`.

First 360 frames of environment video (about 2 source seconds), persistent
bidirectional LK, 15x15 windows, pyramid level 2, FB distance <0.75px, LK
error <30, conditional corner replenishment. Measures tracking only, without
point undistortion, keyframe selection, geometric outlier rejection or mapping.
This is simpler than the prior Python benchmark and not a complete frontend.

| Input/config | Process median/P95 ms | Raw-file throughput fps | Median tracks |
|---|---:|---:|---:|
| 336x190, 180-point cap, 1 thread | 33.750 / 35.878 | 29.334 | 177 |
| 336x190, 180-point cap, 2 threads | 36.380 / 38.315 | 27.327 | 177 |
| 672x380, 400-point cap, 2 threads | 98.357 / 105.420 | 10.086 | 385 |

336x190 raw input median local retention 100%, minimum 98.25%; this is only
local photometric/forward-backward tracking, not geometric accuracy. Timing
includes file reads but excludes decode and grayscale conversion. Input gray
files made using Python OpenCV 4.12.0 INTER_AREA resize and BGR-to-gray.
Preparing both resolutions from 360 source frames took 12.579 s.

Separate software FFmpeg pipe at 336x190 achieved only 3.766fps end-to-end,
with median input-wait 225.239ms and median tracking 39.306ms. FFmpeg filter
uses different resize defaults from the raw-input preparation. Pipeline
contention/decoder overhead not isolated further. Do not treat pipe vs raw
tracking retention as an equal-input algorithm comparison.

Python and C++ use different installed OpenCV builds (4.12 vs 4.11), and these
are bounded short samples. No claim that C++ inherently outperforms Python or
that this is an optimized hardware limit. No live VIN grayscale pipeline,
NPU/IVE acceleration, map or SLAM backend benchmark was performed.

Conclusion: none of these measured implementations reaches 180fps processing.
180fps acquisition remains independently verified. Small-image sparse tracking
around 29fps leaves no demonstrated CPU margin for full mapping/loop closure.
Next work needs profiling/optimized image path or a reduced tracking rate and
strict map limits; alternatively offload the backend to a stronger computer.
Full-board SLAM remains unqualified.

Artifacts: cpp336.json (FFmpeg pipe), cpp336_raw.json, cpp672_raw.json,
cpp336_thread1.json. No system dependencies installed; staged helpers, binary
and raw gray samples remain under `/root/slam-bench-20261007`.

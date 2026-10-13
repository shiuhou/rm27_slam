# Board resource and frontend benchmark, 2026-10-07

Live root@10.18.198.1, hostname maixcam2-9d05, aarch64 Ubuntu 22.04,
kernel 4.19.125. Two Cortex-A53 cores, maximum 1.2GHz. Linux-visible memory
446MiB, about 334MiB available before/after benchmark; swap absent. /root has
about 38GiB free. g++ and OpenCV C++ headers/shared libraries present;
Python OpenCV 4.12.0, NumPy 2.2.6, two OpenCV threads. CMake, Eigen, g2o and
DBoW2 were not found in the checked standard paths. No dependencies installed.

Ran the same persistent sparse-LK Python frontend on the first 360 native
180fps frames (about 2 seconds of source), tracking at 672x380. Command:
`cd /root/slam-bench-20261007 && python3 -u benchmark_frontend.py /root/os04a10-tests/os04a10-20261007-005702-52804b 360`

Result: 31.973 seconds wall time, 11.260 processed fps including decode;
processing mean throughput 14.016 fps; median 68.362ms, P95 82.018ms;
decode median 16.882ms. Median 385 active tracks, local retention 99.746%,
20 candidate keyframes. No live camera/preview concurrency tested. This
bounded sample is not a full-video or complete SLAM benchmark.

The copied report.json contains a stale hardcoded 'Windows-host' limitations
string from the portable script; its platform field correctly reports Linux
aarch64. Script was corrected locally after this run; timing/data unchanged.

Conclusion: the measured Python frontend does not achieve 180fps on the board,
even without mapping/loop closure. This does not establish a performance limit
for optimized C++/hardware-assisted code. Full SLAM backend feasibility remains
unverified, and memory/map limits and required dependencies must be addressed.
No backend was built/started, no trajectory or map generated, no NPU acceleration
assumed. Source recordings and calibration remain intact.

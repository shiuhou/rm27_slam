# OS04A10 historical geometry reference

`os04a10-20261007/calibration_result.json` 和 `fit_protocol.json` 是本组当时的原文件，
不是给另一块板的默认参数。结果 SHA256：
`1ef473ffb4dbf024ff682b41907e6f499397199168fa49dc82fd9890365191f8`。

对应固定 focus OS04A10 full180 / 1344×760，OpenCV Brown-Conrady 五系数顺序
`[k1,k2,p1,p2,k3]`，27 fit / 7 validation 视图。
同会话 held-out validation RMS 约 0.150498 px，P95 0.265305 px；不等于独立会话验证。

镜头精确身份、部分采集来源字段及 sensor crop 信息仍有 UNKNOWN，
**不能把 GEOMETRIC_CHECKS_PASS 改成满足严格 harness 的 VALIDATED**。
原图、逐批采集 manifest、完整验证图不包含在本 clone 中。
改镜头、focus、裁剪/缩放或相机模式后应重新核验/标定，不直接复制 fx/fy 或畸变。

本结果不含 Camera–IMU 外参/时差或 IMU 噪声参数，不是同步 VIO 标定。

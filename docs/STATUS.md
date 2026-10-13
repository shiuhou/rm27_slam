# SLAM baseline and status — 2026-10-13 publication

## 历史 VERIFIED

- 主机公开数据 Stella：原固定版本的 native / RM27 adapter / normalization / evaluation 完成。
- 主机 ORB-SLAM3：stock 原版在退出时 SIGSEGV；记录的生命周期修补后执行完成。
  不是 SLAM 估计器算法失败，也不是未修改原版资格通过。
- 本组 MaixCAM2/M3C 的短时 C++ 稀疏 KLT：336×190/180点/1线程约 29.33 FPS，
  672×380/400点/2线程约 10.09 FPS。不是完整前端、建图或实时 SLAM。
- 本组 OS04A10 固定光学配置：同会话 27 fit / 7 validation 几何检查通过；
  结果及限制在 [标定参考说明](../examples/calibration/README.md)。

## PARTIAL / UNKNOWN

- 公共后端总体 VSL-3P 仍 PARTIAL；不等于真实 RM27 相机轨迹资格通过。
- MaixCAM2 上完整 Stella/ORB 的构建、回放、实时性能和持续运行：UNKNOWN / NOT_QUALIFIED。
- 另一块板/另一镜头的标定、实际可用内存与性能：UNKNOWN。
- 对应录影的可靠曝光时间、跨传感器时钟映射、米制尺度、硬件安全：未由本仓库证明。
- 没有以“相机 180 FPS”推导“SLAM 180 FPS”，也没有假设 NPU 会自动加速几何 SLAM。

## 本次发布实际验证

见 [VALIDATION](VALIDATION.md)。新软件测试只验证便携工具、输入契约、源文件保存及现有 adapter。
历史性能数字仍是原测试结果，没有新设备运行，没有更改接受门槛。

旧 `rm27/perception/vision/docs/` 报告按原字节保留，其 NOT_STARTED/next 段落描述当时状态。
部分引用指向仓库外原始制品；请以本索引理解发布范围，不把缺失数据的 clone 称为完整实验重放。

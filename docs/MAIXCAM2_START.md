# 视觉组 MaixCAM2 SLAM 最小起步路线

目标：先回答完整单目 SLAM 在同学自己的板上能否构建、稳定运行，以及资源是否可接受。
本路线是计划，不是已完成的板端 SLAM 资格验证。

## 已有东西先复用

- 板端 KLT 及灰度工具：[操作说明](../tools/maixcam2/README.md)。
- 相机采集/录影/回放：外部项目
  [maixcam2_dart_vision](https://github.com/blademaster679/maixcam2_dart_vision)，
  本地来源检查时 commit `6d2f6251dd839c8673cfcf8a977e22a09433afcf`。
  关注 `tools/os04a10_highfps/`、`tools/offline_recorder/`、`tools/video_replay/`。
  这是相机和视觉工具工程，不是 SLAM；其 SDK/驱动/采集步骤需单独审查，不能直接执行旧上板脚本。
- 既有离线 SLAM：[公共后端结果](../rm27/perception/vision/docs/VSL-3P_PUBLIC_BACKEND_QUALIFICATION.md)、
  [离线 harness](../rm27/perception/vision/docs/VSL-3_EXPERIMENT_HARNESS.md)。

## A. 先核对自己的板和镜头

记录架构、Linux/镜像、可用内存、CPU 核数/频率、OpenCV、编译器和温度传感器。
历史本组样机是 aarch64、两 Cortex-A53、Linux 可见约 446 MiB；不要把它当成所有 MaixCAM2 的固定可用内存。
分辨率、sensor、镜头、焦距、曝光、裁剪/缩放必须单独记录。
我们的 OS04A10 标定不能套用到另一 OS04D10/镜头或不同 focus。

## B. 固定录像板端回放，先分离相机链路与计算链路

用同一份视频准备 360 帧灰度前缀，复现 KLT 工作量，量 FPS、时间分位数和资源。
这不是完整 SLAM，只建立前端基线。记录失败、短输入和依赖缺失，不修改门槛来获得 PASS。
先不要加入实时相机、显示、H.264 再编码或 PX4；避免同时引入多个未知瓶颈。

## C. 构建一个完整后端，优先 Stella

先在外部独立目录克隆固定历史版本（不要把依赖下载到本仓库已跟踪目录）：

```bash
git clone --recursive https://github.com/stella-cv/stella_vslam.git /absolute/external/stella_vslam
git -C /absolute/external/stella_vslam checkout --detach e445b5452535e781fdf6777ec33a06f5f8f5e416
git -C /absolute/external/stella_vslam submodule update --init --recursive
git clone --recursive https://github.com/stella-cv/stella_vslam_examples.git /absolute/external/stella_examples
git -C /absolute/external/stella_examples checkout --detach defc69eecc36e51cdda22885bb86954f08ad6887
git -C /absolute/external/stella_examples submodule update --init --recursive
```

版本来源和依赖 pin 见 [PROVENANCE](PROVENANCE.md)。
依赖安装/构建按所选版本的官方说明及板端实际 ABI 准备；本仓库不含可直接运行的 aarch64 Stella。
既有 runner 使用外部 `run_tum_rgbd_slam` 的 monocular 模式、无 viewer、无 sleep、auto-term；
输入需要关联正确标定、时间证据和哈希，不是把任意 H.264 路径直接交给 runner。

```bash
python3 -m rm27.perception.vision.localization.experiments.runner --help
python3 -m rm27.perception.vision.localization.experiments.public_tum --help
```

先重现公开数据端到端路径，再使用自己的相机数据。
只有原始输入和实测配置一致时才比较轨迹；纯单目尺度默认 ARBITRARY。
没有独立 Ground Truth 就不编造 ATE/RPE。
保存 backend pin、词袋/库/二进制 SHA256、命令、退出码、RSS、处理时间和完整轨迹。
模型和算法阈值不在此发布任务中改变。

ORB-SLAM3 是第二条对照，其历史 stock 版本在退出时 SIGSEGV，修补后通过主机执行。
**原 shutdown patch/完整构建配方不在本地发布材料中**，必须找回原制品或重新做可追溯的诊断；
不能把我们报告中的 patched PASS 当作官方原版或板端 PASS。

## D. 最后才接实时相机

先确定采集线程/队列/丢帧策略与灰度图接口，再接已能运行的后端。
优先研究 VIN/ISP 图像入口，避免未经测量地把 H.264 软解路径当实时方案。
保留 frame sequence 和原始 PTS；PTS/收到图像的主机时间不自动等于曝光时间。
相机采集频率、SLAM 处理频率、输出频率是三个不同指标。

本路线不连接飞控、不发送 odometry/setpoint、不启用 EKF、不开展飞行。
它可以与 rm27_slam-vio 的 IMU/同步研究并行；单目回放成功不代替 Camera–IMU 标定或真实 VIO。

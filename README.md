# RM27 SLAM · MaixCAM2 research starter

这是视觉组独立研究 **MaixCAM2 上的单目 SLAM** 的起步仓库。
复用既有 RM27 相机标定、Stella / ORB-SLAM3 adapter、轨迹评估与板端稀疏跟踪测试。
它不是已经移植、验收完成的 SLAM APP；不包含飞控控制程序。

```bash
git clone https://github.com/shiuhou/rm27_slam.git
cd rm27_slam
```

## 从哪里开始

1. [MaixCAM2 起步步骤](docs/MAIXCAM2_START.md)：先固定录像回放，再尝试完整后端，最后接实时相机。
2. [板端前端测速工具](tools/maixcam2/README.md)：原样保留的 C++ KLT 和新便携灰度准备工具。
3. [历史结果与边界](docs/STATUS.md)：明确区分成功、失败、未验证，避免重复之前的误判。
4. [交接](HANDOFF.md)、[导入来源](docs/PROVENANCE.md)、[新仓库验证](docs/VALIDATION.md)。

## 这次带来了什么

| 内容 | 位置 | 资格范围 |
|---|---|---|
| Python/C++ KLT 原始工具及历史数据 | `tools/maixcam2/`、`reports/2026-10-07-*/` | 稀疏跟踪，不是位姿估计/建图 |
| 便携视频 → 两种灰度原始帧 | `tools/maixcam2/prepare_gray.py` | 本地解码顺序，无曝光时间/同步证据 |
| Stella / ORB adapter、数据契约、轨迹评估 | `rm27/perception/vision/localization/` | 复用离线研究框架，需要外部后端和合格输入 |
| 原 SLAM 路线与历史报告 | `rm27/perception/vision/` | 历史快照，不是当前整机 PASS |
| 本机 OS04A10 几何标定结果 | `examples/calibration/` | 原光学配置参考，不适用于另一镜头/焦距/裁剪 |
| 克隆后可运行的软件回归 | `tests/` | 软件与合成夹具，不证明板端 SLAM 性能 |

原有共用 localization 包按字节保留，包含少量 OpenVINS 接口文件以维持完整依赖边界。
本仓库的研究入口是单目 Stella / ORB，不发布 VIO 主线的 ROS2 构建、PX4/UART 控制器或 IMU 实验。
当前 VIO 主线位于独立的 [rm27_vio](https://github.com/shiuhou/rm27_vio)，两仓库 push 不会互相同步。历史导入材料中的 `rm27_slam-vio` 名称仅作为来源保留。

## 如何理解进度

本仓库的当前边界以 [STATUS](docs/STATUS.md) 和 [HANDOFF](HANDOFF.md) 为准。
板端 KLT 的帧率是前端稀疏跟踪测量，不是完整 SLAM 后端帧率；主机数据集或合成
测试成功不证明板端实时定位、米制尺度、相机曝光时序或飞行可用性。
历史实验的原始录像与第三方后端不随 clone 分发，缺少输入时不能声称已复现。

## 主机软件测试

在独立 Python 环境安装已有研究依赖，不要覆盖板端 MaixPy/系统 OpenCV：

```bash
python3 -m venv .venv
# Linux: source .venv/bin/activate
# Windows PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m pytest tests -q
```

这些依赖不会安装完整 Stella/ORB 或 C++ OpenCV 开发库。
新仓库在 Windows Python 3.12 上的软件测试结果见 [VALIDATION](docs/VALIDATION.md)。
板端运行需要先核对其实际架构、镜像和依赖；本次没有访问或修改任何设备。

## 不包含什么

原始录像/图片、公开数据集、词袋、第三方源码树/二进制、SDK、虚拟环境、设备凭证、
PX4 固件/参数和完整原始实验日志均未发布。部分历史报告链接到这些外部材料，克隆不含它们。
录影可另行提供；只有拿到对应原始输入，才能重放历史实测，而不是用夹具代替它。

纯单目研究无需连接 PX4，但尺度不能自动称为米制。这里不启用 EKF、不发控制指令、
不改驱动/固件，也不把目标识别或 KLT 跟踪当作完整 SLAM。

外部算法与 SDK 的来源、许可证和固定版本见 [PROVENANCE](docs/PROVENANCE.md)。

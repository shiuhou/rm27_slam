# MaixCAM2 offline sparse tracking tools

`frontend_bench.cpp` 是 2026-10-07 已实际在本组 MaixCAM2/M3C 上构建并运行的原文件，
字节/来源由 `docs/import-manifest.json` 固定。这是双向 KLT 跟踪和角点补充，
没有 SLAM 位姿、三角化、建图、回环、IMU 或控制输出。

## 1. 准备相同格式的输入

用现有 Python OpenCV，提供自己的视频和新的输出目录：

```bash
python3 tools/maixcam2/prepare_gray.py \
  --input /absolute/path/environment.h264 \
  --output artifacts/gray-new-01 --frames 360
```

输出 `gray336.raw`（336×190）、`gray672.raw`（672×380）、`preparation.json`。
像素算法与历史脚本相同：INTER_AREA resize，再 BGR2GRAY，uint8 连续行。
它只证明请求前缀成功解码，不证明整片完好、没有录制丢帧或有可靠曝光时间戳。
视频少于请求帧数会失败，保留 `INCOMPLETE` 和原始已解码前缀；禁止补帧或强行通过。
拒绝覆盖已有目录，帧数限 1..3600；这只是准备工具的操作上限，不是 SLAM 验收阈值。
新 wrapper 的合成视频测试不代表实际板端吞吐。

## 2. 在板端构建原来的 C++ 测速器

只在已具备 g++、pkg-config 和匹配的 OpenCV C++ 开发库时执行：

```bash
g++ --version
pkg-config --modversion opencv4
mkdir -p build
g++ -O3 -DNDEBUG -std=c++17 tools/maixcam2/frontend_bench.cpp \
  $(pkg-config --cflags --libs opencv4) -o build/frontend_bench
ldd build/frontend_bench
```

`pip install opencv-python` 不是安装 C++ 开发库的替代方法。
若缺失依赖，应先整理构建方案；不要为了这项实验替换系统相机库或刷镜像。
另一条路线是在匹配 SDK 的 Linux 主机交叉编译；x86 主机二进制不能复制成 aarch64 可执行文件。
本次发布没有重新构建或运行板端二进制，历史构建的记录在 `reports/2026-10-07-cpp/RESULT.md`。

## 3. 固定工作量回放

将灰度文件复制到板端自己的独立实验目录，再运行：

```bash
./build/frontend_bench artifacts/gray-new-01/gray336.raw 336 360 180 1
./build/frontend_bench artifacts/gray-new-01/gray672.raw 672 360 400 2
```

参数是 `raw_file width frames max_points threads`；只有 width=336/672 两档。
输出 JSON 含实际处理帧数、wall time、处理时间 median/P95、跟踪点数、局部保留率。
退出码 0 表示读到了请求帧数，不是 SLAM 通过；短输入返回 4，参数不合法返回 2。
原测速器不是高防御性的通用媒体 parser，使用本工具准备的正数参数和完整输入。

历史 raw-file 结果约 29.33 FPS（336×190/180点/1线程）、10.09 FPS（672×380/400点/2线程）。
包括 raw 文件读取，不包括视频解码、灰度转换或完整 SLAM。
比较时固定输入 SHA256、算法版本、编译选项、OpenCV、线程、供电和其他进程负载；
另行记录 CPU/RSS/温度/降频。不能用这次主机软件测试声称板端性能复测成功。

## 历史助手

`historical/benchmark_frontend.py` 与 `historical/prepare_gray_bench.py` 原样保留，
包含我们当时的绝对路径/标定路径，**不是直接可运行的推荐入口**。
Python 与 C++ 测试工作量和 OpenCV 构建不同，不拿它们推断语言本身的性能优劣。

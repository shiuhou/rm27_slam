# 来源、版本与发布边界

本仓库由用户指定，从 `shiuhou/rm27_slam-vio` 的已有源码和本地历史材料选择性导入，
不重写整个工程，不移动/删除原仓库。来源 HEAD：
`74d44b09c65e2a839b74d834756f0d178207d679`。
原工作树另有 IMU/RAM 报告等未提交修改，此发布未改动它们。
导入后另有 SLAM 删除/VIO 范围修改出现在原工作树；本任务没有执行那些修改或将其还原。
这里的来源是导入时固定的文件快照，不声称原工作树现在仍等于该快照。

[import-manifest.json](import-manifest.json) 逐项列出 77 个原文件的路径、大小与 SHA256。
原文件按字节保存，包括历史助手、报告、实际标定结果和共用 localization 包。
新的 portable `prepare_gray.py`、测试与起步说明单独标识，不冒充历史已测脚本。
`.gitattributes` 保持原字节，确保 Windows/Linux 克隆不会改变历史摘要。
原 Windows 工作区的部分文件包含 CRLF，Git whitespace 检查明确使用 cr-at-eol 口径。
旧 `collect_m3c_env.sh` 也按原字节保留；不把它当当前可直接运行的 Linux 入口。
需要复用时先在独立工作副本处理换行并记录派生 SHA256，不能覆盖原文件或伪称同一原件。

## 外部算法与依赖

| 项目 | 来源 | 历史 pin / 边界 |
|---|---|---|
| Stella | https://github.com/stella-cv/stella_vslam | `e445b5452535e781fdf6777ec33a06f5f8f5e416` |
| Stella examples | https://github.com/stella-cv/stella_vslam_examples | `defc69eecc36e51cdda22885bb86954f08ad6887` |
| ORB-SLAM3 | https://github.com/UZ-SLAMLab/ORB_SLAM3 | `4452a3c4ab75b1cde34e5505a36ec3f9edcdc4c4`；历史成功需 shutdown patch |
| g2o | https://github.com/RainerKuemmerle/g2o | `e8df2004e07ea8f5b8e6a8b9f2dc067b45b45036` |
| Pangolin | https://github.com/stevenlovegrove/Pangolin | v0.6 / `dd801d244db3a8e27b7fe8020cd751404aa818fd` |
| FBoW vocabulary | https://github.com/stella-cv/FBoW_orb_vocab | `708407ae4cd59219b996eda7ed1f4562c7ae106a` |
| MaixCAM2 capture tools | https://github.com/blademaster679/maixcam2_dart_vision | local source inspected at `6d2f6251dd839c8673cfcf8a977e22a09433afcf` |
| MaixCDK | https://github.com/sipeed/MaixCDK | 必须匹配自己设备的镜像/ABI，不指定已验证的通用最新版 |

第三方算法、SDK、词袋和二进制未 vendored；使用/再分发时检查相应上游 LICENSE。
此导入不授予新的统一许可，不把上游代码宣称为 RM27 自研。
ORB patch、build recipe、原始日志目前只由旧报告引用，未冒称已随 clone 提供。

## 数据边界

- 发布：已存在的 JSON 测速摘要和几何拟合结果、研究代码、操作说明与合成软件测试。
- 不发布：原始 90 MB H.264、图片/灰度帧、公开数据集、词袋、环境、SDK、二进制、凭证、PX4 参数/固件。
- 本地录影来源：`.maixpy/runs/os04a10-20261007-005702-52804b/record.h264`（原 VIO 工作区）。
  不因没有发布而重生成或重新采集；重放真实结果需要另行取得原输入。
- 历史报告中的 `/root/slam-bench-20261007/` 是当时部署位置，不保证当前远端状态。

本次没有 SSH、设备访问、驱动/固件/参数改变或新采集；没有写 Obsidian Vault。

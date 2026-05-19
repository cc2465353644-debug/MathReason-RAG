# Development Log

## Day 1

完成内容：

- 创建 GitHub 仓库；
- 编写第一版 README.md；
- 将项目同步到 GitHub。

遇到的问题：

- Markdown 表格和代码块格式不熟悉；
- 本地目录和 GitHub 仓库同步流程不熟悉。

解决方式：

- 学会使用 `git add`、`git commit`、`git push`；
- 配置 Git 代理后成功推送到 GitHub。

---

## Day 2

完成内容：

- 建立项目基础目录；
- 创建 `requirements.txt`；
- 测试本地模型运行；
- 修复 PyTorch CPU 版问题；
- 安装 CUDA 版 PyTorch；
- 确认 RTX 4060 可以用于本地推理。

遇到的问题：

- 运行模型时报错：`Torch not compiled with CUDA enabled`；
- 原因是安装了 CPU 版 PyTorch。

解决方式：

- 使用以下命令重新安装 CUDA 版 PyTorch：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

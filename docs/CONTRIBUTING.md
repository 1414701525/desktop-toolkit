# Contributing

欢迎贡献！以下是参与项目的基本流程。

## 如何贡献

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "Add your feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

## 开发环境

### Python 项目

```bash
# Python 3.10+ 推荐
python --version

# 安装依赖（仅 Awake 需要额外依赖）
pip install pystray pillow

# 运行测试
python -m pytest tests/
```

### C# 项目

```powershell
# 需要 .NET 8 SDK
dotnet --version

# 运行
cd AwakeLite
dotnet run

# 发布
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true
```

## 代码规范

### Python

- 遵循 PEP 8
- 使用类型注解（Type Hints）
- 函数和类添加 docstring
- 变量命名使用 snake_case

### C#

- 遵循 C# 编码规范
- 使用 PascalCase 命名类和方法
- 使用 camelCase 命名局部变量和参数
- 添加 XML 文档注释

## 提交规范

提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- `feat`：新功能
- `fix`：修复 bug
- `docs`：文档更新
- `style`：代码格式调整
- `refactor`：重构
- `test`：添加测试
- `chore`：构建/工具变更

示例：

```
feat(awake-lite): 添加自定义主题颜色支持

- 新增主题配置文件
- 支持深色/浅色主题切换
- 更新托盘图标颜色

Closes #12
```

## 报告 Issue

使用 GitHub Issues 报告 bug 或提出功能建议。请包含：

- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS 版本、Python/.NET 版本）

## Pull Request 检查清单

- [ ] 代码符合项目规范
- [ ] 添加了必要的注释和文档
- [ ] 所有现有测试通过
- [ ] 新功能包含测试
- [ ] 更新了相关文档

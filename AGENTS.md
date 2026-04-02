# AGENTS.md

## Dev environment

* Python：`>=3.10`
* 依赖管理：`uv`
* 构建后端：`hatchling`

### Setup commands

* 安装依赖：`uv sync`
* 运行 Python 测试：`uv run pytest`
* 运行 Ruff 检查：`uv run ruff check qqmusic_api tests`
* 运行 Pyrefly 检查：`uv run pyrefly check`
* 运行 Docs 构建：`uv run zensical build`
* 本地预提交检查：`uv run prek run --all-files`

## Commit messages

* 使用 Conventional Commits：`<type>(<scope>): <subject>`。
* 提交信息使用中文。
* commit-msg 钩子会校验 Commitizen / Conventional Gitmoji 格式。：

## Testing rules

* **专注 Modules 层**：测试重心放在 `modules` 层，将其视为黑盒。采用基于数据驱动（`@pytest.mark.parametrize`）的函数式测试方法，将输入参数与期望结果的特征断言解耦。
* **真实网络请求（No Mock）**：禁止 Mock 底层网络请求或核心组装逻辑。必须直接与真实的 QQ 音乐 API 交互，以验证接口连通性、参数拼装和数据模型（Models）解析的正确性。
* **优雅处理限流（Rate Limit）**：由于采用真实网络请求，当触发上游 API 的风控或频率限制异常时，必须使用自定义装饰器捕获该异常并调用 `pytest.skip()` 安全跳过，严禁因此导致测试失败。
* **平铺函数写法**：摒弃测试类（`class TestXXX`），强制采用平铺的独立纯函数（Flat Functions）编写测试用例，通过 fixtures 注入依赖，保证测试的独立性。
* 测试用例必须包含单行中文 docstring，且 docstring 内部必须使用英文标点符号。
* 优先在现有的测试文件中添加用例，仅在测试全新模块时才允许创建新的测试文件。

## Documentation rules

### Python

* Docstrings 使用 Google Style。
* public API、class、方法、函数必须有 docstring。
* 测试函数必须包含单行中文 docstring（英文标点）。
* `Args` / `Returns` / `Yields` / `Raises` 按需提供。
* 仅描述可观察行为，禁止描述实现细节。
* 类型检查以 `pyrefly` 为准，不使用 `basedpyright`。

### docs/

* 仅面向用户，描述 Usage 与 Behavior。
* 新增页面必须同步更新 `zensical.toml` 的 `nav`。
* 文档构建工具实际使用 `zensical`，配置文件是 `zensical.toml`。

## Agent behavior

* 每次回答都以 `皇上启奏:` 开头。
* **核心规约**：遵循 `docs/contributing.md` 中的详细规约。**在执行任务前，必须完整阅读该指南以确保合规。**
* 仅在明确要求时，才能 `git commit` 或 `git push`。

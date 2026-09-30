# MCP 服务清单

## Gety

用途：检索已索引的本地文件及相关内容片段。
官方接入说明：https://docs.gety.ai/mcp

2026-09-28 只读检查：
- Codex：E:/CodexHome/config.toml 已有 gety MCP 配置。
- DeepSeek Harness：用户 .dsh/cordis.patch.yml 已有 Gety 管理的接入段，注明端口与授权字段由 Gety 自动维护。
- WorkBuddy：客户端已安装；Gety 连接状态尚未核实。
- 当前任务未实际调用 Gety 搜索，故上述不等于端到端验证。

Gety 设置 -> AI Integrations 可配置客户端。优先由 Gety 管理接入；本库不覆盖这些字段，不保存端口快照为永久配置，不保存令牌。
接入后在三个客户端分别搜索同一个已知文档，并核对路径和片段。搜索结果进入云端模型上下文时，会发送给该模型服务；本地索引不等于内容永不出本机。

其他 MCP 日后按服务添加说明和不含凭据的配置模板；各客户端认证与权限仍分别管理。

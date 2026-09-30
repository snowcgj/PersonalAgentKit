---
name: agentkit-library
description: 查找或维护用户在 D:/AgentKit 的跨客户端公共规则、Skills、知识入口和 MCP 服务清单；适用于公共资产更新、同步和接入状态排查。
---

# AgentKit 公共库

先读 D:/AgentKit/README.md。按任务只读相关目录：规则 rules/common.md；知识 knowledge/INDEX.md；服务 mcp/README.md；客户端路径 adapters/clients.json。

公共源是 D:/AgentKit，客户端副本不作为新来源。更新源内容后运行 `pwsh -File D:/AgentKit/tools/sync.ps1` 预览；已获同步授权时运行同一命令加 `-Apply`。
发生冲突时展示涉及路径和差异，与用户确认应保留的内容，不删除状态文件来绕过冲突。
不要把厂商专属工具名称或 API Key 写入通用 Skill；专属能力保留在对应客户端。
客户端的实际加载须在新任务中验证，不能用模型自称“已加载”作为唯一证据；让它读取对应文件并核对内容。

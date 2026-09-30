# 接入验证状态（2026-09-28）

| 客户端 | 公共规则 | 公共 Skill | Gety |
|---|---|---|---|
| Codex | 文件同步完成；当前任务收到更新后的 AGENTS.md，确认规则加载 | 文件同步完成，等待新任务技能发现验证 | 已存在配置，未做搜索验证 |
| DeepSeek Harness / DSH Desktop | 用户 .dsh/AGENTS.md 已分发，等待新任务验证 | 用户 .dsh/skills 已分发，等待发现验证 | Gety 管理的配置已存在，未做搜索验证 |
| WorkBuddy | 用户 .codebuddy/CODEBUDDY.md 已分发，兼容路径需本机新任务验证 | 用户 .workbuddy/skills 已分发，等待发现验证 | MCP 服务端已实测可用；WorkBuddy 客户端侧仍需在连接器里 Trust 后新开任务 |

同步脚本已验证：预览无写入、原内容保留、重复运行不变、源更新、标记外修改保留、标记内冲突拒绝。修正了 Windows 换行差异导致误报冲突的问题。
已有 Codex 全局规则的原文字节已在 backups 中备份。未修改模型、认证、MCP 配置、Gety 索引范围和软件权限。

在另外两个软件中新开任务，发送：
“请检查你是否自动加载了 AgentKit 公共规则和 agentkit-library Skill。先报告实际加载证据，再读取 D:/AgentKit/rules/common.md 和 D:/AgentKit/skills/agentkit-library/SKILL.md，说明公共源在哪里、修改后如何同步。区分自动发现和按我提供的路径手动读取，不要修改文件。”

若只能手动读取，需要继续排查客户端的全局加载入口，而不是认为已经完成接入。

## WorkBuddy 数据迁移（2026-09-28）
实际数据已迁至 D:/AgentData/WorkBuddy，C:/Users/29485/.workbuddy 保留为 Junction。AgentKit 分发路径无需变更，同步预览正常。WorkBuddy 已启动，D 盘出现新 WAL 和日志；界面历史任务及 Gety 搜索待用户验证。C 盘备份保留在 C:/Users/29485/.workbuddy.backup-20260928-151235。

### 迁移后验证（2026-09-28 15:30，已实测）
- 配置落点：进程 WORKBUDDY_CONFIG_DIR=C:/Users/29485/.workbuddy（Junction）→ 实际 D:/AgentData/WorkBuddy；新写入落在 D（workbuddy.db-wal 持续更新）。
- 历史任务：projects/ 下三个会话 jsonl 均在 D 且可读，当前会话文件持续增长 —— 界面历史可用。
- 功能：node v22.22.2、python 3.13.14 可调用；用户 Skill agentkit-library 与内置插件从 ~/.workbuddy 路径正常解析；用户 MEMORY.md 已注入；MCP 通道可用（agent-mail 返回未开通，非故障）。
- 完整性：备份与新目录顶层条目无差异，skills/plugins/binaries/app/security 文件数与体积一致或更多，无丢失。
- 未受影响：.codebuddy/CODEBUDDY.md 仍在 C 且完整；工作区 C:/Users/29485/WorkBuddy 仅 320 KB；Gety 数据在 AppData，不受影响。
- 仍待验证：Gety 在 WorkBuddy 内的调用（需先在连接器里 Trust）；C 盘 940 MB 备份是否删除。

### Gety MCP 验证（2026-09-28 16:20，已实测到服务端）
- 配置：Gety 已自动写入 ~/.workbuddy/mcp.json（http://127.0.0.1:31226/mcp，Bearer token）；Gety.exe 在运行，端口 31226 处于 LISTENING。
- 服务端直连实测：initialize 返回 200，serverInfo=Gety 0.6.3，tools/list 返回 3 个工具 —— Search、GetDoc、ListConnectors。
- 端到端检索（同一已知文件法）：查询 common.md 中的原句「Gety 只覆盖它实际索引的资料」，77 条命中，第 1 条即 D:/AgentKit/rules/common.md（真实路径与片段，非猜测路径），第 2 条为 E:/CodexHome/AGENTS.md 副本。索引覆盖 C/D/E/F 四个 NTFS 卷。
- 客户端侧未完成：当前会话工具列表与 mcp-tool-list.json 均无 gety，日志无连接记录 —— 需在 WorkBuddy「连接器 → 自定义连接器 → MCP Server Management」里对 gety 点 Trust，再新开任务。
- 副作用提示：Gety 索引含 D:\，迁移后的 WorkBuddy 数据（会话 jsonl、日志）也在索引范围内，需要时可在 Gety 里排除 D:/AgentData。


# AgentKit：个人公共 Agent 资产

这是唯一人工维护的公共来源。Codex、DeepSeek Harness、WorkBuddy 中的 AgentKit 内容是可重新生成的副本。

例外：`D:/AgentKit/TODO.md` 是所有 agent 直接共同维护的唯一待办文件，不分发副本。它记录跨会话待处理事项，包含维护约定和执行条件；记录事项不代表授权执行。用户明确提出待办时先查重再记录，更新前重新读取，避免覆盖其他 agent 的修改。维护入口已写入公共规则。已运行的客户端可能需要新开任务才能加载更新规则。

## 日常用法

数据位置和管理约定见 [Agent 数据管理](knowledge/Agent数据管理.md)。这份公共背景按需读取，不要求每个任务加载全部知识。

1. 改公共规则：编辑 rules/common.md。
2. 加公共 Skill：在 skills/agentkit-名称/SKILL.md 编写，配套文件留在同目录。客户端特有工具需另行适配。
3. 加知识：更新 knowledge/INDEX.md；原始项目文件留在原位置。
4. 预览同步：`pwsh -File D:/AgentKit/tools/sync.ps1`
5. 确认输出后应用：`pwsh -File D:/AgentKit/tools/sync.ps1 -Apply`
6. 新开客户端任务验证加载；已有长对话可能保留旧上下文。

每次更新源后需运行同步，不是实时文件监控。同步仅处理规则标记块和本库的 agentkit-* Skills；发生目标修改、来源删除、同名冲突会停止，不自动裁决或删除。

## 接入位置

见 adapters/clients.json。规则路径：Codex 的 E:/CodexHome/AGENTS.md；Harness 的用户 .dsh/AGENTS.md；WorkBuddy 使用官方说明兼容的用户 .codebuddy/CODEBUDDY.md。公共 Skill 分发到三个客户端各自的 skills 目录。

WorkBuddy 的全局兼容路径及 Harness 当前桌面版本的实际加载都需要新任务验证。如果某客户端未加载，检查其版本和设置，不能直接宣布成功。

## 范围

不合并三个软件的整个配置文件。不迁移登录信息、API Key、内部数据库、自动记忆、内置或商店插件。不把 Codex 专用排障 Skill 当作通用技能分发。旧 D:/CodexKit 已停止维护，唯一记录已完整归档至 tasks/电脑存储维护/历史来源；现行入口统一使用 AgentKit。2026-09-30 用户已授权删除旧目录，但自动审批阻止执行，目录尚在，待用户手动删除。

Gety 接入由 Gety 管理，见 mcp/README.md。模型密钥仍由对应客户端管理。

## 备份与恢复

写入前备份旧文件，保存在 backups/时间戳，manifest.json 记录原路径、备份文件和写后哈希。backup 为 null 表示此次新建。
需要撤回时先比较文件当前哈希与 manifest 中 new_hash；存在后续修改应先合并，不直接恢复。旧文件可从备份恢复；新建文件的删除需用户明确授权。恢复后同步状态也需相应调整，不能无条件删除整个 state.json。
备份目录只保存在本机，不放进公共分发内容。

## 验证

在每个客户端的新任务中请求：“找到公共库路径，读取公共规则和 agentkit-library Skill，报告来源路径并概括维护方式。”
然后用同一已知文件测试 Gety；仅返回猜测路径不算验证。记录在 adapters/STATUS.md。

## 依据

- Harness 全局指令及技能目录：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/config-catalog.md
- WorkBuddy 项目与 CodeBuddy 用户配置兼容：https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project
- 用户规则路径：https://www.codebuddy.cn/docs/cli/memory
- Gety：https://docs.gety.ai/mcp

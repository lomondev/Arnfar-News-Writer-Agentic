# Fact ledger — AI tools/skills for making diagrams (diagram-design, drawio-skill, Excalidraw MCP) — 2026-10-13

Mode: digest (3 items, explainer). Style: diagram.

## diagram-design (cathrynlavery)
| # | Fact | Figure | Confidence | Sources |
|---|---|---|---|---|
| 1 | Open-source agent skill for editorial-style diagrams; on GitHub Trending 2026-10-11 | — | ຢືນຢັນແລ້ວ | [1][2] |
| 2 | 44 diagram types (Skillselion says 41 — older count) | 44 | ຢືນຢັນແລ້ວ (repo + AIToolly) | [1][2]; [3]=41 |
| 3 | Agents: Claude Code, Codex, GitHub Copilot, Cursor, Factory Droid, Pi (+ others) | — | ຢືນຢັນແລ້ວ | [1][2] |
| 4 | Output self-contained HTML + inline SVG; export SVG/PNG; offline | — | ຢືນຢັນແລ້ວ | [1][2][3] |
| 5 | Brand onboarding reads website colours/fonts; contrast check | — | ຢືນຢັນແລ້ວ (2) | [1][3] |
| 6 | Redraws draw.io / Mermaid / Excalidraw files | — | ຢືນຢັນແລ້ວ (2) | [1][3] |
| 7 | MIT licence | — | primary | [1] |
| 8 | Stars (51.5k on repo vs 31.7k on Skillselion) | — | conflicting — omit | [1][3] |
| 9 | Caveat: quality depends on model; layouts vary; output not editable source | — | primary | [1] |

## drawio-skill (Agents365-ai)
| 10 | Agent skill: prompt/code/Terraform/K8s/SQL/OpenAPI/GraphQL → editable draw.io diagrams | — | primary + listings | [4][5] |
| 11 | Self-checks rendered PNG and fixes layout | — | primary | [4] |
| 12 | Exports PNG/SVG/PDF, HTML viewer, PPTX, Mermaid | — | primary | [4] |
| 13 | Agents: Claude Code, Cursor, Copilot, Codex, others | — | primary | [4] |
| 14 | Requires draw.io desktop CLI; MIT | — | primary | [4] |
| 15 | Stars ~10.1k | — | 1 source — omit | [4] |

## Excalidraw MCP
| 16 | Official Excalidraw MCP (excalidraw/excalidraw-mcp, mcp.excalidraw.com/mcp) turns chat into editable hand-drawn diagrams | — | ຢືນຢັນແລ້ວ (2) | [6][7] |
| 17 | Usable as Claude connector; installable to Claude Code, Codex, Cursor | — | ລາຍງານ (2) | [6][7] |
| 18 | Edit by request (add/remove/rearrange), open in Excalidraw | — | ຢືນຢັນແລ້ວ (2) | [6][7] |
| 19 | Tester notes: layout/icon placement still needs manual fixes | — | ລາຍງານ (1, hands-on) | [6] |
| 20 | Community yctimlin/mcp_excalidraw: live canvas, 26 tools, MIT | — | not used on cards | [8] |

## Caveats
- Lao text rendering in generated diagrams not verified.
- Cloud processing of prompts/system descriptions.

Sources:
[1] GitHub — cathrynlavery/diagram-design — https://github.com/cathrynlavery/diagram-design
[2] AIToolly (2026-10-11/12) — https://aitoolly.com/ai-news/article/2026-10-12-diagram-design-launches-editorial-grade-diagram-system-for-leading-ai-coding-assistants-and-develope
[3] Skillselion guide (upd. 2026-09-27) — https://skillselion.com/guides/diagram-design-skill-claude-code-guide
[4] GitHub — Agents365-ai/drawio-skill — https://github.com/Agents365-ai/drawio-skill
[5] skills-hub.ai — draw-io skill — https://skills-hub.ai/skills/agent-toolkit-draw-io
[6] Classmethod (2026-03-01) — https://dev.classmethod.jp/en/articles/excalidraw-mcp-claude-code/
[7] MCP Servers — Excalidraw remote MCP — https://mcpservers.org/remote-mcp-servers/excalidraw-app-demo
[8] MCP Servers — yctimlin/mcp_excalidraw — https://mcpservers.org/servers/yctimlin/mcp_excalidraw

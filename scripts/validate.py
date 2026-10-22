#!/usr/bin/env python3
"""检查技能集的结构：JSON 能解析、每个 SKILL.md 的 frontmatter 有 name/description、
name 和目录名一致、每个子技能都在入口技能里有路由。CI 和本地都跑这一个脚本。"""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
errors = []

for path in [*ROOT.glob(".claude-plugin/*.json"), *ROOT.glob("plugins/*/.claude-plugin/plugin.json")]:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: JSON 解析失败：{exc}")

skills = {}
for skill_md in ROOT.glob("plugins/*/skills/*/SKILL.md"):
    rel = skill_md.relative_to(ROOT)
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{rel}: 缺少 frontmatter")
        continue
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{rel}: frontmatter 不是合法 YAML：{exc}")
        continue
    name = meta.get("name")
    if not name or not meta.get("description"):
        errors.append(f"{rel}: frontmatter 需要 name 和 description")
    elif name != skill_md.parent.name:
        errors.append(f"{rel}: name「{name}」和目录名「{skill_md.parent.name}」不一致")
    skills[name] = text

router = skills.get("ship-it", "")
if skills and not router:
    errors.append("缺少入口技能 ship-it")
for name in sorted(skills):
    if name != "ship-it" and f"`{name}`" not in router:
        errors.append(f"入口技能没有提到子技能：{name}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"通过：{len(skills)} 个技能")

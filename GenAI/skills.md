# Agent skills
- Agent skils are folders of Instructions, scripts, and resources, that load on demand, to perform certain tasks, and is an open standard
- Tailor domain specific agents, reducing reptition, and create complex workflows
- How to do the work, and how you want it to be done
- .github/skills/<skill domain>/SKILL.md
- Sample skill, related to PRD drafting shown below. [Reference](https://www.youtube.com/watch?v=JepVi1tBNEE&list=PPSV&t=22s)
- Load progressivelyed (only, if needed)
- Skills could tie up with scripts, documentation, that already exists
- Useful in reducing context window. Similar results can be achieved using instructions, but they're loaded always, polluting the contenxt window and filling it up quickly
```markdown
name:
description:
---
# <Title of skill>
## What this skill does
## When to use the skill

<!-- steps specific to skill, instructions etc -->
## Context Grathering
## Section drafting
## validation

## Checklist
## Example
## Tips and Best Practices
```

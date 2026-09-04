
## Prompt files
- Prompt files are reusable prompts (this is reusable in chats)
- Use `Configure Prompts` in VSCode, new prompt files
- Example of `remember` prompt (save as remember.prompt.md file)
```md
---
agent:
description:
model:
---
<variables>
MEMORY_FILE_PATH: .github/instructions/memory.instructions.md
</variables>

The user is asking you to save your memory. The memory is special instruction file, located at MEMORY_FILE_PATH
```
- Once defined, you can trigger using `/remember` in chat

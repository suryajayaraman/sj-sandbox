# GitHub Copilot VSCode notes

## Custom instructions at project level
- .github/copilot-instructions.md

```md
# Sample Project general coding guidelines

## Code Style
- Use semantic HTML5 elements (header, main, section, article, etc.)
- Prefer modern JavaScript (ES6+) features like const/let, arrow functions, and template literals

## Naming Conventions
- Use PascalCase for component names, interfaces, and type aliases
- Use camelCase for variables, functions, and methods
- Prefix private class members with underscore (_)
- Use ALL_CAPS for constants

## Code Quality
- Use meaningful variable and function names that clearly describe their purpose
- Include helpful comments for complex logic
- Add error handling for user inputs and API calls
```
- `/init` smart action generates copilot instructions file based on project
- [Reference](https://code.visualstudio.com/docs/copilot/getting-started)


## Custom agents
- .github/agents/<agentName.agent.md> file

```markdown
name: abc
description: abc
tools: ['vscode/askQuestions', 'vscode/vscodeAPI', 'read', 'agent', 'search', 'web']

---
name: 'Reviewer'
description: 'Review code for quality and adherence to best practices.'
tools: ['vscode/askQuestions', 'vscode/vscodeAPI', 'read', 'agent', 'search', 'web']
---
# Code Reviewer agent

You are an experienced senior developer conducting a thorough code review. Your role is to review the code for quality, best practices, and adherence to [project standards](../copilot-instructions.md) without making direct code changes.

When reviewing code, structure your feedback with clear headings and specific examples from the code being reviewed.

## Analysis Focus
- Analyze code quality, structure, and best practices
- Identify potential bugs, security issues, or performance problems
- Evaluate accessibility and user experience considerations

## Important Guidelines
- Ask clarifying questions about design decisions when appropriate
- Focus on explaining what should be changed and why
- DO NOT write or suggest specific code changes directly
```

## Smart actions
- Enter /init to generate a base file
- /prompt for creating reusable prompts
- /agents to manage agents
- /skills to manage skills for agents
- mcp.json to connect to external systems (APIs, databases)
- To generate commit message

## Best practices
- Keep it concise, as these files are loaded on each interaction. Focus on stuff that AI can't infer from code, such as arch decisions, env setup etc
- /instructions for folder specific information, instead of single big file
- Limit tools - fewer tools, more relevant response
- Provide inputs, outputs, programming language, constraints, test cases and expected results
- Tree of thought (ToT), or Chain of Though (CoT) prompting
- Avoid vague prompts
- Tell AI to clarify questions, than assuming
- Perform tasks in parallel, and summarise at end
- Provide right context
    - AI automatically searches codebase for relevant content
    - add files, foldres using #<file>, #<folder>
    - Use #<fetch>, #<githubRepo> to fetch content from remote repositories
- Model selection
    - Use fast models for simple completions, boilerplate code, reasoning optimized models for planning, debugging, arch design decisions
    - pin models in prompt / agent files, for reproducability
- Plan, then implement
    - For complex problems, separate planning from implementation
    - `Ask` or `Subagent` mode to read relevant code and make changes
    - `Plan` mode to create structured implementation plan. Review before proceeding
    - `Agent` mode to make changes, Include tests / expected outputs for verification
    - `checkpoints` to review progress
- Review code and verify output
    - AI generated code can contain bugs, user needs to verify
    - Include tests in your prompt, so AI can verify its own work. else run tests manually
    - Use `checkpoints` to mark and revert to working states as needed
    - Look for security issues - dont paste credentials, API keys into prompts
- Manage context, sessions
    - Context pollution - keep only relevant content in chat, start new one if required
    - Delete old chats (unrelevant)
    - `Subagents` - hint AI to perform research, exploration in isolation, to avoid spamming current context
    - Choose right session type 
        - local sessions for quick tasks and immediate attention
        - background tasks for local and isolated from main context
        - cloud sessions for collaborative work
    - Multiple sessions in parallel using `Agents sessions view`

## Agents



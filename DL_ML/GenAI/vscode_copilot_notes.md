# GitHub Copilot VSCode notes

## How Prompts are used in VSCode
- If you compile a system prompt like "Hello World" in GHC, copilot sends a prompt like below (context window gets added)
- For new messages, all the below and responses from model, are appended and sent again

```md
<!-- Very generic identity and rules -->
# System Prompt
## Core functionality and global rules
you're an intelligent AI coding assistant

<!-- This i very specific to model -->
## general instructions (model specific)
Never print code block with file changes

## Tool use instructions
Dont call run in terminal command, multiple times in parallel

## Output format instructions
How to format output in chat for toeknization of things like file links

-------------------------------------

<!-- Next, uer prompt gets added -->
# User prompt
## Environment Info
OS info etc

## Workspace infor
project
    Folder1
        File1
        File2
    Folder2

-------------------------------------

<!-- 2nd User prompt, containing context window -->
# User prompt2
## Contact infor
Current date, time; list of open terminals

## Editor context
any files, user has added to chat

## User request
Hello World
```


### Intructions file
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
-  General project structure, patterns that be used, at project level. (custom instructions get added in context window), **get added at last, to Agent System prompt**
- Can have multiple instructions file. **copilot instructions is the last file to get added, in System prompt**
- [Reference](https://code.visualstudio.com/docs/copilot/getting-started)
- Sample structure
```md
# Copilot instructions for <project>
## Steps to build project
## Naming conventions
## Source file conventions
## Formatting
<!-- refer to clang-formatting and other tools -->
## Copyright headers
## Code Review focus
## Acronyms
## Documentation and comments guidelines
```

### prompt files
- Gets added, before Context info in `User prompt`
- User request gets modified to `Follow instructions in []() - Hello World`


## Custom agents
- .github/agents/<agentName.agent.md> file
- Way to specify overriding instructions to defautl Agent bheaviour
- `Plan` mode is example of custom agent, intended to research, plan, not implement
- **Custom agent instructions, gets added after custom instructions**

```markdown
---
name: 'Reviewer'
description: 'Review code for quality and adherence to best practices.disable-mode-invocation: true
tools: ['vscode/askQuestions', 'vscode/vscodeAPI', 'read', 'agent', 'search', 'web']
handoffs:
    - label: name of handoff
      agent: agent
      prompt: 'Start Implementation'
      send: true
---
# Code Reviewer agent

You are an experienced senior developer conducting a thorough code review. Your role is to review the code for quality, best practices, and adherence to [project standards](../copilot-instructions.md) without making direct code changes.

When reviewing code, structure your feedback with clear headings and specific examples from the code being reviewed.

<rules>
- rule 1
</rules>

<workflow>

## 1. Discovery
<!-- Focus on high level concepts; check for feasibility -->
<!-- Use subagents -->
<research_instructions> </research_instructions>

## 2. Alignment
- Use #tool:vscode/askQuestions to ask clarifying questions

## 3. Design
- Once context is clear, draft comprehensive implementation plan per  <plan_style_guide>

## 4. Refinement
- Show draft to user. Clarify doubts; atlernatives to explore; Once approval given, acknowledge, user able to see handoff buttons
- Keep iterating until explicit approval, or handoff

</workflow>


<plan_style_guide>
## Plan
**Steps**
**Verification**
**Decisions**
</plan_style_guide>


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
- Enter `/init` to generate a instructions file
- /prompt for creating reusable prompts
- /agents to manage agents
- `/skills` to manage skills for agents
- mcp.json to connect to external systems (APIs, databases)
- To generate commit message
- `/generate` from awesome copilot structured autonomy generate to generate implementation, provided a plan md file. This generates all content, in single PR, and with testable commits for each step

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
- `Context rot` - as contenxt window grows, model peformance drops significantly
- Dont worry about location of prompty / custom instruction file
- `Premimum planning; thrifty implementation` - generate a markdown file, containing all changes to be made -  this can be done by premimum model, but implementation can be done by model, with lesser premimum requests

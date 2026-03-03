# Custom AI agents with VSCode

## Usecase
- Specialized roles like Planner, Architect, Reviewer
- Role specific behavior - instructions, tools, context
- Handoffs b/w agents
- Agents can leverage MCPs
- standard migrations rules apply automatically 
- Controlled scope, limited at each agent level
- Use models better reasoning, for code changes suggestion (create an md file), smaller / faster model for actual code changes

## Evolution
### Agents
- Generic assiatance, with limited context
- Manual setup and repetitive prompts
- Prone to hallucination

### Custom chat mode
- Specific roles / workflows
- domain specific context

### Custom agents
- Automate tasks end to end, one tailored for each task

## Example usecase

### Goal
- Migrating test cases from unitTest to pytest for an application

### Task breakdown
#### Planner agent
- Defines overall mighration strategy and sequences

#### Environment setup Agent
- Prepare dependencies and hands over a ready environment

#### Codebase analysis agent
- Supplies code insights for mihration

#### Test migration agent
- Convert old test caes to new framework

#### Test validation agent
- Executes migrated tests for correctness

#### Documentation agent
- Updates documentation

### Implementation
- Configure custom agents
- Add description, tools
    - Tools can be either built-in (or) through MCP servers
        - understand each by reading docs
        - `search` for searching codebase
        - `todos` for multi-step process
    - handoffs
        - label: Agent handoff id
        - agent: receipient agent id
        - prompt: Prompt to recipient agent
        - send: true / false
- Handoffs can be non linear or bidirectional as well
- Agent md files can be created by agents themselves
- Orchestrator agent to automate planning

- Example
```md
---
name:
description
tools : ['search', 'fetch', 'githubRepo', 'todos']
model: 
handoffs:
    - label: Enviornment Setup
      agent: Endivonrment_Setup_agent
      prompt: Planning complete. Being einvronment setup phase - Analyse README.md and pyprooject.toml for environment requirements. Check for existing condac envrionemnts matching required python version. Create of arctivate pappropriate environment. Install all pdendencies from pyporject.toml and requirments. txt.  Validate all package imports. After environment setup is validates, automatically hand off to Codebsase_Analyaysis_aGent
      send: true
    

```

## Questions
- How to create good agent.md files?
- Can we reuse prompt file, instead of entering inline prompts?
- Configuring permissions for each agent (included in agent.md file)?
- Artifacts (md files) to save understanding of codebase analysis
- Custom MCP within organizations

# Skills for AI Agents

This repository contains skills to use with AI agents like Claude. Skills are modular, self-contained packages that extend an AI agent's capabilities by providing specialized knowledge, workflows, and tools.

## About Skills

Skills are folders of instructions, scripts, and resources that AI agents load dynamically to improve performance on specialized tasks. Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata that the agent uses.

This repository follows the [Agent Skills standard](https://github.com/anthropics/skills) created by Anthropic.

## Repository Structure

```
skills/
├── greeting-assistant/    # Sample skill demonstrating the basic structure
│   └── SKILL.md          # Skill instructions and metadata
└── [future-skills]/       # Add more skills here
```

## Skill Format

Each skill consists of:

- **SKILL.md** (required): Contains YAML frontmatter with metadata and Markdown instructions
  - `name`: The skill identifier
  - `description`: What the skill does and when to use it
  - Instructions in Markdown format

- **Optional bundled resources**:
  - `scripts/`: Executable code for deterministic tasks
  - `references/`: Documentation loaded as needed
  - `assets/`: Files used in output (templates, images, etc.)

## Sample Skill

The `greeting-assistant` skill demonstrates a simple, complete skill implementation. It shows:
- Proper YAML frontmatter structure
- Clear capability descriptions
- Step-by-step usage instructions
- Examples and best practices

## Creating New Skills

To create a new skill:

1. Create a folder in `skills/` with your skill name
2. Add a `SKILL.md` file with:
   - YAML frontmatter (name and description)
   - Markdown instructions for using the skill
3. Optionally add `scripts/`, `references/`, or `assets/` folders as needed

## Learn More

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)

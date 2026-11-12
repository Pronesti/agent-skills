# Agent skills

A curated library of 74 agent skills for Codex, Claude Code, and Cursor: 54 standalone skills and a 20-skill Caveman edition, vendored from their authors at pinned revisions. It also ships one set of global instructions shared by Codex and Claude Code, and an installer that links everything into each host.

Only seven focused skills start on their own; every other skill runs when you select it. [POLICY.md](POLICY.md) explains the rules and the reasons behind them.

## Install

```sh
git clone https://github.com/Pronesti/agent-skills
cd agent-skills
python3 scripts/install.py   # preview
./install.sh                 # apply
```

The installer links skills into `~/.agents/skills` and `~/.claude/skills`, creates the shared global instructions only where none exist, and generates a machine-specific PHP runtime profile. Existing files are preserved or backed up. To update later:

```sh
git pull --ff-only && ./install.sh
```

The Caveman plugin and the instruction sync need extra steps; see the [installation guide](MANIFEST.md#installation).

## Read next

- [MANIFEST.md](MANIFEST.md): the catalog, sources, installation, and updates.
- [POLICY.md](POLICY.md): which skills start automatically, and why.
- [WORKFLOW-GUIDE.md](WORKFLOW-GUIDE.md): 56 scenarios showing which skills to use, in which order.
- [config/AGENTS.md](config/AGENTS.md): the shared global instructions template.

## Checks

```sh
python3 -m unittest discover tests
pip install -r scripts/requirements.txt && python3 scripts/validate.py
```

Third-party licenses are in [licenses/](licenses/).

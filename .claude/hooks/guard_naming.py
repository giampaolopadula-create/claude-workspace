import sys, json, os, re

WORKSPACE_ROOT = "c:/Users/giampaolo.padula_pig/Desktop/Claude Workspace"
root_norm = WORKSPACE_ROOT.replace("\\", "/")
NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*\.md$')

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

file = data.get("tool_input", {}).get("file_path", "")
if not file:
    sys.exit(0)

file_norm = file.replace("\\", "/")
if not file_norm.lower().startswith(root_norm.lower() + "/"):
    sys.exit(0)

rel = file_norm[len(root_norm) + 1:]
parts = rel.split("/")
if len(parts) < 2:
    sys.exit(0)

top_level = parts[0]
if top_level not in ("context", "workflows"):
    sys.exit(0)

if os.path.isfile(file_norm):
    sys.exit(0)

base = parts[-1]
if not base.lower().endswith(".md"):
    sys.exit(0)

if not NAME_RE.match(base):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Nome file non conforme: dentro context/ e workflows/ i nuovi file .md devono avere nomi minuscoli, senza accenti o caratteri speciali, con parole separate da trattini (es. nome-file.md)."
        }
    }))

sys.exit(0)

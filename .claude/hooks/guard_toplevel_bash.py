import sys, json, os, re

WORKSPACE_ROOT = "c:/Users/giampaolo.padula_pig/Desktop/Claude Workspace"


def norm_path(p):
    p = p.replace("\\", "/")
    m = re.match(r'^/([a-zA-Z])/(.*)$', p)
    if m:
        p = m.group(1) + ":/" + m.group(2)
    return p


root_norm = norm_path(WORKSPACE_ROOT)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

command = data.get("tool_input", {}).get("command", "")
if not command or "mkdir" not in command:
    sys.exit(0)

tokens = re.findall(r'"([^"]+)"|\'([^\']+)\'|(\S+)', command)
flat = [t[0] or t[1] or t[2] for t in tokens]

if "mkdir" not in flat:
    sys.exit(0)
idx = flat.index("mkdir")

candidate = None
for tok in flat[idx + 1:]:
    if tok.startswith("-"):
        continue
    candidate = tok
    break

if not candidate:
    sys.exit(0)

p = norm_path(candidate)
if not re.match(r'^[a-zA-Z]:/', p):
    p = root_norm + "/" + p

if not p.lower().startswith(root_norm.lower() + "/"):
    sys.exit(0)

rel = p[len(root_norm) + 1:]
parts = [x for x in rel.split("/") if x]
if not parts:
    sys.exit(0)

top_level = parts[0]
top_level_path = root_norm + "/" + top_level

if not os.path.isdir(top_level_path):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Questo comando creerebbe una nuova cartella di primo livello ('" + top_level + "') senza approvazione esplicita. Chiedi conferma a Giampaolo prima di procedere."
        }
    }))

sys.exit(0)

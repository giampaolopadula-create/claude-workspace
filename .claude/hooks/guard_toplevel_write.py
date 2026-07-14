import sys, json, os

WORKSPACE_ROOT = "c:/Users/giampaolo.padula_pig/Desktop/Claude Workspace"

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

file = data.get("tool_input", {}).get("file_path", "")
if not file:
    sys.exit(0)

file_norm = file.replace("\\", "/")
root_norm = WORKSPACE_ROOT.replace("\\", "/")

if not file_norm.lower().startswith(root_norm.lower() + "/"):
    sys.exit(0)

rel = file_norm[len(root_norm) + 1:]
parts = rel.split("/")
if len(parts) < 2:
    sys.exit(0)

top_level = parts[0]
top_level_path = root_norm + "/" + top_level

if not os.path.isdir(top_level_path):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Questo percorso creerebbe una nuova cartella di primo livello ('" + top_level + "') senza approvazione esplicita. Chiedi conferma a Giampaolo prima di procedere."
        }
    }))

sys.exit(0)

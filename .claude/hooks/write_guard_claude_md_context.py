import sys, json, os

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

file = data.get("tool_input", {}).get("file_path", "")
if not file:
    sys.exit(0)

file_norm = file.replace("\\", "/")
base = file_norm.rsplit("/", 1)[-1]
is_claude_md = base == "CLAUDE.md"
is_context_md = "/context/" in file_norm and file_norm.endswith(".md")

if (is_claude_md or is_context_md) and os.path.isfile(file_norm):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Il file esiste gia: usa Edit invece di Write per una modifica mirata, oppure leggi il file e mostra un diff esplicito prima di riscriverlo interamente."
        }
    }))

sys.exit(0)

import sys, json, os, re

WORKSPACE_ROOT = "c:/Users/giampaolo.padula_pig/Desktop/Claude Workspace"


def norm_path(p):
    p = p.replace("\\", "/")
    m = re.match(r'^/([a-zA-Z])/(.*)$', p)
    if m:
        p = m.group(1) + ":/" + m.group(2)
    return p


root_norm = norm_path(WORKSPACE_ROOT)

# Sanctioned exceptions outside the workspace:
# 1. The session scratchpad under AppData/Local/Temp/claude/<project>/<session-id>/scratchpad
#    (session-id varies per session, user-folder segment may appear as short 8.3 name or long name).
SCRATCH_RE = re.compile(
    r'appdata/local/temp/claude/c--users-giampaolo-padula-pig-desktop-claude-workspace/[^/]+/scratchpad(/|$)',
    re.IGNORECASE,
)
# 2. The auto-memory directory for this project.
MEMORY_RE = re.compile(
    r'\.claude/projects/c--users-giampaolo-padula-pig-desktop-claude-workspace/memory(/|$)',
    re.IGNORECASE,
)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

file = data.get("tool_input", {}).get("file_path", "")
if not file:
    sys.exit(0)

p = norm_path(file)

if p.lower() == root_norm.lower() or p.lower().startswith(root_norm.lower() + "/"):
    sys.exit(0)

if SCRATCH_RE.search(p):
    sys.exit(0)

if MEMORY_RE.search(p):
    sys.exit(0)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "Percorso fuori dal workspace autorizzato ('" + file + "'). "
            "I file vanno creati dentro 'Claude Workspace', nello scratchpad di sessione, "
            "o nella cartella di memoria automatica. Se questo percorso e' davvero necessario, "
            "chiedi conferma esplicita a Giampaolo prima di procedere."
        )
    }
}))

sys.exit(0)

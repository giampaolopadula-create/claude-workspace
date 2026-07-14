import sys, json, os, re

WORKSPACE_ROOT = "c:/Users/giampaolo.padula_pig/Desktop/Claude Workspace"
APPROVAL_MARKER = "#giampaolo-approved"

NO_DEST_CMDS = {"rm", "rmdir", "remove-item", "ri", "rd", "del", "erase"}
DEST_CMDS = {"mv", "move-item", "mi", "move", "rename-item", "rni", "ren", "rename"}
WATCHED = NO_DEST_CMDS | DEST_CMDS
DEST_FLAGS = {"-destination", "-newname", "-target-directory", "-t"}

SEGMENT_SPLIT_RE = re.compile(r'\n|;|&&|\|\|(?!\|)|\|')


def norm_path(p):
    p = p.replace("\\", "/")
    m = re.match(r'^/([a-zA-Z])/(.*)$', p)
    if m:
        p = m.group(1) + ":/" + m.group(2)
    return p


root_norm = norm_path(WORKSPACE_ROOT)


def resolve_existing(tok):
    if tok.startswith("-"):
        return None
    p = norm_path(tok)
    if not re.match(r'^[a-zA-Z]:/', p):
        p = root_norm + "/" + p
    if not p.lower().startswith(root_norm.lower() + "/"):
        return None
    if os.path.exists(p):
        return p
    return None


def check_segment(segment):
    if APPROVAL_MARKER in segment.lower():
        return []

    tokens = re.findall(r'"([^"]+)"|\'([^\']+)\'|(\S+)', segment)
    flat = [t[0] or t[1] or t[2] for t in tokens]
    if not flat:
        return []

    # Only recognize the watched command if it is the FIRST token of the
    # segment (i.e. the actual command being invoked, not a word appearing
    # later as an argument/string to some other command).
    cmd_name = flat[0].lower()
    if cmd_name not in WATCHED:
        return []

    args = flat[1:]

    excluded_positions = set()
    explicit_dest_flag_used = False
    for k, a in enumerate(args):
        if a.lower() in DEST_FLAGS:
            explicit_dest_flag_used = True
            if k + 1 < len(args):
                excluded_positions.add(k + 1)

    if cmd_name in DEST_CMDS and not explicit_dest_flag_used:
        positional = [k for k, a in enumerate(args) if not a.startswith("-") and k not in excluded_positions]
        if len(positional) >= 2:
            excluded_positions.add(positional[-1])

    found = []
    for k, a in enumerate(args):
        if a.startswith("-"):
            continue
        if k in excluded_positions:
            continue
        existing = resolve_existing(a)
        if existing:
            found.append(existing)
    return found


try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

command = data.get("tool_input", {}).get("command", "")
if not command:
    sys.exit(0)

segments = SEGMENT_SPLIT_RE.split(command)

flagged = []
for seg in segments:
    flagged.extend(check_segment(seg))

if flagged:
    unique = sorted(set(flagged))
    shown = unique[:5]
    suffix = "..." if len(unique) > 5 else ""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Comando bloccato: rinomina/spostamento/eliminazione di elementi gia' esistenti ("
                + ", ".join(shown) + suffix
                + ") senza approvazione esplicita. Se Giampaolo ha davvero approvato questa azione in questo turno, "
                + "ripeti il comando aggiungendo " + APPROVAL_MARKER + " in coda alla riga interessata."
            )
        }
    }))

sys.exit(0)

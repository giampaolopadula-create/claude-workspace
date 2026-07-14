import sys, json

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

questions = data.get("tool_input", {}).get("questions", [])
if isinstance(questions, list) and len(questions) > 1:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Regola: una domanda alla volta. Poni una sola domanda per chiamata, oppure, se l'utente ha esplicitamente chiesto piu' domande insieme, scrivile come testo normale invece di usare questo strumento."
        }
    }))

sys.exit(0)

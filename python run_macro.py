# run_macro.py
import os, json, requests

BASE = os.environ["RUBE_BASE"]   # 예: https://api.rube.app
AUTH = os.environ["RUBE_AUTH"]   # Composio/Rube 토큰

def call_tool(step, sid):
    args = step["args"]
    if sid:
        args = args.replace("$SID", sid)
    r = requests.post(BASE + step["path"],
                      headers={"Authorization": f"Bearer {AUTH}",
                               "Content-Type": "application/json"},
                      data=args)
    data = r.json()
    # 1단계에서 session.id 추출
    if step["name"] == "NEW_SESSION":
        sid_found = (data.get("data", {}).get("data", {}).get("session", {}) or
                     data.get("data", {}).get("session", {}) or
                     data.get("session", {})).get("id")
        if not sid_found:
            raise RuntimeError("Session ID not found")
        return data, sid_found
    return data, sid

def run(macro):
    sid = None
    for step in macro:
        data, sid = call_tool(step, sid)
        print(f"[{step['name']}] ok")
    print("DONE")

if __name__ == "__main__":
    macro = json.load(open("macro.json","r",encoding="utf-8"))
    run(macro)

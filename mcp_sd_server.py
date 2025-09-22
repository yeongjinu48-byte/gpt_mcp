import os
import sys
import json
import base64
from datetime import datetime

import requests


def _print(message: dict):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def _read():
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)


def generate_image_txt2img(
    prompt: str,
    negative_prompt: str = "",
    steps: int = 20,
    width: int = 512,
    height: int = 512,
    sampler_name: str = None,
    cfg_scale: float = 7.0,
    seed: int = -1,
    batch_size: int = 1,
    a1111_url: str = "http://127.0.0.1:7860",
    outputs_dir: str = "outputs",
):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "width": width,
        "height": height,
        "cfg_scale": cfg_scale,
        "seed": seed,
        "batch_size": batch_size,
    }
    if sampler_name:
        payload["sampler_name"] = sampler_name

    resp = requests.post(f"{a1111_url}/sdapi/v1/txt2img", json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    images_b64 = data.get("images", [])
    if not images_b64:
        raise RuntimeError("No images returned from AUTOMATIC1111")

    os.makedirs(outputs_dir, exist_ok=True)
    saved = []
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    for idx, b64img in enumerate(images_b64):
        img_bytes = base64.b64decode(b64img.split(",")[-1])
        fn = os.path.join(outputs_dir, f"txt2img_{ts}_{idx+1}.png")
        with open(fn, "wb") as f:
            f.write(img_bytes)
        saved.append(fn)
    return saved


def main():
    # Minimal MCP-like stdio protocol: list tools and call tool
    # Messages are JSON lines: {"type":"list_tools"} or {"type":"call_tool","name":"txt2img","args":{...}}
    _print({
        "type": "ready",
        "tools": [
            {
                "name": "txt2img",
                "description": "Generate image from text using AUTOMATIC1111 /sdapi/v1/txt2img",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string"},
                        "negative_prompt": {"type": "string"},
                        "steps": {"type": "integer"},
                        "width": {"type": "integer"},
                        "height": {"type": "integer"},
                        "sampler_name": {"type": ["string", "null"]},
                        "cfg_scale": {"type": "number"},
                        "seed": {"type": "integer"},
                        "batch_size": {"type": "integer"},
                        "a1111_url": {"type": "string"},
                        "outputs_dir": {"type": "string"}
                    },
                    "required": ["prompt"],
                    "additionalProperties": True
                },
            }
        ]
    })

    while True:
        msg = _read()
        if msg is None:
            break

        mtype = msg.get("type")
        if mtype == "list_tools":
            _print({"type": "tools", "tools": ["txt2img"]})
            continue

        if mtype == "call_tool":
            name = msg.get("name")
            args = msg.get("args", {})
            try:
                if name == "txt2img":
                    files = generate_image_txt2img(**args)
                    _print({"type": "tool_result", "name": name, "ok": True, "files": files})
                else:
                    _print({"type": "tool_result", "name": name, "ok": False, "error": f"Unknown tool: {name}"})
            except Exception as e:
                _print({"type": "tool_result", "name": name, "ok": False, "error": str(e)})
            continue

        if mtype == "ping":
            _print({"type": "pong"})
            continue

        if mtype in ("exit", "shutdown"):
            break


if __name__ == "__main__":
    main()


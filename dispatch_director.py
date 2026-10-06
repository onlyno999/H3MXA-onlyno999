#!/usr/bin/env python3
"""H3MXA-onlyno999 dispatcher — MiniMax H3 Director, RunningHub workflow
2084788947984666625, Node 12 (MiniMaxH3Director) only.

Hard rules baked in (empirically verified 2026-10-06, see SKILL.md):
- Reference images are written into BOTH timeline_data.global.refs AND
  segments[].refs ("double-layer"). Global-only refs are silently ignored
  by the current online version.
- instanceType is always "default" (Standard).
- The seed is always supplied explicitly and echoed in the output JSON;
  record it in the project TASK.md for every dispatch.

Prompt file format: plain text. If it contains a line "====DETAIL====",
the part before it is used as the global (subject) prompt inside
timeline_data and the part after it as the segment prompt; the FULL text
is always sent as Node 12 global_prompt. Without the marker, the whole
text serves as both.

Usage:
  dispatch_director.py run --prompt-file P --seed 20261006 --frames 240 \
      --refs openapi/aaa.png,openapi/bbb.jpg[,openapi/tail.jpg]
  dispatch_director.py query TASKID
  dispatch_director.py poll TASKID --outdir DIR [--prefix seg1]
"""
import sys, os, json, time, argparse, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request

BASE = "https://www.runninghub.cn"
WORKFLOW_ID = "2084788947984666625"
CRED = "custom.runninghub"
TASK_TYPE = "r2v — 参考主体生视频(Reference to Video)"

NEG = ("background music, bgm, score, orchestral music, subtitles, text overlay, "
       "watermark, deformed limbs, extra fingers, blurry, low quality, slow motion, "
       "speech, dialogue, singing, frozen frame")


class DispatchError(Exception):
    pass


def post(path, payload, timeout=30):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "User-Agent": "h3mxa-dispatch/1.0 (RunningHub OpenAPI v2)"},
        method="POST")
    add_surrogate_to_request(req, CRED, allowed_hosts=["www.runninghub.cn"])
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ref_objects(ref_paths):
    return [{"index": i, "imageFile": f, "fileName": "", "type": "input",
             "subfolder": ""} for i, f in enumerate(ref_paths)]


def build_timeline(subject_prompt, detail_prompt, ref_paths, frames, width, height):
    refs = ref_objects(ref_paths)
    tl = {
        "version": 5, "editMode": "segment", "totalFrames": frames, "frameRate": 24,
        "global": {
            "taskType": TASK_TYPE,
            "prompt": subject_prompt, "negativePrompt": NEG, "refs": refs,
        },
        "output": {"totalFrames": frames, "frameRate": 24,
                   "width": width, "height": height},
        "segments": [{"id": "seg_01", "start": 0, "length": frames,
                      "frameCount": frames, "durationSec": frames / 24,
                      "prompt": detail_prompt, "negativePrompt": NEG,
                      "refs": refs}],  # double-layer: same refs as global
        "continuityOverlapFrames": 22,
    }
    return json.dumps(tl, ensure_ascii=False)


def dispatch(prompt_file, seed, frames, ref_paths, width, height):
    with open(prompt_file, encoding="utf-8") as f:
        full = f.read()
    if "\n====DETAIL====\n" in full:
        subject_prompt, detail_prompt = full.split("\n====DETAIL====\n", 1)
        subject_prompt, detail_prompt = subject_prompt.strip(), detail_prompt.strip()
    else:
        subject_prompt = detail_prompt = full.strip()
    timeline = build_timeline(subject_prompt, detail_prompt, ref_paths,
                              frames, width, height)
    nodes = [
        {"nodeId": "12", "fieldName": "task_type", "fieldValue": TASK_TYPE},
        {"nodeId": "12", "fieldName": "global_prompt", "fieldValue": full.strip()},
        {"nodeId": "12", "fieldName": "seed", "fieldValue": seed},
        {"nodeId": "12", "fieldName": "frame_rate", "fieldValue": 24},
        {"nodeId": "12", "fieldName": "width", "fieldValue": width},
        {"nodeId": "12", "fieldName": "height", "fieldValue": height},
        {"nodeId": "12", "fieldName": "total_frames", "fieldValue": frames},
        {"nodeId": "12", "fieldName": "timeline_data", "fieldValue": timeline},
    ]
    r = post(f"/openapi/v2/run/workflow/{WORKFLOW_ID}",
             {"nodeInfoList": nodes, "instanceType": "default"}, timeout=60)
    ec = r.get("errorCode")
    if ec not in (None, "", 0, "0"):
        raise DispatchError(
            f"dispatch failed: errorCode={ec} errorMessage={r.get('errorMessage')}")
    tid = (r.get("data") or {}).get("taskId") or r.get("taskId")
    print(json.dumps({"taskId": tid, "seed": seed, "frames": frames}))
    return tid


def query_once(task_id):
    return post("/openapi/v2/query", {"taskId": task_id}, timeout=20)


def poll(task_id, outdir, prefix="seg", timeout_min=40):
    t0 = time.time()
    while time.time() - t0 < timeout_min * 60:
        r = query_once(task_id)
        st = r.get("status")
        if st == "SUCCESS":
            results = r.get("results") or []
            urls = [x.get("fileUrl") or x.get("url")
                    for x in results if isinstance(x, dict)]
            os.makedirs(outdir, exist_ok=True)
            saved = []
            for i, u in enumerate(urls):
                out = os.path.join(outdir, f"{prefix}_{i}.mp4" if len(urls) > 1
                                   else f"{prefix}.mp4")
                urllib.request.urlretrieve(u, out)
                saved.append(out)
            print(json.dumps({"status": "SUCCESS", "saved": saved}))
            return saved
        if st == "FAILED":
            print(json.dumps({"status": "FAILED",
                              "failedReason": r.get("failedReason")},
                             ensure_ascii=False)[:800])
            return None
        time.sleep(20)
    print(json.dumps({"status": "TIMEOUT"}))
    return None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--frames", type=int, default=240,
                   help="240=10s, 480=20s; a single segment at 720 frames OOMs")
    p.add_argument("--refs", required=True,
                   help="comma-separated openapi/ paths, in <Picture N> order; "
                        "append the previous segment's tail frame as the last "
                        "ref for tail-frame relay (it becomes <Picture 3>)")
    p.add_argument("--width", type=int, default=720)
    p.add_argument("--height", type=int, default=1280)
    q = sub.add_parser("query"); q.add_argument("taskid")
    pl = sub.add_parser("poll"); pl.add_argument("taskid")
    pl.add_argument("--outdir", required=True)
    pl.add_argument("--prefix", default="seg")
    a = ap.parse_args()
    if a.cmd == "run":
        dispatch(a.prompt_file, a.seed, a.frames,
                 [x for x in a.refs.split(",") if x], a.width, a.height)
    elif a.cmd == "query":
        print(json.dumps(query_once(a.taskid), ensure_ascii=False)[:800])
    elif a.cmd == "poll":
        poll(a.taskid, a.outdir, a.prefix)

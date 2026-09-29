#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / "patches/src/main/kotlin/app/whatsappmorphe/patches/whatsapp"

def fail(message):
    print(f"ERROR: {message}")
    raise SystemExit(1)

def load(path):
    with open(ROOT / path, encoding="utf-8") as f:
        return json.load(f)

baseline = load("compatibility/patch-baseline.json")
matrix = load("compatibility/matrix.json")
patches = load("patches-list.json")

expected_files = baseline["files"]
actual_files = sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in PATCH_DIR.glob("*.kt"))
if actual_files != sorted(expected_files):
    fail(f"Patch source set changed. expected={sorted(expected_files)} actual={actual_files}")

for rel, expected_hash in expected_files.items():
    actual_hash = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        fail(f"Patch source changed: {rel}")

candidate = matrix["candidateVersion"]
record = load(f"compatibility/{candidate}.json")
if record["version"] != candidate:
    fail("Candidate version record does not match matrix candidateVersion")
if record["packageName"] != "com.whatsapp":
    fail("Compatibility record packageName must be com.whatsapp")
if record["scope"] != "compatibility-only":
    fail("Compatibility record must remain compatibility-only")
if record["patchBehaviorChanged"] is not False:
    fail("patchBehaviorChanged must remain false")

names = {p["name"] for p in patches["patches"]}
expected_names = {
    "Anti Detector", "Anti Revoke", "Anti View Once", "Freeze Last Seen",
    "Hide Read Receipts", "Hide Typing", "Login Fix", "HD Media"
}
if names != expected_names:
    fail(f"Patch metadata set changed. expected={sorted(expected_names)} actual={sorted(names)}")

for patch in patches["patches"]:
    packages = patch.get("compatiblePackages") or []
    whatsapp = [x for x in packages if x.get("packageName") == "com.whatsapp"]
    if len(whatsapp) != 1:
        fail(f"{patch['name']}: expected exactly one com.whatsapp compatibility declaration")
    versions = {x.get("version") for x in (whatsapp[0].get("targets") or [])}
    if candidate not in versions:
        fail(f"{patch['name']}: candidate {candidate} not declared; got {sorted(versions)}")

print(f"Compatibility validation passed for {candidate}; {len(names)} patch sources remain frozen.")

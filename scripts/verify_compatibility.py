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

# Status promotion guard: compatibility states cannot be advanced without evidence.
tests = record["tests"]
status = record["status"]
requirements = {
    "build-validated": ("bundleBuild", "dexPresent", "patchMetadata"),
    "patch-validated": ("bundleBuild", "dexPresent", "patchMetadata", "patchTime"),
    "device-validated": ("bundleBuild", "dexPresent", "patchMetadata", "patchTime", "launch", "loginSession", "sendReceive", "restart"),
    "stable": ("bundleBuild", "dexPresent", "patchMetadata", "patchTime", "launch", "loginSession", "sendReceive", "restart"),
}
for key in requirements.get(status, ()):
    if tests.get(key) is not True:
        fail(f"Status {status} requires tests.{key}=true")

matrix_versions = {item["version"]: item for item in matrix.get("versions", [])}
if candidate not in matrix_versions:
    fail(f"Candidate {candidate} missing from compatibility/matrix.json")

matrix_entry = matrix_versions[candidate]
if matrix_entry.get("status") != status:
    fail(f"Matrix status {matrix_entry.get('status')} does not match record status {status}")

if matrix.get("stableVersion") is not None:
    stable_version = matrix["stableVersion"]
    if stable_version not in matrix_versions:
        fail(f"stableVersion {stable_version} missing from matrix versions")
    if matrix_versions[stable_version].get("status") != "stable":
        fail(f"stableVersion {stable_version} is not marked stable")

print(f"Status promotion guard passed: {status}")

# Toolchain lock: compatibility work must not silently change build inputs.
toolchain = load("compatibility/toolchain-lock.json")
for rel, expected_hash in toolchain["lockedFiles"].items():
    actual_hash = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        fail(f"Toolchain/build file changed outside compatibility policy: {rel}")

# Patch metadata lock: names, descriptions, defaults, dependencies and options stay frozen.
metadata_baseline = load("compatibility/patch-metadata-baseline.json")
baseline_by_name = {p["name"]: p for p in metadata_baseline["patches"]}
for patch in patches["patches"]:
    base = baseline_by_name.get(patch["name"])
    if base is None:
        fail(f"Patch metadata baseline missing: {patch['name']}")
    current = {
        "name": patch.get("name"),
        "description": patch.get("description"),
        "default": patch.get("default"),
        "category": patch.get("category"),
        "dependencies": patch.get("dependencies") or [],
        "options": patch.get("options") or [],
    }
    if current != base:
        fail(f"Patch metadata changed: {patch['name']}")

# Compatibility target declarations may change only by version support, not package identity.
constants = (ROOT / "patches/src/main/kotlin/app/whatsappmorphe/patches/shared/Constants.kt").read_text(encoding="utf-8")
if 'packageName = "com.whatsapp"' not in constants:
    fail("Constants.kt package identity changed")
if 'apkFileType = ApkFileType.APK' not in constants:
    fail("Constants.kt APK file type changed")

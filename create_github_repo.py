import os
import json
import base64
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

root = Path(r"C:\FiduWEBDocs")
os.chdir(root)

# Ensure Git repo is initialized in the copied documentation folder.
try:
    subprocess.run(["git", "init", "-b", "main"], check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as exc:
    if "already exists" not in exc.stderr.lower():
        raise

subprocess.run(["git", "config", "user.name", "Gabriel"], check=True)
subprocess.run(["git", "config", "user.email", "gabrielparravega26@gmail.com"], check=True)

# Read GitHub credential helper from the configured local Git credential store.
proc = subprocess.run(
    ["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n",
    text=True,
    capture_output=True,
    check=True,
)

username = None
token = None
for line in proc.stdout.splitlines():
    if line.startswith("username="):
        username = line.split("=", 1)[1]
    elif line.startswith("password="):
        token = line.split("=", 1)[1]

if not username or not token:
    raise RuntimeError("No GitHub credentials found in git credential fill output.")

repo_name = "FiduWEB"
repo_desc = "Documentación de arquitectura y especificaciones de negocio para FiduWEB"
payload = json.dumps({
    "name": repo_name,
    "description": repo_desc,
    "private": False,
    "has_issues": True,
    "has_wiki": True,
    "auto_init": False,
}).encode("utf-8")

auth_header = base64.b64encode(f"{username}:{token}".encode("utf-8")).decode("ascii")

request = urllib.request.Request(
    "https://api.github.com/user/repos",
    data=payload,
    method="POST",
    headers={
        "Authorization": f"Basic {auth_header}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "FiduWEB-Docs-Repo-Creator",
        "Content-Type": "application/json",
    },
)

try:
    with urllib.request.urlopen(request, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        data = json.loads(body)
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", errors="replace")
    print(body)
    raise SystemExit(f"GitHub API error: {exc.code}")

# If repository already exists, GitHub returns 422; continue if remote is already reachable.
# Otherwise create and use the clone URL for the required origin.
remote_repo = f"https://github.com/{username}/{repo_name}.git"

subprocess.run(["git", "remote", "remove", "origin"], check=False)
subprocess.run(["git", "remote", "add", "origin", remote_repo], check=True)

# Commit all files into a history for the docs folder.
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Initial import of FiduWEB documentation"], check=False)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

print("CREATED_REPO_AND_PUSHED")
print(f"REMOTE={remote_repo}")

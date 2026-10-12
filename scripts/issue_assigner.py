#!/usr/bin/env python3
"""
GitLab Issue Assigner & 1-Click Link Generator
Maps active MRs to their underlying issues and outputs 1-click self-assignment URLs.
"""

import os
import sys
import json
import ssl
import re
import urllib.request

TOKEN = os.getenv("GITLAB_TOKEN")
USERNAME = os.getenv("GITLAB_USERNAME")

if not TOKEN or not USERNAME:
    print("Error: Please set GITLAB_TOKEN and GITLAB_USERNAME environment variables.")
    print("Example: export GITLAB_TOKEN='glpat-xxx' GITLAB_USERNAME='your_username'")
    sys.exit(1)

ctx = ssl._create_unverified_context()
HEADERS = {"PRIVATE-TOKEN": TOKEN, "Content-Type": "application/json"}

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def main():
    print(f"🔗 Analyzing open MRs and mapping linked issues for @{USERNAME}...\n")
    url = f"https://gitlab.com/api/v4/merge_requests?author_username={USERNAME}&state=opened&per_page=50"
    mrs = get(url)
    
    if not isinstance(mrs, list):
        print(f"Error fetching MRs: {mrs}")
        sys.exit(1)
        
    for mr in mrs:
        pid = mr["project_id"]
        iid = mr["iid"]
        ref = mr["references"]["full"]
        title = mr["title"]
        branch = mr.get("source_branch", "")
        desc = mr.get("description", "") or ""
        
        # Get project path
        proj = get(f"https://gitlab.com/api/v4/projects/{pid}")
        project_path = proj.get("path_with_namespace", "")
        
        # Check closes_issues
        closes = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/closes_issues")
        issues = []
        if isinstance(closes, list) and closes:
            for c in closes:
                assignees = [a["username"] for a in c.get("assignees", [])]
                issues.append((c["iid"], c["title"], assignees))
        else:
            # Extract from branch or description
            cand_iids = list(dict.fromkeys(re.findall(r"(\d{4,7})", branch) + re.findall(r"#(\d+)", desc)))
            for cand in cand_iids:
                iss = get(f"https://gitlab.com/api/v4/projects/{pid}/issues/{cand}")
                if isinstance(iss, dict) and "iid" in iss:
                    assignees = [a["username"] for a in iss.get("assignees", [])]
                    issues.append((iss["iid"], iss["title"], assignees))
                    
        print(f"📌 MR: [{ref}] {title[:60]}")
        if not issues:
            print("   ℹ️ No linked issue detected in description or branch name.")
        for iss_id, iss_title, assignees in issues:
            is_assigned = USERNAME in assignees
            badge = "✅ ASSIGNED TO YOU" if is_assigned else f"⚠️ UNASSIGNED (Current: {assignees})"
            manage_url = f"https://contributors.gitlab.com/manage-issue?projectPath={project_path}&issueIid={iss_id}&action=work"
            print(f"   Issue #{iss_id}: {iss_title[:50]} [{badge}]")
            if not is_assigned:
                print(f"   👉 1-Click Self-Assign: {manage_url}")
        print("-" * 80)

if __name__ == "__main__":
    main()

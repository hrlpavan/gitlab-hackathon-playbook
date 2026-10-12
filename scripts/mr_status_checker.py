#!/usr/bin/env python3
"""
GitLab MR Status Checker & Pipeline Monitor
Monitors active hackathon MRs, pipelines, approvals, and blocking discussions.
"""

import os
import sys
import json
import ssl
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
    print(f"🔍 Fetching active Merge Requests for user: @{USERNAME}...")
    url = f"https://gitlab.com/api/v4/merge_requests?author_username={USERNAME}&state=opened&per_page=50"
    mrs = get(url)
    
    if not isinstance(mrs, list):
        print(f"Error fetching MRs: {mrs}")
        sys.exit(1)
        
    print(f"\nFound {len(mrs)} open Merge Requests:\n" + "="*80)
    
    for mr in mrs:
        pid = mr["project_id"]
        iid = mr["iid"]
        ref = mr["references"]["full"]
        title = mr["title"]
        status = mr.get("detailed_merge_status", "unknown")
        
        # Pipeline status
        pipe = mr.get("head_pipeline")
        pipe_status = pipe.get("status") if pipe else "no pipeline"
        
        # Approvals
        appr_data = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/approvals")
        approved_by = [a["user"]["username"] for a in appr_data.get("approved_by", [])]
        
        # Unresolved discussions
        disc_data = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/discussions")
        unresolved = 0
        if isinstance(disc_data, list):
            for d in disc_data:
                notes = d.get("notes", [])
                if any(n.get("resolvable") and not n.get("resolved") for n in notes):
                    unresolved += 1
                    
        # Formatting status icons
        pipe_icon = "🟢" if pipe_status == "success" else ("🟡" if pipe_status == "running" else "🔴")
        status_icon = "🚀" if status == "mergeable" else "⏳"
        
        print(f"{status_icon} [{ref}] {title[:60]}")
        print(f"   Pipeline: {pipe_icon} {pipe_status} | Merge Status: {status}")
        print(f"   Approvals: {', '.join(approved_by) if approved_by else 'None'} | Unresolved Threads: {unresolved}")
        print("-" * 80)

if __name__ == "__main__":
    main()

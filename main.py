
import argparse
import json
from config import Config
from core.github_client import GitHubClient
from agents import AnalyzeAgent, SummaryAgent, ReviewAgent

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent PR Assistant")
    parser.add_argument("--repo", required=True, help="Format: owner/repo, e.g., octocat/Hello-World")
    parser.add_argument("--pr", type=int, required=True, help="PR number")
    parser.add_argument("--dry-run", action="store_true", help="Only print, do not post comment to GitHub")
    args = parser.parse_args()

    owner, repo = args.repo.split("/")

    # 1. Fetch diff
    gh = GitHubClient()
    print(f"[1/5] Fetching diff for PR #{args.pr} from {owner}/{repo} ...")
    try:
        diff_text = gh.get_pr_diff(owner, repo, args.pr)
    except Exception as e:
        print(f" Failed to fetch diff: {e}")
        return
    if not diff_text.strip():
        print(" No diff content found.")
        return

    # 2. Long-chain reasoning: analyze diff (AnalyzeAgent)
    print("[2/5] Running AnalyzeAgent (long-chain reasoning) ...")
    analyzer = AnalyzeAgent()
    analysis = analyzer.run(diff_text)
    print(f" Analysis result:\n{json.dumps(analysis, indent=2)}")

    # 3. Multi-Agent collaboration: run SummaryAgent and ReviewAgent in parallel (simulated sequentially)
    print("[3/5] Running SummaryAgent ...")
    summarizer = SummaryAgent()
    summary = summarizer.run(analysis)
    print(f" Summary:\n{summary}")

    print("[4/5] Running ReviewAgent ...")
    reviewer = ReviewAgent()
    review = reviewer.run(diff_text, analysis)
    print(f" Review:\n{review}")

    # 4. Aggregate results
    final_comment = f"""##  Multi-Agent PR Assistant (Backend: {Config.LLM_BACKEND})

###  Structure Analysis
```json
{json.dumps(analysis, indent=2)}

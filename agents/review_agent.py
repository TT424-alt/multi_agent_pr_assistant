from core.llm_client import LLMClient

SYSTEM_PROMPT = """You are a strict code reviewer. Based on the diff below and the analysis results, check for potential issues:
- Security vulnerabilities (e.g., SQL injection, hardcoded passwords)
- Performance issues (e.g., N+1 queries, O(n^2) loops)
- Readability/style (e.g., PEP8 violations, missing comments)
- Logic errors (e.g., off-by-one, null pointer risks)

Output format:
### Critical issues
- ...
### Warnings
- ...
### Suggestions
- ...

For each issue, specify the file name if possible.
"""

class ReviewAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, diff_text: str, analysis: dict) -> str:
        import json
        user_prompt = f"""Diff content:
{diff_text}

Analysis results:
{json.dumps(analysis, indent=2)}

Please provide the review report.
"""
        return self.llm.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )

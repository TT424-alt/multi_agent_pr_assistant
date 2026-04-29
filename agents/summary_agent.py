from core.llm_client import LLMClient

SYSTEM_PROMPT = """You are a technical documentation expert. Based on the provided code change analysis, generate a clear and professional PR summary.
Summary format:
- One sentence describing the purpose of the PR (inferred)
- Main changes (list)
- Impact on downstream (if any)
- Suggested testing scope

Output in Markdown, no more than 500 words.
"""

class SummaryAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, analysis: dict) -> str:
        import json
        user_prompt = f"Generate a PR summary based on the following analysis results:\n{json.dumps(analysis, indent=2)}"
        return self.llm.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

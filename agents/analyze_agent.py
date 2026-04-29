import json
from core.llm_client import LLMClient

SYSTEM_PROMPT = """You are a code analysis expert. Given a PR diff text, you need to:
- Extract all changed file paths
- List modified functions/classes in each file (if context is available in the diff)
- Count added and deleted lines
- Mark "potentially affected other modules" (inferred based on imports or call relationships)

Output format as JSON, for example:
{
  "files": [{"path": "...", "functions": ["func1"], "add_lines": 10, "del_lines": 2}],
  "total_add": 100,
  "total_del": 20,
  "affected_modules": ["module_a", "module_b"]
}
"""

class AnalyzeAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, diff_text: str) -> dict:
        user_prompt = f"Please analyze the following PR diff:\n\n{diff_text}"
        response = self.llm.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        # Extract JSON
        try:
            return json.loads(response)
        except:
            # Fallback empty structure
            return {"files": [], "total_add": 0, "total_del": 0, "affected_modules": []}

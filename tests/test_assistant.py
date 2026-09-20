import unittest
from unittest.mock import patch

from kachysec.assistant import AssistantContext, build_prompt, render_response


class AssistantTests(unittest.TestCase):
    def test_prompt_contains_scope_boundary(self) -> None:
        context = AssistantContext("status", "audit", "tools")
        prompt = build_prompt("How do I inspect my lab?", context)
        self.assertIn("explicitly authorized offensive security", prompt)
        self.assertIn("Do not execute commands yourself", prompt)
        self.assertIn("How do I inspect my lab?", prompt)

    def test_render_response(self) -> None:
        from kachysec.assistant import AssistantResponse

        rendered = render_response(AssistantResponse("test", "hello"))
        self.assertIn("KachySec Assistant [test]", rendered)
        self.assertIn("hello", rendered)

    @patch("kachysec.assistant.shutil.which", return_value=None)
    def test_ollama_is_optional(self, _which) -> None:
        from kachysec.assistant import ollama_available

        self.assertFalse(ollama_available())


if __name__ == "__main__":
    unittest.main()

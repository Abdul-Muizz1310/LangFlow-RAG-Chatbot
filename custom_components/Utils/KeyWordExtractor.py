from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message
import json

class KeywordExtractorComponent(Component):
    display_name = "Keyword Extractor"
    description = "Extracts keywords and question from input JSON."
    icon = "type"
    name = "KeywordExtractor"

    documentation: str = "https://docs.langflow.org/components-custom-components"

    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="Input JSON",
            info="Provide a JSON with 'Keywords' (a list of strings) and 'Question' (a string).",
            value='{"Keywords": ["banking", "2021", "Pakistan"], "Question": "How did the banking sector perform in 2021?"}',
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Extracted Keywords", name="keywords_output", method="get_keywords"),
        Output(display_name="User Question", name="question_output", method="get_question"),
    ]

    def get_question(self) -> Message:
        parsed = self.parse_input(self.input_value)
        question = parsed.get("Question", "")
        self.status = question
        return Message(text=question)

    def get_keywords(self) -> Message:
        parsed = self.parse_input(self.input_value)
        keywords = parsed.get("Keywords", [])
        if isinstance(keywords, list):
            result = ", ".join(map(str, keywords))
        else:
            result = "Invalid format for 'Keywords'"
        self.status = result
        return Message(text=result)

    def parse_input(self, input_str: str):
        try:
            return json.loads(input_str)
        except json.JSONDecodeError:
            return {"Keywords": [], "Question": ""}

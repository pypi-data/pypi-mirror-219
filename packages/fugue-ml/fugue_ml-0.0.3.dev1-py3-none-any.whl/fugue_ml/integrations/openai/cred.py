from typing import Any, Dict

import openai


class OpenAICredentialObject:
    def __init__(self):
        self.extract()

    def extract(self) -> None:
        self.api_key = openai.api_key
        self.api_type = openai.api_type
        self.api_base = openai.api_base
        self.api_version = openai.api_version
        self.api_key_path = openai.api_key_path
        self.organization = openai.organization

    def apply(self) -> None:
        openai.api_key = self.api_key
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        openai.api_key_path = self.api_key_path
        openai.organization = self.organization

    def __getstate__(self) -> Dict[str, Any]:
        self.extract()
        return self.__dict__

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self.apply()

from functools import lru_cache
from typing import List

class APIKeyManager:
    def __init__(self, api_keys: List[str]):
        if not api_keys:
            raise ValueError("No API keys provided")
        self.api_keys = api_keys
        self.current_index = 0

    def get_next_key(self) -> str:
        key = self.api_keys[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.api_keys)
        return key

@lru_cache(maxsize=100)
def cached_api_call(query: str):
    # Your API call logic here
    pass
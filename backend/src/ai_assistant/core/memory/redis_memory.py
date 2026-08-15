import json

import redis

from .base_memory import BaseMemory


class RedisMemory(BaseMemory):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        ttl: int = 3600,
        key: str = "conversation",
        client: redis.Redis | None = None,
    ):
        self.client = (
            client
            if client is not None
            else redis.Redis(
                host=host,
                port=port,
                decode_responses=True,
            )
        )

        self.ttl = ttl
        self.key = key
        
        self._summary_key = f"{key}:summary"


    def get_history(self) -> list[dict[str, str]]:
        data = self.client.get(self.key)

        if data is None:
            return []

        return json.loads(data)


    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        history = self.get_history()

        history.append(
            {
                "role": role,
                "content": content,
            }
        )

        self.client.set(
            self.key,
            json.dumps(history),
            ex=self.ttl,
        )


    def replace_history(
        self,
        history: list[dict[str, str]],
        ) -> None:
        
        self.client.set(
            self.key,
            json.dumps(history),
            ex=self.ttl,
        )
        
    def get_summary(
        self,
        ) -> str | None:

        data = self.client.get(
            self._summary_key,
        )

        if data is None:
            return None

        if isinstance(data, bytes):
            return data.decode("utf-8")

        return data


    def save_summary(
        self,
        summary: str,
    ) -> None:

        self.client.set(
            self._summary_key,
            summary,
            ex=self.ttl,
        )
"""
Reusable AI service wrapper for OpenAI API interactions.

Provides a centralized interface with retry logic, error handling,
and JSON extraction for all AI-powered features.
"""

from __future__ import annotations

import json
import time
from typing import Any, Optional

from openai import OpenAI, APIError, RateLimitError, APIConnectionError

from app.config import (
    openai_client,
    AI_MODEL,
    AI_TEMPERATURE_LOW,
    MAX_RETRIES,
)
from app.utils.helpers import extract_json_from_response


class AIService:
    """
    Centralized AI service for all OpenAI interactions.
    
    Features:
    - Retry logic with exponential backoff
    - Structured JSON extraction
    - Temperature control per use-case
    - Token usage optimization
    """

    def __init__(self, client: Optional[OpenAI] = None):
        self.client = client or openai_client

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = AI_TEMPERATURE_LOW,
        max_tokens: int = 2000,
        json_mode: bool = True,
    ) -> str:
        """
        Send a chat completion request to OpenAI.
        
        Args:
            system_prompt: System instruction for the model
            user_prompt: User message / content to process
            temperature: Creativity control (0.0 - 1.0)
            max_tokens: Maximum response length
            json_mode: Whether to request JSON response format
            
        Returns:
            Raw response text from the model
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        kwargs: dict[str, Any] = {
            "model": AI_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        last_error: Optional[Exception] = None

        for attempt in range(MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(**kwargs)
                content = response.choices[0].message.content
                if content is None:
                    raise ValueError("Empty response from AI model")
                return content.strip()

            except RateLimitError as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    wait_time = 2 ** (attempt + 1)
                    time.sleep(wait_time)
                continue

            except (APIError, APIConnectionError) as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    time.sleep(1)
                continue

        raise RuntimeError(
            f"AI service failed after {MAX_RETRIES + 1} attempts: {last_error}"
        )

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = AI_TEMPERATURE_LOW,
        max_tokens: int = 2000,
    ) -> dict[str, Any]:
        """
        Generate and parse a JSON response from the AI model.
        
        Includes fallback JSON extraction for responses that contain
        markdown fences or surrounding text.
        """
        raw = self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=True,
        )
        return extract_json_from_response(raw)


# Module-level singleton
ai_service = AIService()

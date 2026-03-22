"""Configuration settings for the Up Bank SDK."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for the Up Bank API client."""

    base_url: str = "https://api.up.com.au/api/v1"
    timeout: float = 30.0
    max_retries: int = 3
    retry_wait_multiplier: float = 1.0
    retry_wait_min: float = 2.0
    retry_wait_max: float = 30.0

    def __post_init__(self) -> None:
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_wait_multiplier <= 0:
            raise ValueError("retry_wait_multiplier must be positive")
        if self.retry_wait_min <= 0:
            raise ValueError("retry_wait_min must be positive")
        if self.retry_wait_max <= 0:
            raise ValueError("retry_wait_max must be positive")
        if self.retry_wait_min > self.retry_wait_max:
            raise ValueError("retry_wait_min must not exceed retry_wait_max")

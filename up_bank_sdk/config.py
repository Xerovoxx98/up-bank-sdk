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

"""Tests for the Up Bank SDK config."""

from __future__ import annotations

import pytest

from up_bank_sdk.config import Config


class TestConfig:
    """Tests for Config dataclass."""

    def test_defaults(self) -> None:
        """Test default configuration values."""
        config = Config()
        assert config.base_url == "https://api.up.com.au/api/v1"
        assert config.timeout == 30.0
        assert config.max_retries == 3
        assert config.retry_wait_multiplier == 1.0
        assert config.retry_wait_min == 2.0
        assert config.retry_wait_max == 30.0

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = Config(
            base_url="https://custom.api.com/v1",
            timeout=60.0,
            max_retries=5,
        )
        assert config.base_url == "https://custom.api.com/v1"
        assert config.timeout == 60.0
        assert config.max_retries == 5
        assert config.retry_wait_min == 2.0

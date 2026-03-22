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


class TestConfigValidation:
    """Tests for Config validation."""

    def test_negative_timeout_raises(self) -> None:
        """Test that negative timeout raises ValueError."""
        with pytest.raises(ValueError, match="timeout must be positive"):
            Config(timeout=-1.0)

    def test_zero_timeout_raises(self) -> None:
        """Test that zero timeout raises ValueError."""
        with pytest.raises(ValueError, match="timeout must be positive"):
            Config(timeout=0.0)

    def test_negative_max_retries_raises(self) -> None:
        """Test that negative max_retries raises ValueError."""
        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            Config(max_retries=-1)

    def test_negative_retry_wait_multiplier_raises(self) -> None:
        """Test that negative retry_wait_multiplier raises ValueError."""
        with pytest.raises(ValueError, match="retry_wait_multiplier must be positive"):
            Config(retry_wait_multiplier=-1.0)

    def test_negative_retry_wait_min_raises(self) -> None:
        """Test that negative retry_wait_min raises ValueError."""
        with pytest.raises(ValueError, match="retry_wait_min must be positive"):
            Config(retry_wait_min=-1.0)

    def test_negative_retry_wait_max_raises(self) -> None:
        """Test that negative retry_wait_max raises ValueError."""
        with pytest.raises(ValueError, match="retry_wait_max must be positive"):
            Config(retry_wait_max=-1.0)

    def test_retry_wait_min_exceeds_max_raises(self) -> None:
        """Test that retry_wait_min > retry_wait_max raises ValueError."""
        with pytest.raises(ValueError, match="retry_wait_min must not exceed retry_wait_max"):
            Config(retry_wait_min=10.0, retry_wait_max=5.0)

    def test_retry_wait_min_equals_max_ok(self) -> None:
        """Test that retry_wait_min == retry_wait_max is valid."""
        config = Config(retry_wait_min=5.0, retry_wait_max=5.0)
        assert config.retry_wait_min == config.retry_wait_max

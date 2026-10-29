
import pytest

from app.clients.deepseek import DeepSeekClient


def test_missing_api_key_raises_error(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    with pytest.raises(
        ValueError,
        match="DEEPSEEK_API_KEY is not configured",
    ):
        DeepSeekClient()

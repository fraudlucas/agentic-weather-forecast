from agentic_weather_forecast.core.settings import Settings, env_settings
from pytest import MonkeyPatch


class TestSettings:
    def test_loads_from_env_file(self):
        s = Settings()
        assert s.gemini_api_key != ""

    def test_env_var_overrides_env_file(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
        s = Settings()
        assert s.gemini_api_key == "test-key-123"

    def test_default_empty_when_no_env_source(self, monkeypatch: MonkeyPatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        s = Settings(_env_file=None)
        assert s.gemini_api_key == ""

    def test_env_settings_is_singleton(self):
        assert isinstance(env_settings, Settings)

    def test_model_config_includes_env_file(self):
        assert Settings.model_config["env_file"] == ".env"
        assert Settings.model_config["env_file_encoding"] == "utf-8"

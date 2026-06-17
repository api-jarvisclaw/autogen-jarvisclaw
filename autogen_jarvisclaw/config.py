"""JarvisClaw config helpers for AutoGen (AG2).

AutoGen uses OpenAI-compatible config_list format. Since JarvisClaw is
OpenAI-compatible, integration is just a config helper — no custom client needed.

For x402 wallet payments, we provide a custom model client that handles
the 402 → sign → retry flow automatically.
"""

from __future__ import annotations

from typing import Optional

import httpx


def jarvisclaw_config(
    model: str = "gpt-5.4",
    api_key: str = "sk-...",
    base_url: str = "https://api.jarvisclaw.ai/v1",
    temperature: float = 0.7,
    **kwargs,
) -> dict:
    """Create a single AutoGen LLM config for JarvisClaw.

    Args:
        model: Model name (e.g., "gpt-5.4", "anthropic/claude-sonnet-4.6")
        api_key: JarvisClaw API key
        base_url: API base URL
        temperature: Sampling temperature

    Returns:
        Config dict compatible with AutoGen's llm_config format.

    Example:
        ```python
        from autogen import ConversableAgent
        from autogen_jarvisclaw import jarvisclaw_config

        config = jarvisclaw_config(model="gpt-5.4", api_key="sk-...")

        agent = ConversableAgent(
            name="assistant",
            llm_config={"config_list": [config]},
        )
        ```
    """
    config = {
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
        "temperature": temperature,
        **kwargs,
    }
    return config


def jarvisclaw_config_list(
    models: Optional[list[str]] = None,
    api_key: str = "sk-...",
    base_url: str = "https://api.jarvisclaw.ai/v1",
    **kwargs,
) -> list[dict]:
    """Create an AutoGen config_list with multiple JarvisClaw models.

    AutoGen tries models in order, falling back if one fails.
    This creates a config_list with multiple models for resilience.

    Args:
        models: List of model names. Defaults to a sensible mix.
        api_key: JarvisClaw API key
        base_url: API base URL

    Returns:
        List of config dicts for AutoGen's llm_config.

    Example:
        ```python
        from autogen import ConversableAgent
        from autogen_jarvisclaw import jarvisclaw_config_list

        configs = jarvisclaw_config_list(
            models=["gpt-5.4", "anthropic/claude-sonnet-4.6", "deepseek/deepseek-chat"],
            api_key="sk-...",
        )

        agent = ConversableAgent(
            name="assistant",
            llm_config={"config_list": configs},
        )
        ```
    """
    if models is None:
        models = ["gpt-5.4", "anthropic/claude-sonnet-4.6", "deepseek/deepseek-chat"]

    return [
        jarvisclaw_config(model=m, api_key=api_key, base_url=base_url, **kwargs)
        for m in models
    ]


def list_models(base_url: str = "https://api.jarvisclaw.ai") -> list[dict]:
    """List available models with pricing (no auth required)."""
    response = httpx.get(f"{base_url}/api/discovery/models", timeout=10.0)
    response.raise_for_status()
    return response.json().get("data", [])


def free_models(base_url: str = "https://api.jarvisclaw.ai") -> dict:
    """Get free and cheap models (no auth required)."""
    response = httpx.get(f"{base_url}/api/discovery/free-models", timeout=10.0)
    response.raise_for_status()
    return response.json()

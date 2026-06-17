# autogen-jarvisclaw

AutoGen (AG2) integration for [JarvisClaw](https://jarvisclaw.ai) AI API — 40+ models, pay with USDC.

## Install

```bash
pip install autogen-jarvisclaw
```

## Usage

### Quick Start

```python
from autogen import ConversableAgent
from autogen_jarvisclaw import jarvisclaw_config

assistant = ConversableAgent(
    name="assistant",
    system_message="You are a helpful AI assistant.",
    llm_config={"config_list": [jarvisclaw_config(model="gpt-5.4", api_key="sk-...")]},
)

user = ConversableAgent(
    name="user",
    human_input_mode="NEVER",
    llm_config=False,
)

user.initiate_chat(assistant, message="What's the capital of France?")
```

### Multi-Model Fallback

AutoGen tries models in order. Use multiple JarvisClaw models for resilience:

```python
from autogen_jarvisclaw import jarvisclaw_config_list

configs = jarvisclaw_config_list(
    models=["gpt-5.4", "anthropic/claude-sonnet-4.6", "deepseek/deepseek-chat"],
    api_key="sk-...",
)

assistant = ConversableAgent(
    name="assistant",
    llm_config={"config_list": configs},
)
```

### Alternative: Direct Config (no extra package)

Since JarvisClaw is OpenAI-compatible, you can configure directly:

```python
config_list = [{
    "model": "gpt-5.4",
    "api_key": "sk-...",
    "base_url": "https://api.jarvisclaw.ai/v1",
}]

assistant = ConversableAgent(
    name="assistant",
    llm_config={"config_list": config_list},
)
```

### Multi-Agent Conversation

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen_jarvisclaw import jarvisclaw_config

config = {"config_list": [jarvisclaw_config(model="gpt-5.4", api_key="sk-...")]}

researcher = ConversableAgent(name="researcher", system_message="Research topics thoroughly.", llm_config=config)
writer = ConversableAgent(name="writer", system_message="Write clear summaries.", llm_config=config)
critic = ConversableAgent(name="critic", system_message="Review for accuracy.", llm_config=config)

group_chat = GroupChat(agents=[researcher, writer, critic], messages=[], max_round=6)
manager = GroupChatManager(groupchat=group_chat, llm_config=config)

researcher.initiate_chat(manager, message="Research quantum computing breakthroughs in 2026")
```

### Discover Models

```python
from autogen_jarvisclaw import jarvisclaw_config_list
from autogen_jarvisclaw.config import list_models, free_models

# Browse available models (no auth)
all_models = list_models()
cheap = free_models()
```

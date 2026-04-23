from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Any

# Agent import first - needed to resolve circular dependency chain
# (agent -> tool -> security -> event -> critic -> tool.builtins -> tool)
from openhands.sdk.agent import Agent, AgentBase

# LLM types needed by event.base and security.analyzer
from openhands.sdk.llm.message import (
    ImageContent,
    Message,
    TextContent,
)

# Keep critical-path imports first to establish the right initialization order
# for modules with circular dependencies
from openhands.sdk.logger import get_logger

# Tool imports after the chain is initialized
from openhands.sdk.tool import (
    Action,
    Observation,
    Tool,
    ToolDefinition,
    list_registered_tools,
    register_tool,
    resolve_tool,
)


try:
    __version__ = version("openhands-sdk")
except PackageNotFoundError:
    __version__ = "0.0.0"  # fallback for editable/unbuilt environments

# Print startup banner early - before loading remaining heavy modules
from openhands.sdk.banner import _print_banner


_print_banner(__version__)


# ============================================================================
# Lazy imports: modules deferred until first use
# ============================================================================
# These modules can be lazy-loaded because they don't have circular dependencies
# or can load their expensive dependencies lazily.

_LAZY_IMPORTS: dict[str, set[str]] = {
    # LLM - expensive due to litellm (~2s), but can be lazy since we already have types
    "openhands.sdk.llm": {
        "LLM",
        "FallbackStrategy",
        "LLMProfileStore",
        "LLMRegistry",
        "LLMStreamChunk",
        "RedactedThinkingBlock",
        "RegistryEvent",
        "ThinkingBlock",
        "TokenCallbackType",
        "TokenUsage",
    },
    # Conversation - expensive due to acp (~200ms)
    "openhands.sdk.conversation": {
        "BaseConversation",
        "Conversation",
        "ConversationCallbackType",
        "ConversationExecutionStatus",
        "LocalConversation",
        "RemoteConversation",
    },
    "openhands.sdk.conversation.conversation_stats": {"ConversationStats"},
    # MCP - expensive due to fastmcp (~220ms)
    "openhands.sdk.mcp": {
        "MCPClient",
        "MCPToolDefinition",
        "MCPToolObservation",
        "create_mcp_tools",
    },
    # Observability - expensive due to lmnr (~213ms)
    "openhands.sdk.observability.laminar": {
        "init_laminar_for_external",
        "maybe_init_laminar",
        "observe",
    },
    # Settings - no major heavy deps
    "openhands.sdk.settings": {
        "ACPAgentSettings",
        "AgentSettings",
        "AgentSettingsConfig",
        "CondenserSettings",
        "ConversationSettings",
        "LLMAgentSettings",
        "SettingsChoice",
        "SettingsFieldSchema",
        "SettingsSchema",
        "SettingsSectionSchema",
        "VerificationSettings",
        "default_agent_settings",
        "export_agent_settings_schema",
        "export_settings_schema",
        "validate_agent_settings",
    },
    "openhands.sdk.settings.metadata": {
        "SettingProminence",
        "SettingsFieldMetadata",
        "SettingsSectionMetadata",
        "field_meta",
    },
    # Subagent
    "openhands.sdk.subagent": {
        "agent_definition_to_factory",
        "load_agents_from_dir",
        "load_project_agents",
        "load_user_agents",
        "register_agent",
    },
    # Plugin
    "openhands.sdk.plugin": {"Plugin"},
    # Skills
    "openhands.sdk.skills": {
        "load_project_skills",
        "load_skills_from_dir",
        "load_user_skills",
    },
    # Utils
    "openhands.sdk.utils": {"page_iterator"},
    # Context
    "openhands.sdk.context": {"AgentContext"},
    "openhands.sdk.context.condenser": {"LLMSummarizingCondenser"},
    # Event
    "openhands.sdk.event": {
        "Event",
        "HookExecutionEvent",
        "LLMConvertibleEvent",
    },
    "openhands.sdk.event.llm_convertible": {"MessageEvent"},
    # IO
    "openhands.sdk.io": {"FileStore", "LocalFileStore"},
    # Workspace
    "openhands.sdk.workspace": {
        "AsyncRemoteWorkspace",
        "LocalWorkspace",
        "RemoteWorkspace",
        "Workspace",
    },
}


def __getattr__(name: str) -> Any:
    """Lazy import support for heavy SDK modules."""
    for module_path, exports in _LAZY_IMPORTS.items():
        if name in exports:
            from importlib import import_module

            module = import_module(module_path)
            obj = getattr(module, name)
            # Cache in this module to avoid repeated lookups
            globals()[name] = obj
            return obj
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "LLM",
    "LLMRegistry",
    "LLMProfileStore",
    "LLMStreamChunk",
    "FallbackStrategy",
    "TokenCallbackType",
    "TokenUsage",
    "ConversationStats",
    "RegistryEvent",
    "Message",
    "TextContent",
    "ImageContent",
    "ThinkingBlock",
    "RedactedThinkingBlock",
    "Tool",
    "ToolDefinition",
    "AgentBase",
    "Agent",
    "Action",
    "Observation",
    "MCPClient",
    "MCPToolDefinition",
    "MCPToolObservation",
    "MessageEvent",
    "HookExecutionEvent",
    "create_mcp_tools",
    "get_logger",
    "Conversation",
    "BaseConversation",
    "LocalConversation",
    "RemoteConversation",
    "ConversationExecutionStatus",
    "ConversationCallbackType",
    "Event",
    "LLMConvertibleEvent",
    "AgentContext",
    "LLMSummarizingCondenser",
    "CondenserSettings",
    "ConversationSettings",
    "VerificationSettings",
    "ACPAgentSettings",
    "AgentSettings",
    "AgentSettingsConfig",
    "LLMAgentSettings",
    "default_agent_settings",
    "export_agent_settings_schema",
    "validate_agent_settings",
    "SettingsChoice",
    "SettingProminence",
    "SettingsFieldMetadata",
    "SettingsFieldSchema",
    "SettingsSchema",
    "SettingsSectionMetadata",
    "SettingsSectionSchema",
    "export_settings_schema",
    "field_meta",
    "FileStore",
    "LocalFileStore",
    "Plugin",
    "register_tool",
    "resolve_tool",
    "list_registered_tools",
    "Workspace",
    "LocalWorkspace",
    "RemoteWorkspace",
    "AsyncRemoteWorkspace",
    "register_agent",
    "load_project_agents",
    "load_user_agents",
    "load_agents_from_dir",
    "agent_definition_to_factory",
    "load_project_skills",
    "load_skills_from_dir",
    "load_user_skills",
    "page_iterator",
    "__version__",
]

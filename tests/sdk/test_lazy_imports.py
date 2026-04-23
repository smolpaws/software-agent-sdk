"""Tests for SDK lazy import functionality.

These tests verify that the SDK's lazy import mechanism works correctly
and doesn't break the public API.
"""

from __future__ import annotations


def test_lazy_imports_module_exists():
    """Test that the SDK can be imported without errors."""
    import openhands.sdk as sdk

    assert sdk is not None


def test_lazy_imports_version():
    """Test that __version__ is available."""
    import openhands.sdk as sdk

    assert sdk.__version__ is not None
    assert isinstance(sdk.__version__, str)


def test_lazy_imports_get_logger():
    """Test that get_logger is available."""
    import openhands.sdk as sdk

    logger = sdk.get_logger("test")
    assert logger is not None


def test_lazy_imports_eager_types():
    """Test that eagerly imported types are available immediately."""
    import openhands.sdk as sdk

    # These are imported eagerly due to circular dependencies
    assert sdk.Agent is not None
    assert sdk.AgentBase is not None
    assert sdk.Tool is not None
    assert sdk.Action is not None
    assert sdk.Observation is not None


def test_lazy_imports_lazy_types():
    """Test that lazy-imported types are available via __getattr__."""
    import openhands.sdk as sdk

    # These should be lazy-loaded
    assert sdk.Conversation is not None
    assert sdk.MCPClient is not None
    assert sdk.LLM is not None


def test_lazy_imports_context():
    """Test that context types are lazy-loaded."""
    import openhands.sdk as sdk

    assert sdk.AgentContext is not None
    assert sdk.LLMSummarizingCondenser is not None


def test_lazy_imports_event():
    """Test that event types are lazy-loaded."""
    import openhands.sdk as sdk

    assert sdk.Event is not None
    assert sdk.MessageEvent is not None


def test_lazy_imports_workspace():
    """Test that workspace types are lazy-loaded."""
    import openhands.sdk as sdk

    assert sdk.Workspace is not None
    assert sdk.LocalWorkspace is not None


def test_lazy_imports_settings():
    """Test that settings types are lazy-loaded."""
    import openhands.sdk as sdk

    assert sdk.AgentSettings is not None
    assert sdk.ConversationSettings is not None


def test_lazy_imports_tool_functions():
    """Test that tool registration functions are available."""
    import openhands.sdk as sdk

    assert callable(sdk.register_tool)
    assert callable(sdk.list_registered_tools)
    assert callable(sdk.resolve_tool)


def test_lazy_imports_all_exports():
    """Test that all expected exports are in __all__."""
    import openhands.sdk as sdk

    # Only eager imports should be in __all__
    expected_eager = [
        "Agent",
        "AgentBase",
        "Tool",
        "get_logger",
        "__version__",
    ]

    for name in expected_eager:
        assert name in sdk.__all__, f"{name} should be in __all__"


def test_lazy_imports_routerllm_deferred():
    """Test that RouterLLM is deferred from LLM module to break circular import."""
    # Import just the llm module
    from openhands.sdk.llm import LLM, RouterLLM

    # LLM should be available
    assert LLM is not None

    # RouterLLM should also work (it's lazily imported)
    assert RouterLLM is not None

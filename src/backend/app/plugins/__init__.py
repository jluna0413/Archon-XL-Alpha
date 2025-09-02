from abc import ABC, abstractmethod
from typing import Any, Dict

class PluginBase(ABC):
    """Base class that all Archon plugins must implement.

    Implementations should handle configuration, lifecycle (start/stop), and expose tools.
    """

    def __init__(self, plugin_id: str, config: Dict[str, Any] | None = None):
        self.plugin_id = plugin_id
        self.config = config or {}

    @abstractmethod
    def start(self) -> None:
        """Start any background processes or connections."""
        raise NotImplementedError()

    @abstractmethod
    def stop(self) -> None:
        """Stop and cleanup resources."""
        raise NotImplementedError()

    @abstractmethod
    def tools(self) -> Dict[str, Any]:
        """Return a mapping of tool-name -> callable/metadata."""
        raise NotImplementedError()

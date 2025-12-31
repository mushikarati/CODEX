"""
Engine Registry and Factory.

Provides automatic discovery and instantiation of compression engines.
Makes it easy to add new engines without modifying core code.
"""

from typing import Dict, Type, Optional, List, Any
from .engines.base import CompressionEngine


class EngineRegistry:
    """
    Central registry for compression engines.

    Engines register themselves and can be instantiated by name.
    Supports automatic discovery and plugin-style architecture.
    """

    _engines: Dict[str, Type[CompressionEngine]] = {}

    @classmethod
    def register(cls, engine_class: Type[CompressionEngine]) -> None:
        """
        Register a compression engine.

        Args:
            engine_class: CompressionEngine subclass to register

        Raises:
            ValueError: If engine name is already registered
        """
        # Instantiate temporarily to get the name
        temp_instance = engine_class()
        engine_name = temp_instance.name.lower()

        if engine_name in cls._engines:
            raise ValueError(f"Engine '{engine_name}' is already registered")

        cls._engines[engine_name] = engine_class
        print(f"Registered compression engine: {temp_instance.name} v{temp_instance.version}")

    @classmethod
    def get_engine(cls, name: str, config: Optional[Dict[str, Any]] = None) -> CompressionEngine:
        """
        Get an engine instance by name.

        Args:
            name: Engine name (case-insensitive)
            config: Optional configuration for the engine

        Returns:
            Instantiated compression engine

        Raises:
            KeyError: If engine not found
        """
        engine_name = name.lower()

        if engine_name not in cls._engines:
            available = ', '.join(cls._engines.keys())
            raise KeyError(f"Engine '{name}' not found. Available: {available}")

        engine_class = cls._engines[engine_name]
        return engine_class(config)

    @classmethod
    def list_engines(cls) -> List[Dict[str, str]]:
        """
        List all registered engines.

        Returns:
            List of engine information dictionaries
        """
        engines = []
        for engine_class in cls._engines.values():
            temp_instance = engine_class()
            engines.append({
                'name': temp_instance.name,
                'version': temp_instance.version,
                'description': temp_instance.description
            })
        return engines

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """
        Check if an engine is registered.

        Args:
            name: Engine name

        Returns:
            True if registered, False otherwise
        """
        return name.lower() in cls._engines

    @classmethod
    def unregister(cls, name: str) -> None:
        """
        Unregister an engine.

        Args:
            name: Engine name to unregister

        Raises:
            KeyError: If engine not found
        """
        engine_name = name.lower()
        if engine_name not in cls._engines:
            raise KeyError(f"Engine '{name}' not registered")

        del cls._engines[engine_name]

    @classmethod
    def clear(cls) -> None:
        """Clear all registered engines."""
        cls._engines.clear()


def register_engine(engine_class: Type[CompressionEngine]) -> Type[CompressionEngine]:
    """
    Decorator for auto-registering engines.

    Usage:
        @register_engine
        class MyEngine(CompressionEngine):
            ...

    Args:
        engine_class: Engine class to register

    Returns:
        The same engine class (for chaining)
    """
    EngineRegistry.register(engine_class)
    return engine_class


# Convenience functions
def get_engine(name: str, config: Optional[Dict[str, Any]] = None) -> CompressionEngine:
    """
    Get a compression engine by name.

    Args:
        name: Engine name
        config: Optional configuration

    Returns:
        Engine instance
    """
    return EngineRegistry.get_engine(name, config)


def list_engines() -> List[Dict[str, str]]:
    """
    List all available engines.

    Returns:
        List of engine info dictionaries
    """
    return EngineRegistry.list_engines()

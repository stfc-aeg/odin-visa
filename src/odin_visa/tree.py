from inspect import isclass
import logging
from pprint import pformat
from types import NoneType
from typing import Callable, Generic, Type, TypeVar, overload

from odin_control.adapters.parameter_tree import ParameterTree

# TODO: Document
# TODO: Make auto get explicit?
Instance = TypeVar("Instance")
Value = TypeVar("Value")


class Leaf(Generic[Instance, Value]):
    def __init__(
        self,
        type: Type[Value],
        get: Callable[[Instance], Value] | None = None,
        set: Callable[[Instance, Value], None] | None = None,
    ):
        self._attr = ""
        self.set = set

        # if the type is not None ('command' leaf), and get isn't specified, we use
        #   a default getter that returns _attr. most leaf nodes will use this
        if type != NoneType and get == None:

            def default_get(instance: Instance) -> Value:
                return getattr(instance, self._attr)

            self.get = default_get
            return

        self.get = get

    def __set_name__(self, owner: Type[Instance], name: str) -> None:
        self._attr = f"_param_{name}"

    @overload
    def __get__(self, instance: None, owner: Type[Instance]) -> "Leaf": ...
    @overload
    def __get__(self, instance: Instance, owner: Type[Instance]) -> Value: ...

    def __get__(
        self, instance: Instance | None, owner: Type[Instance]
    ) -> "Leaf" | Value:

        if instance is None:
            return self
        return getattr(instance, self._attr)

    def __set__(self, instance: Instance, value: Value) -> None:

        setattr(instance, self._attr, value)


Instance = TypeVar("Instance")
Value = TypeVar("Value")


class SubTree(Generic[Instance, Value]):
    def __init__(self, type: Type[Value]):
        self._attr = ""

    def __set_name__(self, owner: Type[Instance], name: str) -> None:
        self._attr = f"_subtree_{name}"

    @overload
    def __get__(self, instance: None, owner: Type[Instance]) -> "SubTree": ...
    @overload
    def __get__(self, instance: Instance, owner: Type[Instance]) -> Value: ...

    def __get__(
        self, instance: Instance | None, owner: Type[Instance]
    ) -> "SubTree" | Value | None:
        if instance is None:
            return self
        return getattr(instance, self._attr, None)

    def __set__(self, instance: Instance, value: Value) -> None:
        setattr(instance, self._attr, value)


class ParameterTreeMixin:
    """Mixin class to provide ParameterTree functionality to classes."""

    def as_tree(self) -> ParameterTree:
        branches = {}

        # TODO: enum as string, autopopulate allowed values
        fields = [(getattr(type(self), attr), attr) for attr in dir(type(self))]
        for field in fields:
            if type(field[0]) == Leaf:
                branches[field[1]] = (
                    (
                        (lambda field=field: field[0].get(self))
                        if field[0].get is not None
                        else None
                    ),
                    (
                        (lambda value, field=field: field[0].set(self, value))
                        if field[0].set is not None
                        else None
                    ),
                )

            if type(field[0]) == SubTree:
                # we need to get the actual subtree value
                attr = getattr(self, field[1])
                subtree = attr.as_tree()
                branches[field[1]] = subtree

        return ParameterTree(branches)

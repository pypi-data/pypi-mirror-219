from __future__ import annotations

import abc
from abc import abstractmethod
from typing import Any, Generic, Literal, Optional, Type, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from slingshot.sdk.errors import SlingshotClientGraphQLException

T = TypeVar("T")

ResponseType = TypeVar("ResponseType", bound=BaseModel)


class GraphQLError(BaseModel):
    message: str
    locations: Optional[list[dict[str, int]]] = None
    path: Optional[list[str]] = None
    extensions: Optional[dict[str, str]] = None


class GraphQLResponse(GenericModel, Generic[T]):
    data: Optional[T] = None
    errors: Optional[list[GraphQLError]] = None

    def as_exception(self) -> SlingshotClientGraphQLException:
        if not self.errors:
            raise ValueError("Cannot create exception from GraphQLResponse with no errors")
        return SlingshotClientGraphQLException.from_graphql_errors(self.errors)

    def get_data_or_raise(self) -> T:
        if self.errors:
            raise self.as_exception()
        if self.data is None:
            raise ValueError("Cannot get data from GraphQL (unexpected)")
        return self.data


class GraphQLSubscriptionResponse(GenericModel, Generic[T]):
    type: Literal['data']
    id: str
    payload: GraphQLResponse[T]


class BaseGraphQLEntity(BaseModel, abc.ABC):
    @property
    @abstractmethod
    def _fragment(self) -> str:
        ...

    @property
    @abstractmethod
    def _depends_on(self) -> list[Type[BaseGraphQLEntity]]:
        raise NotImplementedError()

    def _get_dependencies_ext(self, visited: set[Type[BaseGraphQLEntity]]) -> set[Type[BaseGraphQLEntity]]:
        # Recursively get all dependencies
        dependencies = set()

        for dependency in self._depends_on:
            dependencies.add(dependency)
            # This is hacky. This is bc we can't declare _fragment or _depends_on as abstract class properties
            if dependency not in visited:
                visited.add(dependency)
                dependencies = dependencies.union(dependency._get_dependencies_ext(dependency, visited))  # type: ignore
        return dependencies.union(visited)

    def _get_dependencies(self) -> list[Type[BaseGraphQLEntity]]:
        return list(self._get_dependencies_ext(set()))

    def get_fragment_string(self) -> str:
        """Get the GraphQL fragment string for this entity, including all dependencies"""
        dependencies = set(self._get_dependencies())
        fragments: list[str] = [dependency._fragment for dependency in dependencies]  # type: ignore
        fragments.append(self._fragment)
        return "\n".join(fragments)


class BaseGraphQLQuery(BaseGraphQLEntity, GenericModel, Generic[ResponseType], abc.ABC):
    query: str
    variables: Optional[dict[str, Any]]
    response_model: Type[ResponseType]

    @property
    @abstractmethod
    def _query(self) -> str:
        ...

    @property
    def _fragment(self) -> str:
        return self._query

    def get_query(self, **kwargs: Any) -> str:
        return self.get_fragment_string()

    def __init__(self, variables: Optional[dict[str, Any]], response_model: Type[ResponseType]):
        super().__init__(query=self.get_query(), variables=variables, response_model=response_model)

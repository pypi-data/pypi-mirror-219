from __future__ import annotations

from typing import Any, List, Optional, Sequence

from pydantic import validator
from typing_extensions import override

from dbt_semantic_interfaces.implementations.base import (
    HashableBaseModel,
    ModelWithMetadataParsing,
)
from dbt_semantic_interfaces.implementations.elements.dimension import PydanticDimension
from dbt_semantic_interfaces.implementations.elements.entity import PydanticEntity
from dbt_semantic_interfaces.implementations.elements.measure import PydanticMeasure
from dbt_semantic_interfaces.implementations.metadata import PydanticMetadata
from dbt_semantic_interfaces.protocols import (
    ProtocolHint,
    SemanticModel,
    SemanticModelDefaults,
)
from dbt_semantic_interfaces.references import (
    LinkableElementReference,
    MeasureReference,
    SemanticModelReference,
    TimeDimensionReference,
)


class NodeRelation(HashableBaseModel):
    """Path object to where the data should be."""

    alias: str
    schema_name: str
    database: Optional[str] = None
    relation_name: str = ""

    @validator("relation_name", always=True)
    @classmethod
    def __create_default_relation_name(cls, value: Any, values: Any) -> str:  # type: ignore[misc]
        """Dynamically build the dot path for `relation_name`, if not specified."""
        if value:
            # Only build the relation_name if it was not present in config.
            return value

        alias, schema, database = values.get("alias"), values.get("schema_name"), values.get("database")
        if alias is None or schema is None:
            raise ValueError(
                f"Failed to build relation_name because alias and/or schema was None. schema: {schema}, alias: {alias}"
            )

        if database is not None:
            value = f"{database}.{schema}.{alias}"
        else:
            value = f"{schema}.{alias}"
        return value

    @staticmethod
    def from_string(sql_str: str) -> NodeRelation:  # noqa: D
        sql_str_split = sql_str.split(".")
        if len(sql_str_split) == 2:
            return NodeRelation(schema_name=sql_str_split[0], alias=sql_str_split[1])
        elif len(sql_str_split) == 3:
            return NodeRelation(database=sql_str_split[0], schema_name=sql_str_split[1], alias=sql_str_split[2])
        raise RuntimeError(
            f"Invalid input for a SQL table, expected form '<schema>.<table>' or '<db>.<schema>.<table>' "
            f"but got: {sql_str}"
        )


class PydanticSemanticModelDefaults(HashableBaseModel, ProtocolHint[SemanticModelDefaults]):  # noqa: D
    @override
    def _implements_protocol(self) -> SemanticModelDefaults:  # noqa: D
        return self

    agg_time_dimension: Optional[str]


class PydanticSemanticModel(HashableBaseModel, ModelWithMetadataParsing, ProtocolHint[SemanticModel]):
    """Describes a semantic model."""

    @override
    def _implements_protocol(self) -> SemanticModel:
        return self

    name: str
    defaults: Optional[PydanticSemanticModelDefaults]
    description: Optional[str]
    node_relation: NodeRelation

    entities: Sequence[PydanticEntity] = []
    measures: Sequence[PydanticMeasure] = []
    dimensions: Sequence[PydanticDimension] = []

    metadata: Optional[PydanticMetadata]

    @property
    def entity_references(self) -> List[LinkableElementReference]:  # noqa: D
        return [i.reference for i in self.entities]

    @property
    def dimension_references(self) -> List[LinkableElementReference]:  # noqa: D
        return [i.reference for i in self.dimensions]

    @property
    def measure_references(self) -> List[MeasureReference]:  # noqa: D
        return [i.reference for i in self.measures]

    @property
    def has_validity_dimensions(self) -> bool:  # noqa: D
        return any([dim.validity_params is not None for dim in self.dimensions])

    @property
    def validity_start_dimension(self) -> Optional[PydanticDimension]:  # noqa: D
        validity_start_dims = [dim for dim in self.dimensions if dim.validity_params and dim.validity_params.is_start]
        if not validity_start_dims:
            return None
        assert (
            len(validity_start_dims) == 1
        ), "Found more than one validity start dimension. This should have been blocked in validation!"
        return validity_start_dims[0]

    @property
    def validity_end_dimension(self) -> Optional[PydanticDimension]:  # noqa: D
        validity_end_dims = [dim for dim in self.dimensions if dim.validity_params and dim.validity_params.is_end]
        if not validity_end_dims:
            return None
        assert (
            len(validity_end_dims) == 1
        ), "Found more than one validity end dimension. This should have been blocked in validation!"
        return validity_end_dims[0]

    @property
    def partitions(self) -> List[PydanticDimension]:  # noqa: D
        return [dim for dim in self.dimensions or [] if dim.is_partition]

    @property
    def partition(self) -> Optional[PydanticDimension]:  # noqa: D
        partitions = self.partitions
        if not partitions:
            return None
        if len(partitions) > 1:
            raise ValueError(f"too many partitions for semantic_model {self.name}")
        return partitions[0]

    @property
    def reference(self) -> SemanticModelReference:  # noqa: D
        return SemanticModelReference(semantic_model_name=self.name)

    def get_measure(self, measure_reference: MeasureReference) -> PydanticMeasure:  # noqa: D
        for measure in self.measures:
            if measure.reference == measure_reference:
                return measure

        raise ValueError(
            f"No dimension with name ({measure_reference.element_name}) in semantic_model with name ({self.name})"
        )

    def get_dimension(self, dimension_reference: LinkableElementReference) -> PydanticDimension:  # noqa: D
        for dim in self.dimensions:
            if dim.reference == dimension_reference:
                return dim

        raise ValueError(f"No dimension with name ({dimension_reference}) in semantic_model with name ({self.name})")

    def get_entity(self, entity_reference: LinkableElementReference) -> PydanticEntity:  # noqa: D
        for entity in self.entities:
            if entity.reference == entity_reference:
                return entity

        raise ValueError(f"No entity with name ({entity_reference}) in semantic_model with name ({self.name})")

    def checked_agg_time_dimension_for_measure(self, measure_reference: MeasureReference):  # noqa: D
        measure = self.get_measure(measure_reference=measure_reference)
        if self.defaults is not None:
            default_agg_time_dimesion = self.defaults.agg_time_dimension

        agg_time_dimension_name = measure.agg_time_dimension or default_agg_time_dimesion
        assert agg_time_dimension_name is not None, (
            f"Aggregation time dimension for measure {measure.name} is not set! This should either be set directly on "
            f"the measure specification in the model, or else defaulted to the primary time dimension in the data "
            f"source containing the measure."
        )
        return TimeDimensionReference(element_name=agg_time_dimension_name)

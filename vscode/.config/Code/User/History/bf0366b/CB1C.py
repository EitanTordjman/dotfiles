"""Table analysis models — shared input/output contracts for the table analysis pipeline."""

from pydantic import BaseModel

from ._base import PromptContext, PromptOutput

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class ColumnStatistics(BaseModel):
    distinct_count: int | None = None
    uniqueness_ratio: float | None = None
    null_percentage: float | None = None
    min: str | None = None
    max: str | None = None
    avg: float | None = None
    avg_length: float | None = None
    sample_values: list[str] = []


class ColumnContext(BaseModel):
    name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    check_constraint: str | None = None
    default_value: str | None = None
    statistics: ColumnStatistics | None = None
    possible_values: list[str] = []


class DependsOnRef(BaseModel):
    schema_name: str
    table: str
    column: str
    referenced_column: str


class DependentRef(BaseModel):
    schema_name: str
    table: str


class ParentDescription(BaseModel):
    schema_name: str
    table: str
    description: str


class DatabaseContext(BaseModel):
    description: str | None = None


class TableRef(BaseModel):
    schema_name: str
    name: str


class TableAnalysisContext(PromptContext):
    table_name: str
    schema_name: str
    row_count: int | None = None
    dependency_level: int | None = None
    columns: list[ColumnContext]
    depends_on: list[DependsOnRef] = []
    dependents: list[DependentRef] = []
    parent_descriptions: list[ParentDescription] = []
    database_context: DatabaseContext | None = None
    all_tables: list[TableRef] = []
    metadata_only: bool = False


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------


class ColumnDescriptionOutput(BaseModel):
    column_name: str
    description: str
    reasoning: str


class TableAnalysisOutput(PromptOutput):
    table_description: str
    reasoning: str
    column_descriptions: list[ColumnDescriptionOutput]

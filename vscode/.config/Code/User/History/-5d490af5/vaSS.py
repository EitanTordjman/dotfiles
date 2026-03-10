"""Table Analysis prompt — translates table-analysis.md Jinja2 template into Python."""

import json
from typing import Type

from pydantic import BaseModel, Field

from ._base import Prompt


# ---------------------------------------------------------------------------
# Context models (input)
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


class SeedContext(BaseModel):
    overall_purpose: str | None = None
    business_domains: list[str] = []
    industry_context: str | None = None
    custom_instructions: str | None = None


class TableRef(BaseModel):
    schema_name: str
    name: str


class TableAnalysisContext(BaseModel):
    table_name: str
    schema_name: str
    row_count: int | None = None
    dependency_level: int | None = None
    columns: list[ColumnContext]
    depends_on: list[DependsOnRef] = []
    dependents: list[DependentRef] = []
    parent_descriptions: list[ParentDescription] = []
    user_notes: str | None = None
    seed_context: SeedContext | None = None
    all_tables: list[TableRef] = []
    metadata_only: bool = False


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------


class ColumnDescriptionOutput(BaseModel):
    column_name: str
    description: str
    reasoning: str


class ParentTableInsight(BaseModel):
    parent_table: str
    insight: str
    confidence: float = Field(ge=0.0, le=1.0)


class TableAnalysisOutput(BaseModel):
    table_description: str
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    column_descriptions: list[ColumnDescriptionOutput]
    inferred_business_domain: str | None = None
    parent_table_insights: list[ParentTableInsight] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _example_json() -> str:
    """Generate a representative JSON example from the output models."""
    example = TableAnalysisOutput(
        table_description="A clear, concise description of what this table stores and its purpose",
        reasoning="Explain the evidence that led to this conclusion",
        confidence=0.95,
        column_descriptions=[
            ColumnDescriptionOutput(
                column_name="col",
                description="What this column represents",
                reasoning="Evidence supporting this interpretation",
            )
        ],
        inferred_business_domain="Sales",
        parent_table_insights=[
            ParentTableInsight(
                parent_table="schema.table",
                insight="New insight about parent table revealed by this analysis",
                confidence=0.85,
            )
        ],
    )
    return json.dumps(example.model_dump(), indent=2)


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------


class TableAnalysisPrompt(Prompt[TableAnalysisContext, TableAnalysisOutput]):

    @property
    def output_model(self) -> Type[TableAnalysisOutput]:
        return TableAnalysisOutput

    def system_prompt(self, context: TableAnalysisContext) -> str:
        return (
            "You are a senior database documentation specialist. "
            "Analyze database schemas and produce precise, developer-friendly "
            "documentation. Be thorough and factual — never speculate beyond "
            "what the evidence supports."
        )

    def user_prompt(self, context: TableAnalysisContext) -> str:
        sections: list[str | None] = [
            self._intro(context),
            self._table_info(context),
            self._columns(context),
            self._relationships(context),
            self._parent_context(context),
            self._user_notes(context),
            self._db_context(context),
            self._all_tables(context),
            self._task(context),
        ]
        return "\n".join(s for s in sections if s is not None)

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _intro(self, context: TableAnalysisContext) -> str:
        lines = [
            "You are analyzing a database table to generate comprehensive documentation. "
            "Your task is to infer the table's purpose based on the evidence provided."
        ]
        if context.metadata_only:
            lines.append(
                "\n> **Metadata-Only Mode**: Only schema metadata is available for this "
                "analysis (table and column names, data types, constraints). No row-level "
                "statistics, sample values, or cardinality information exist. Base your "
                "reasoning solely on naming conventions, data types, and structural relationships."
            )
        return "\n".join(lines)

    def _table_info(self, context: TableAnalysisContext) -> str:
        lines = ["\n## Table Information"]
        lines.append(f"- **Name**: {context.table_name}")
        lines.append(f"- **Schema**: {context.schema_name}")
        if context.row_count is not None:
            lines.append(f"- **Row Count**: {context.row_count}")
        if context.dependency_level is not None:
            lines.append(f"- **Dependency Level**: {context.dependency_level} (0 = no dependencies)")
        return "\n".join(lines)

    def _columns(self, context: TableAnalysisContext) -> str:
        lines = ["\n## Columns"]
        for column in context.columns:
            lines.extend(self._format_column(column, context))
        return "\n".join(lines)

    def _format_column(self, column: ColumnContext, context: TableAnalysisContext) -> list[str]:
        not_null = " NOT NULL" if not column.is_nullable else ""
        lines: list[str] = [f"\n- **{column.name}** (`{column.data_type}`){not_null}"]

        if column.is_primary_key:
            lines.append("  - **PRIMARY KEY**")

        fk_ref = next((dep for dep in context.depends_on if dep.column == column.name), None)
        if fk_ref:
            lines.append(
                f"  - **FOREIGN KEY** → "
                f"{fk_ref.schema_name}.{fk_ref.table}.{fk_ref.referenced_column}"
            )

        if column.check_constraint:
            lines.append(f"  - Check Constraint: {column.check_constraint}")

        if column.default_value:
            lines.append(f"  - Default: {column.default_value}")

        if not context.metadata_only and column.statistics:
            lines.extend(self._format_column_statistics(column.statistics))

        if not context.metadata_only and column.possible_values:
            lines.append(f"  - Possible Values: {', '.join(column.possible_values)}")

        return lines

    def _format_column_statistics(self, statistics: ColumnStatistics) -> list[str]:
        lines: list[str] = []
        if statistics.distinct_count is not None and statistics.uniqueness_ratio is not None:
            lines.append(
                f"  - Distinct Values: {statistics.distinct_count} "
                f"({round(statistics.uniqueness_ratio * 100, 1)}% unique)"
            )
        if statistics.null_percentage is not None and statistics.null_percentage > 0:
            lines.append(f"  - Nulls: {round(statistics.null_percentage, 1)}%")
        if statistics.min is not None:
            range_str = f"  - Range: {statistics.min} to {statistics.max}"
            if statistics.avg is not None:
                range_str += f" (avg: {round(statistics.avg, 2)})"
            lines.append(range_str)
        if statistics.avg_length is not None:
            lines.append(f"  - Avg Length: {round(statistics.avg_length, 1)} chars")
        if statistics.sample_values:
            lines.append(f"  - Sample Values: {json.dumps(statistics.sample_values)}")
        return lines

    def _relationships(self, context: TableAnalysisContext) -> str:
        lines = ["\n## Relationships"]
        if context.depends_on:
            lines.append("**This table references (depends on):**")
            for dependency in context.depends_on:
                lines.append(
                    f"- {dependency.schema_name}.{dependency.table} "
                    f"(via column: {dependency.column} → {dependency.referenced_column})"
                )
        if context.dependents:
            lines.append("\n**Referenced by (dependents):**")
            for dependent in context.dependents:
                lines.append(f"- {dependent.schema_name}.{dependent.table}")
        if not context.depends_on:
            lines.append(
                "**Note**: This table has no dependencies on other tables (dependency level 0). "
                "It is likely a foundational/lookup table."
            )
        return "\n".join(lines)

    def _parent_context(self, context: TableAnalysisContext) -> str | None:
        if not context.parent_descriptions:
            return None
        lines = ["\n## Parent Table Context", "Understanding from tables this table references:\n"]
        for parent in context.parent_descriptions:
            lines.append(f"**{parent.schema_name}.{parent.table}**: {parent.description}")
        return "\n".join(lines)

    def _user_notes(self, context: TableAnalysisContext) -> str | None:
        if not context.user_notes:
            return None
        return "\n## User Notes\n" + context.user_notes

    def _db_context(self, context: TableAnalysisContext) -> str | None:
        if not context.seed_context:
            return None
        seed = context.seed_context
        lines = ["\n## Database Context"]
        if seed.overall_purpose:
            lines.append(f"- **Purpose**: {seed.overall_purpose}")
        if seed.business_domains:
            lines.append(f"- **Business Domains**: {', '.join(seed.business_domains)}")
        if seed.industry_context:
            lines.append(f"- **Industry**: {seed.industry_context}")
        if seed.custom_instructions:
            lines.append(f"- **Special Instructions**: {seed.custom_instructions}")
        return "\n".join(lines)

    def _all_tables(self, context: TableAnalysisContext) -> str | None:
        if not context.all_tables:
            return None
        lines = [
            "\n## All Database Tables",
            "**IMPORTANT**: When referring to table relationships, "
            "you MUST use one of these exact table names:",
        ]
        for table in context.all_tables:
            lines.append(f"- {table.schema_name}.{table.name}")
        lines.append("\n**Do NOT make up table names** — only use the exact names listed above.")
        return "\n".join(lines)

    def _task(self, context: TableAnalysisContext) -> str:
        evidence_sources = "column names, relationships, data types"
        if not context.metadata_only:
            evidence_sources += ", sample values, cardinality"

        stat_guidelines = ""
        if not context.metadata_only:
            stat_guidelines = (
                "- Low cardinality (< 20 distinct values) suggests enum/category values "
                "— use them to understand meaning.\n"
                "- High uniqueness ratio (> 95%) suggests an identifier or code column.\n"
                "- Null percentage reveals whether a column is required or optional.\n"
            )

        return (
            "\n---\n\n## Your Task\n"
            "Based on the evidence above, generate a JSON response with this exact structure:\n"
            "\n```json\n"
            + _example_json()
            + "\n```\n\n"
            "**Guidelines:**\n"
            f"1. **Table Description**: Focus on WHAT the table stores and WHY it exists.\n"
            f"2. **Reasoning**: Reference specific evidence ({evidence_sources}).\n"
            "3. **Confidence**: 0–1 scale. Be conservative — use < 0.7 if ambiguous.\n"
            "4. **Column Descriptions**: Describe every column. Do not skip any.\n"
            "5. **Business Domain**: Infer from table name and purpose (e.g., Sales, HR, Inventory, Billing).\n"
            "6. **Parent Table Insights**: Include only if this analysis reveals genuinely new information about a parent table.\n"
            "\n"
            "**Important:**\n"
            "- When mentioning table names in descriptions, always use `schema.table` format.\n"
            + stat_guidelines
            + "\nReturn ONLY valid JSON. Do not include markdown code fences or explanatory text."
        )

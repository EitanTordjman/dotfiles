"""Test script for the prompt engine.

Builds a sample TableAnalysisContext and prints the rendered prompt
exactly as it would be sent to the LLM.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from prompt_engine import get_prompt, TableAnalysisContext
from prompt_engine.table_analysis import (
    ColumnContext,
    ColumnStatistics,
    DatabaseContext,
    DependsOnRef,
    DependentRef,
    ParentDescription,
    TableRef,
)

# ---------------------------------------------------------------------------
# Build a sample context — an "orders" table
# ---------------------------------------------------------------------------

context = TableAnalysisContext(
    table_name="orders",
    schema_name="sales",
    row_count=842_310,
    dependency_level=1,
    columns=[
        ColumnContext(
            name="id",
            data_type="bigint",
            is_nullable=False,
            is_primary_key=True,
            statistics=ColumnStatistics(
                distinct_count=842_310,
                uniqueness_ratio=1.0,
                null_percentage=0.0,
            ),
        ),
        ColumnContext(
            name="user_id",
            data_type="bigint",
            is_nullable=False,
            statistics=ColumnStatistics(
                distinct_count=54_200,
                uniqueness_ratio=0.064,
                null_percentage=0.0,
            ),
        ),
        ColumnContext(
            name="status",
            data_type="varchar(20)",
            is_nullable=False,
            statistics=ColumnStatistics(
                distinct_count=5,
                uniqueness_ratio=0.0,
                null_percentage=0.0,
                sample_values=["pending", "confirmed", "shipped", "delivered", "cancelled"],
            ),
            possible_values=["pending", "confirmed", "shipped", "delivered", "cancelled"],
        ),
        ColumnContext(
            name="total_amount",
            data_type="numeric(12,2)",
            is_nullable=False,
            statistics=ColumnStatistics(
                distinct_count=320_000,
                uniqueness_ratio=0.38,
                null_percentage=0.0,
                min="0.99",
                max="9999.99",
                avg=127.45,
            ),
        ),
        ColumnContext(
            name="shipping_address_id",
            data_type="bigint",
            is_nullable=True,
            statistics=ColumnStatistics(
                distinct_count=41_000,
                uniqueness_ratio=0.049,
                null_percentage=3.2,
            ),
        ),
        ColumnContext(
            name="created_at",
            data_type="timestamptz",
            is_nullable=False,
            statistics=ColumnStatistics(
                distinct_count=842_310,
                uniqueness_ratio=1.0,
                null_percentage=0.0,
                min="2021-01-01 00:00:01+00",
                max="2024-12-31 23:59:59+00",
            ),
        ),
        ColumnContext(
            name="notes",
            data_type="text",
            is_nullable=True,
            statistics=ColumnStatistics(
                distinct_count=12_400,
                uniqueness_ratio=0.015,
                null_percentage=88.5,
                avg_length=42.3,
            ),
        ),
    ],
    depends_on=[
        DependsOnRef(
            schema_name="public", table="users",
            column="user_id", referenced_column="id",
        ),
        DependsOnRef(
            schema_name="public", table="addresses",
            column="shipping_address_id", referenced_column="id",
        ),
    ],
    dependents=[
        DependentRef(schema_name="sales", table="order_items"),
        DependentRef(schema_name="sales", table="payments"),
    ],
    parent_descriptions=[
        ParentDescription(
            schema_name="public",
            table="users",
            description="Registered customer accounts, including authentication credentials and profile data.",
        ),
        ParentDescription(
            schema_name="public",
            table="addresses",
            description="Physical delivery and billing addresses associated with user accounts.",
        ),
    ],
    database_context=DatabaseContext(
        description="E-commerce platform in the retail industry, covering Sales and Fulfilment domains.",
    ),
    all_tables=[
        TableRef(schema_name="public", name="users"),
        TableRef(schema_name="public", name="addresses"),
        TableRef(schema_name="sales", name="orders"),
        TableRef(schema_name="sales", name="order_items"),
        TableRef(schema_name="sales", name="payments"),
    ],
)

# ---------------------------------------------------------------------------
# Render and print
# ---------------------------------------------------------------------------

prompt = get_prompt("table_analysis")
rendered = prompt.render(context)
messages = rendered.to_openai_messages()

DIVIDER = "=" * 70

print(DIVIDER)
print("SYSTEM MESSAGE")
print(DIVIDER)
print(rendered.system_message)

print()
print(DIVIDER)
print("USER MESSAGE")
print(DIVIDER)
print(rendered.user_message)

print()
print(DIVIDER)
print(f"to_openai_messages() → {len(messages)} message(s)")
for i, msg in enumerate(messages):
    print(f"  [{i}] role={msg['role']}  chars={len(msg['content'])}")

print()
print(DIVIDER)
print("OUTPUT SCHEMA (TableAnalysisOutput fields)")
print(DIVIDER)
for name, field in prompt.output_model.model_fields.items():
    print(f"  {name}: {field.annotation}")

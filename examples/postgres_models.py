"""
That example shows how to create a DataEntityList object with DataEntity objects for a potential Postgres database.
Resulted DataEntityList object are ready to be ingested to the OpenDataDiscovery platform.

generator - helper object to generate ODDRN for Postgres entities
database - DataEntity object for a database. Database has data_entity_group with DataEntity objects for tables and views.
table - DataEntity object for a table
view - DataEntity object for a view which connected to the table
"""

from oddrn_generator import PostgresqlGenerator

from odd_models.models import (
    DataEntity,
    DataEntityGroup,
    DataEntityList,
    DataEntityType,
    DataSet,
    DataSetField,
    DataSetFieldType,
    DataTransformer,
    MetadataExtension,
    Type,
)

generator = PostgresqlGenerator(
    host_settings="localhost", databases="my_database", schemas="public"
)

table = DataEntity(
    oddrn=generator.get_oddrn_by_path("tables", "my_table"),
    name="my_table",
    type=DataEntityType.TABLE,
    metadata=[
        MetadataExtension(
            schema_url="https://example.com/schema.json", metadata={"key": "value"}
        )
    ],
    dataset=DataSet(
        field_list=[
            DataSetField(
                oddrn=generator.get_oddrn_by_path("tables_columns", "id"),
                name="id",
                type=DataSetFieldType(
                    type=Type.TYPE_NUMBER, logical_type="int", is_nullable=False
                ),
            ),
            DataSetField(
                oddrn=generator.get_oddrn_by_path("tables_columns", "name"),
                name="name",
                type=DataSetFieldType(
                    type=Type.TYPE_STRING, logical_type="str", is_nullable=False
                ),
            ),
        ]
    ),
)

view = DataEntity(
    oddrn=generator.get_oddrn_by_path("views", "my_views"),
    name="my_view",
    type=DataEntityType.VIEW,
    data_transformer=DataTransformer(inputs=[table.oddrn], outputs=[]),
    dataset=DataSet(
        field_list=[
            DataSetField(
                oddrn=generator.get_oddrn_by_path("views_columns", "name"),
                name="name",
                type=DataSetFieldType(
                    type=Type.TYPE_STRING, logical_type="str", is_nullable=False
                ),
            )
        ]
    ),
)

database = DataEntity(
    oddrn=generator.get_oddrn_by_path("databases", "my_database"),
    name="my_database",
    type=DataEntityType.DATABASE_SERVICE,
    data_entity_group=DataEntityGroup(entities_list=[table.oddrn, view.oddrn]),
)

data_entity_list = DataEntityList(
    data_source_oddrn=generator.get_data_source_oddrn(), items=[table, view, database]
)

print(data_entity_list.json(indent=4, sort_keys=True))

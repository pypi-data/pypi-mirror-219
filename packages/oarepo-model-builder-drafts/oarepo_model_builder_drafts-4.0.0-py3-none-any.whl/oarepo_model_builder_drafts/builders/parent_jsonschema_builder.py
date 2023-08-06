from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.utils.dict import dict_get


class JSONSchemaDraftsParentBuilder(JSONSchemaBuilder):
    TYPE = "jsonschema_drafts_parent"
    output_file_type = "jsonschema"
    output_file_name = ["draft-parent-record-schema", "file"]
    parent_module_root_name = "jsonschemas"

    def target_json(self):
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            # "$id": f"{schema.current_model.schema_server}{schema.current_model.drafts_parent_schema_name}",
            "$id": "local://parent-v1.0.0.json",
            "type": "object",
            "properties": {"id": {"type": "keyword"}},
        }

    def build_node(self, node):
        from oarepo_model_builder.datatypes import datatypes

        json = self.target_json()
        parsed_section = datatypes.get_datatype(
            parent=None,
            data=json,
            key=None,
            model=json,
            schema=json,
        )
        parsed_section.prepare({})
        skip = dict_get(
            self.current_model.definition, ["json-schema-settings", "skip"], False
        )
        if skip:
            return
        generated = self.generate(node)
        self.output.merge(generated)

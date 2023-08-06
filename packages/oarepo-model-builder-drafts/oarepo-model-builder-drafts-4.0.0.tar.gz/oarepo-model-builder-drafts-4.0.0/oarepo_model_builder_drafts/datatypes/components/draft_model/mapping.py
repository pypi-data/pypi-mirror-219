from oarepo_model_builder.datatypes import DataTypeComponent, datatypes

from oarepo_model_builder_drafts.datatypes import DraftDataType


class DraftMappingModelComponent(DataTypeComponent):
    eligible_datatypes = [DraftDataType]

    def process_mapping(self, datatype, section, **kwargs):
        if self.is_draft_profile:  # this will work but idk if it's correct approach
            section.children["expires_at"] = datatypes.get_datatype(
                datatype,
                {
                    "type": "datetime",
                    "sample": {"skip": True},
                    "marshmallow": {"read": False, "write": False},
                    "ui": {"marshmallow": {"read": False, "write": False}},
                },
                "expires_at",
                datatype.model,
                datatype.schema,
            )
            section.children["expires_at"].prepare(context={})
            section.children["fork_version_id"] = datatypes.get_datatype(
                datatype,
                {
                    "type": "integer",
                    "sample": {"skip": True},
                    "marshmallow": {"read": False, "write": False},
                    "ui": {"marshmallow": {"read": False, "write": False}},
                },
                "fork_version_id",
                datatype.model,
                datatype.schema,
            )
            section.children["fork_version_id"].prepare(context={})

    def before_model_prepare(self, datatype, *, context, **kwargs):
        self.is_draft_profile = context["profile"] == "draft"

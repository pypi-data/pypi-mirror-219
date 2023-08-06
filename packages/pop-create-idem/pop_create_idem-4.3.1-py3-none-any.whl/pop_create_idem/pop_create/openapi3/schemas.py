import openapi3


def parse(hub, api: openapi3.OpenAPI):
    schemas = {}

    # Sometimes a schema could just point to different schema object
    # Let's hold them into a separate mapping for adding them into flat schema structure
    transitive_schema_mappings = {}
    # Get a flat structure for schemas
    for name, schema in api.components.raw_element.items():
        if name == "schemas":
            for object_name, param in schema.items():
                parameters = []
                if param.get("$ref", None):
                    # We may need to sanitize it later
                    # "InventoryOrder": {
                    #     "$ref": "#/components/schemas/StoreOrder"
                    # },
                    transitive_schema_mappings[
                        f"#/components/schemas/{object_name}"
                    ] = param.get("$ref")
                elif param.get("type", "") == "object":
                    # "StoreOrder": {
                    #     "type": "object",
                    #     "properties": {
                    #         "name": {
                    #             "type": "string",
                    #             "description": ""
                    #         },
                    #     }
                    for prop_name, prop_value in param.get("properties", {}).items():
                        # Check for nested members first
                        # "pet_order": {
                        #    "$ref": "#/components/schemas/StoreOrder"
                        #  },
                        nested_member_ref = prop_value.get("$ref")
                        nested_member_ref_type = "nested" if nested_member_ref else None
                        if "array" == prop_value.get("type"):
                            # "tags": {
                            #     "type": "array",
                            #     "items": {
                            #         "$ref": "#/definitions/Tag"
                            #     }
                            # },
                            # "photoUrls": {
                            #     "type": "array",
                            #     "items": {
                            #         "type": "string",
                            #     }
                            # },
                            nested_member_ref = prop_value.get("items", {}).get("$ref")
                            # Keeping the default array for now so that it is becomes a list in function params
                            nested_member_ref_type = (
                                "nested_array" if nested_member_ref else "array"
                            )

                        parameters.append(
                            dict(
                                idem_name=hub.tool.format.case.snake(prop_name),
                                actual_name=prop_name,
                                required=prop_name in param.get("required", []),
                                type=nested_member_ref_type
                                if nested_member_ref_type
                                else prop_value.get("type"),
                                nested_member=nested_member_ref,
                                description=prop_value.get("description") or prop_name,
                            )
                        )
                else:
                    # We may need to sanitize it later
                    # "InventoryOrderStatus": {
                    #     "type": "string",
                    #     "description": "<>",
                    # },
                    parameters.append(
                        dict(
                            idem_name="primitive",
                            type=param.get("type"),
                            description=param.get("description"),
                        )
                    )

                schemas[f"#/components/schemas/{object_name}"] = parameters

    for key, actual_schema_ref in transitive_schema_mappings.items():
        # Update schemas with actual schema reference
        schemas[key] = schemas[actual_schema_ref]

    return schemas

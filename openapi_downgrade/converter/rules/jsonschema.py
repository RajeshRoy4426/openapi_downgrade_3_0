from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..warnings import WarningCollector

def downgrade_json_schema(schema: dict, warnings: "WarningCollector") -> dict:
    # Keywords that are not supported in OpenAPI 3.0 and are not handled by other rules.
    # "if", "then", "else" are handled by conditionals_to_oneof.py
    # "const" is handled by const_to_enum.py
    unsupported = ["not", "dependentSchemas", "unevaluatedProperties"]
    
    if isinstance(schema, dict):
        for u in unsupported:
            if u in schema:
                schema[f"x-dropped-{u}"] = schema.pop(u)
                warnings.add(
                    f"The keyword '{u}' is not supported in OpenAPI 3.0 and has been moved to 'x-dropped-{u}'."
                )
        
        for key, value in schema.items():
            downgrade_json_schema(value, warnings)
            
    elif isinstance(schema, list):
        for item in schema:
            downgrade_json_schema(item, warnings)
            
    return schema

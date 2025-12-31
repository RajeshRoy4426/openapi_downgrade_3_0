from .rules.nullable import convert_nullable
from .rules.mixed_types import convert_mixed_types
from .rules.examples import convert_examples
from .rules.webhooks import drop_webhooks
from .rules.jsonschema import downgrade_json_schema
from .rules.booleans import fix_booleans
from .validator import validate_openapi_3
from .rules.exclusives import fix_exclusive_min_max
from .rules.fix_null_type import fix_null_type
from .rules.const_to_enum import convert_const
from .rules.conditionals_to_oneof import conditionals_to_oneof
from .rules.emulate_tuple_items import emulate_tuple_items
from .warnings import WarningCollector
from .rules.warn_unsupported import warn_unsupported_keywords
from .rules.anyof_null import simplify_anyof_null

def convert_spec(spec: dict) -> dict:
    warnings = WarningCollector()
    spec = convert_nullable(spec)
    spec = convert_mixed_types(spec)
    spec = convert_examples(spec)
    spec = drop_webhooks(spec, warnings)
    spec = downgrade_json_schema(spec, warnings)
    spec = fix_booleans(spec)
    spec = fix_exclusive_min_max(spec)
    spec = simplify_anyof_null(spec)
    spec = fix_null_type(spec)
    spec = convert_const(spec)
    spec = conditionals_to_oneof(spec)
    spec = emulate_tuple_items(spec, warnings)
    warn_unsupported_keywords(spec, warnings)

    for key in ["jsonSchemaDialect", "$schema"]:
        spec.pop(key, None)

    spec["openapi"] = "3.0.3"
    is_valid, error = validate_openapi_3(spec)
    if not is_valid:
        raise ValueError(f" OpenAPI 3.0.x Validation Failed:\n{error}")
    if warnings.has_warnings():
        warnings.export()
    return spec
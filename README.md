# OpenAPI Downgrader

 Convert OpenAPI 3.1.x specifications to 3.0.x — with logic preservation, support for `nullable`, `const`, advanced schema handling, and conditionals via `oneOf`.

##  Features

The `openapi-downgrade` tool provides a robust solution for converting OpenAPI 3.1.x specifications to 3.0.x, ensuring maximum compatibility while preserving the original API's logic and intent. Key features include:

-   **Safe Conversion:** Transforms 3.1.x specifications to 3.0.3, handling differences in schema definitions and structural elements.
-   **`nullable` Keyword Handling:** Converts OpenAPI 3.1's `type: ["string", "null"]` syntax to OpenAPI 3.0's `type: "string", nullable: true`.
-   **`const` to `enum` Conversion:** Replaces the `const` keyword (OpenAPI 3.1) with a single-value `enum` (OpenAPI 3.0) to maintain schema constraints.
-   **`if/then/else` to `oneOf` Transformation:** Translates complex conditional schemas using `if/then/else` into equivalent `oneOf` structures, ensuring logical integrity.
-   **`examples` Keyword Adaptation:** Converts the OpenAPI 3.1 `examples` array to the single `example` keyword supported in OpenAPI 3.0, using the first example provided.
-   **Webhook Downgrade:** Transforms OpenAPI 3.1 `webhooks` into OpenAPI 3.0 `callbacks` where suitable operations (POST, PUT, PATCH, DELETE) are available. If no suitable operations are found, a warning is issued.
-   **JSON Schema Downgrade:** Handles various JSON Schema keywords not directly supported in OpenAPI 3.0 (e.g., `not`, `dependentSchemas`, `unevaluatedProperties`) by moving them to `x-dropped-` vendor extensions and issuing warnings.
-   **Boolean String Fixes:** Corrects boolean values represented as strings (e.g., `"true"`, `"false"`) to actual boolean types (`true`, `false`).
-   **Exclusive Minimum/Maximum Fixes:** Adjusts `exclusiveMinimum` and `exclusiveMaximum` definitions for OpenAPI 3.0 compatibility.
-   **Null Type Fixes:** Converts `type: "null"` to `nullable: true` for better OpenAPI 3.0 representation.
-   **Tuple Emulation:** Emulates tuple-style `items` or `prefixItems` in arrays using `minItems`, `maxItems`, and a custom `x-tuple-items` vendor extension.
-   **Unsupported Keyword Warnings:** Identifies and warns about other OpenAPI 3.1 keywords that are not supported in 3.0.x and cannot be automatically converted.
-   **Validation:** Ensures the converted specification is valid against the OpenAPI 3.0.3 schema.
-   **Warning System:** Provides clear warnings for any unsupported or dropped keywords, or for conversions that require manual review, outputting them to the console and an optional `warnings.txt` file.

## ⚙️ Conversion Rules in Detail

The conversion process applies a series of rules to ensure compatibility and preserve logic:

1.  **`nullable` Conversion:**
    *   **OpenAPI 3.1:** `type: ["string", "null"]`
    *   **OpenAPI 3.0:** `type: "string", nullable: true`
    *   **Purpose:** Adapts the way nullability is expressed.

2.  **`const` to `enum`:**
    *   **OpenAPI 3.1:** `const: "value"`
    *   **OpenAPI 3.0:** `enum: ["value"]`
    *   **Purpose:** Provides an equivalent constraint using OpenAPI 3.0's `enum` keyword.

3.  **`if/then/else` to `oneOf`:**
    *   **OpenAPI 3.1:** Conditional schemas using `if`, `then`, and `else`.
    *   **OpenAPI 3.0:** Transformed into `oneOf` structures with appropriate `required` and `properties` to mimic the conditional logic.
    *   **Purpose:** Emulates complex conditional logic not directly available in OpenAPI 3.0.

4.  **`examples` Array to `example`:**
    *   **OpenAPI 3.1:** `examples: ["example1", "example2"]`
    *   **OpenAPI 3.0:** `example: "example1"`
    *   **Purpose:** Adapts to the single `example` field in OpenAPI 3.0.

5.  **Webhook Downgrade:**
    *   **OpenAPI 3.1:** `webhooks` section.
    *   **OpenAPI 3.0:** Converted to `callbacks` within `paths` for POST, PUT, PATCH, and DELETE operations. A default URL expression `{$request.body#/callbackUrl}` is used.
    *   **Purpose:** Provides a compatible mechanism for event-driven API descriptions. Warnings are issued if webhooks cannot be attached to suitable operations.

6.  **JSON Schema Downgrade:**
    *   **OpenAPI 3.1:** Supports a wider range of JSON Schema keywords (e.g., `not`, `dependentSchemas`, `unevaluatedProperties`).
    *   **OpenAPI 3.0:** These keywords are moved to `x-dropped-` vendor extensions (e.g., `x-dropped-not`) and warnings are generated.
    *   **Purpose:** Preserves information about unsupported keywords while ensuring schema validity for OpenAPI 3.0.

7.  **Boolean String Fixes:**
    *   **OpenAPI 3.1:** Allows boolean values as strings (e.g., `"true"`).
    *   **OpenAPI 3.0:** Requires actual boolean types (`true`).
    *   **Purpose:** Ensures correct data type representation.

8.  **Exclusive Minimum/Maximum Fixes:**
    *   **OpenAPI 3.1:** `exclusiveMinimum: 10`
    *   **OpenAPI 3.0:** `minimum: 10, exclusiveMinimum: true`
    *   **Purpose:** Aligns with OpenAPI 3.0's way of defining exclusive bounds.

9.  **Null Type Fixes:**
    *   **OpenAPI 3.1:** `type: "null"`
    *   **OpenAPI 3.0:** `nullable: true`
    *   **Purpose:** Standardizes null type representation.

10. **Tuple Emulation:**
    *   **OpenAPI 3.1:** `items: [schema1, schema2]` or `prefixItems: [schema1, schema2]`
    *   **OpenAPI 3.0:** Emulated using `minItems`, `maxItems`, and `x-tuple-items` vendor extension.
    *   **Purpose:** Provides a way to represent ordered, fixed-length arrays.

11. **Unsupported Keyword Warnings:**
    *   **OpenAPI 3.1:** Keywords like `contains`, `patternProperties`, `items` (in some forms) are not fully supported in OpenAPI 3.0.
    *   **OpenAPI 3.0:** These keywords are retained but warnings are issued to alert the user about potential compatibility issues.
    *   **Purpose:** Informs the user about elements that might behave differently or require manual adjustment.

## 📦 Installation

You can install the tool from PyPI:

```bash
pip install openapi-downgrade
```

Or, for development, you can clone the repository and install it in editable mode:

```bash
git clone https://github.com/RajeshRoy4426/openapi_downgrade_3_0.git
cd openapi_downgrade_3_0
pip install -e .
```

## Usage

The command-line interface allows you to convert an OpenAPI specification from a file or a URL.

### Command Syntax

```bash
openapi_downgrade <input_path_or_url> <output_path>
```

To see detailed help and available options, use:

```bash
openapi_downgrade --help
```

### Arguments

-   `<input_path_or_url>`: The path to your local OpenAPI 3.1.x file or a URL to a raw spec.
-   `<output_path>`: The file path where the converted 3.0.x spec will be saved.

### Example

```bash
python -m openapi_downgrade.cli https://testapi334-d4fvgterd3cjd2bf.southeastasia-01.azurewebsites.net/openapi.json openapi_3_0.json
```

This will download the OpenAPI 3.1.x specification from the provided URL, convert it to OpenAPI 3.0.x, and save the result as `openapi_3_0.json` in your current directory.

### Handling Warnings

During conversion, the tool may encounter elements that are not directly convertible or require manual review. These situations generate warnings:

-   **Console Output:** Warnings are printed directly to your console during the conversion process.
-   **`warnings.txt` File:** A `warnings.txt` file is automatically generated in the current working directory if any warnings occur. This file contains a detailed list of all warnings, which you should review to ensure the converted specification meets your requirements.

It's crucial to review these warnings and make any necessary manual adjustments to the generated OpenAPI 3.0.x specification.

## Testing

Clone the repository, then in the cloned directory:

```
virtualenv .
. bin/activate
python3 -m pip install -e .
python3 -m pytest tests/
```

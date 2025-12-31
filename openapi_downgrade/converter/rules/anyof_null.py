def simplify_anyof_null(schema: dict) -> dict:
    """
    Detects anyOf/oneOf where one of the options is {"type": "null"}.
    Removes it, sets nullable: true on the parent, and merges if possible.
    
    This must run BEFORE fix_null_type, as it looks for {"type": "null"}.
    """
    if isinstance(schema, dict):
        # Recurse first
        for key, value in list(schema.items()):
            if isinstance(value, (dict, list)):
                simplify_anyof_null(value)

        # Check for anyOf or oneOf
        for key in ["anyOf", "oneOf"]:
            if key in schema and isinstance(schema[key], list):
                items = schema[key]
                null_index = -1
                
                # Find type: null
                for idx, item in enumerate(items):
                    if isinstance(item, dict) and item.get("type") == "null":
                        null_index = idx
                        break
                
                if null_index != -1:
                    # Remove the null item
                    items.pop(null_index)
                    
                    # Mark parent as nullable
                    schema["nullable"] = True
                    
                    # If empty list remains (was just null?), unlikely but possible
                    if not items:
                        del schema[key]
                        # effectively any (nullable)
                    
                    # If only 1 item remains, we can simplify
                    elif len(items) == 1:
                        single_item = items[0]
                        del schema[key]
                        
                        # Merge logic
                        if "$ref" in single_item:
                            # Cannot merge $ref with siblings in OA3.0 generally
                            # Solution: wrap in allOf
                            schema["allOf"] = [single_item]
                        else:
                            # Merge properties
                            # Be careful of conflicts, but usually safe to merge keys
                            for k, v in single_item.items():
                                if k not in schema:
                                    schema[k] = v
                                else:
                                    # If conflict, keep existing? or overwrite?
                                    # For type, format, etc, overwrite is usually fine
                                    # But let's check
                                    pass
    
    elif isinstance(schema, list):
        for item in schema:
            simplify_anyof_null(item)
            
    return schema

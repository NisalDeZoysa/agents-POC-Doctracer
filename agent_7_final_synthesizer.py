"""
Agent 7: Merge content and table structure into final operation object
"""
def agent_7_synthesize(operation_data: dict, structure_data: dict, table_data: dict) -> dict:
    combined = {"operation_type": operation_data["operation_type"], "details": {}}
    combined["details"].update(structure_data.get("details", {}))
    for key in ["departments_and_institutions", "laws_and_ordinances"]:
        if table_data.get(key):
            if "related_institutional_and_legal_framework" not in combined["details"]:
                combined["details"]["related_institutional_and_legal_framework"] = {}
            combined["details"]["related_institutional_and_legal_framework"][key] = table_data[key]
    return combined

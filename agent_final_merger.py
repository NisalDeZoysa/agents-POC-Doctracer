"""
Final Merging Agent
Input: metadata dict, and amendment changes from multiple agents
Output: Final JSON file
"""
import json

def agent_merge_all(metadata: dict, changes: list, output_path: str):
    result = {
        "metadata": metadata,
        "changes": changes
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
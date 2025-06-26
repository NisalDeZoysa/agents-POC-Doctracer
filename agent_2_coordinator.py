
# agent_2_coordinator.py
"""
Agent 2: Coordinator Agent
Input: Structured text
Output: Dictionary: metadata, part1, part2, part3
"""
def agent_2_coordinate(structured_text: str) -> dict:
    lines = structured_text.splitlines()
    metadata_text = []
    part1, part2, part3 = [], [], []
    state = "metadata"

    for line in lines:
        if "=== CHANGE 1 ===" in line:
            state = "part1"
            continue
        elif "=== CHANGE 2 ===" in line:
            state = "part2"
            continue
        elif "=== CHANGE 3 ===" in line:
            state = "part3"
            continue

        if state == "metadata":
            metadata_text.append(line)
        elif state == "part1":
            part1.append(line)
        elif state == "part2":
            part2.append(line)
        elif state == "part3":
            part3.append(line)

    return {
        "metadata": "\n".join(metadata_text),
        "part1": "\n".join(part1),
        "part2": "\n".join(part2),
        "part3": "\n".join(part3),
    }

from agent_1_text_extractor import agent_1_extract
from agent_2_coordinator import agent_2_coordinate
from agent_3_metadata_extractor import agent_3_metadata
from agent_4_structure_identifier import agent_4_identify_operations
from agent_5_content_extractor import agent_5_extract_structure
from agent_6_table_extractor import agent_6_extract_tables
from agent_7_final_synthesizer import agent_7_synthesize
from agent_final_merger import agent_merge_all

# Replace this with your actual LLM API wrapper
def llm_generate(prompt: str) -> dict:
    import openai, json
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return json.loads(response.choices[0].message["content"])

# 1. Extract text from PDF
text = agent_1_extract("gota-amendment.pdf")

# 2. Coordinate and segment
segments = agent_2_coordinate(text)

# 3. Extract metadata
metadata = agent_3_metadata(segments["metadata"], llm_generate)

# 4. Process each amendment part
all_changes = []
for part_key in ["part1", "part2", "part3"]:
    blocks = agent_4_identify_operations(segments[part_key], llm_generate)
    for block in blocks:
        op = block
        struct = agent_5_extract_structure(op["text"], llm_generate)
        tables = agent_6_extract_tables(op["text"], llm_generate)
        final = agent_7_synthesize(op, struct, tables)
        all_changes.append(final)

# 5. Merge and export
agent_merge_all(metadata, all_changes, "final_output.json")

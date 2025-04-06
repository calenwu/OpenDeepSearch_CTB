import json
import os

def trim_jsonl_file(input_path, max_lines=300):
    # Read all lines up to max_lines
    with open(input_path, 'r') as f:
        lines = []
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            lines.append(line.strip())
    
    # Create backup of original file
    backup_path = input_path + '.backup'
    if not os.path.exists(backup_path):
        os.rename(input_path, backup_path)
    
    # Write trimmed content back to original file
    with open(input_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    
    print(f"Successfully trimmed file to {len(lines)} lines")
    print(f"Original file backed up to: {backup_path}")

if __name__ == "__main__":
    input_file = "/Users/owen/Projects/datathon25/OpenDeepSearch_CTB/output/fireworks_ai__accounts__fireworks__models__llama-v3p3-70b-instruct/codeact/frames_test_set/fireworks_ai__accounts__fireworks__models__llama-v3p3-70b-instruct__codeact__frames_test_set__trial0.jsonl"
    trim_jsonl_file(input_file) 
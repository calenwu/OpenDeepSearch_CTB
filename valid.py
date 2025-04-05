import json
with open('/Users/georgye/Documents/repos/OpenDeepSearch_CTB/output/fireworks_ai__accounts__fireworks__models__qwq-32b/codeact/frames_test_set/fireworks_ai__accounts__fireworks__models__qwq-32b__codeact__frames_test_set__trial0.jsonl', 'r') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except Exception as e:
            print(f"Error on line {i}: {e}")
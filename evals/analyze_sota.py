import json
import os
import sys

# Get the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the FRAMES benchmark JSONL file
# File is located in the datasets directory relative to the script location
INPUT_FILE = os.path.join(SCRIPT_DIR, "datasets", "fireworks_ai_accounts_fireworks_models_deepseek_r1_codeact_frames.jsonl")
# Place output in the same directory as the input file
OUTPUT_FILE = os.path.join(os.path.dirname(INPUT_FILE), "ODS_failure_analysis.md")

# Hardcoded list of wrong question IDs (simulate 203 wrong answers).
# (Replace these numbers with the actual wrong question IDs from your evaluation.)
WRONG_IDS = list(set([
    5, 15, 19, 28, 32, 44, 46, 52, 53, 54, 55, 58, 62, 65, 70, 72, 74, 81, 82, 84,
    86, 90, 94, 95, 97, 100, 105, 109, 111, 115, 119, 120, 122, 123, 125, 126,
    131, 134, 136, 139, 144, 147, 152, 153, 155, 158, 162, 163, 165, 166, 170,
    171, 173, 175, 177, 180, 183, 185, 187, 188, 189, 190, 193, 194, 197, 201,
    203, 205, 206, 207, 208, 210, 212, 214, 215, 218, 220, 221, 223, 224, 226,
    228, 229, 230, 233, 234, 237, 238, 239, 240, 241, 244, 245, 248, 249, 252,
    253, 254, 255, 256, 259, 260, 261, 262, 265, 267, 270, 271, 275, 277, 278,
    279, 280, 282, 285, 288, 289, 290, 292, 293, 298, 299, 302, 303, 304, 308,
    309, 311, 312, 314, 317, 318, 320, 321, 322, 323, 324, 325, 327, 329, 330,
    331, 332, 335, 337, 338, 340, 341, 342, 344, 345, 348, 351, 353, 355, 358,
    359, 360, 361, 366, 369, 370, 371, 373, 374, 376, 378, 380, 382, 385, 388,
    389, 390, 392, 393, 395, 396, 397, 398, 400, 404, 406, 408, 409, 411, 412,
    415, 416, 418, 419, 420, 422, 423, 424, 425, 426, 427, 430, 431, 433, 437,
    440, 442, 444, 446, 447, 448, 451, 452, 454, 455, 456, 458, 460, 461, 462,
    463, 466, 467, 470, 472, 473, 475, 477, 479, 480, 481, 483, 486, 488, 489,
    492, 493, 495, 496, 497, 499
]))

# Hardcoded mapping of failure categories to wrong question IDs.
# Adjust these lists to match your error analysis.
CATEGORIES = {
    "Incomplete Multi-Hop Reasoning": [
        55, 72, 81, 82, 90, 97, 105, 115, 125, 144,
        158, 170, 180, 185, 189, 190, 193, 230, 238, 259, 298, 324, 344, 345, 395
    ],
    "Incorrect Answer Grounding": [
        15, 19, 28, 32, 46, 86, 119, 131, 139, 147,
        165, 166, 175, 183, 187, 194, 203, 205, 206, 207, 214, 215, 223, 226, 234,
        237, 240, 241, 248, 249, 252, 253, 254, 255, 256, 262, 267, 275, 278, 279,
        280, 282, 288, 289, 290, 293, 299, 302, 303, 304, 308, 311, 312, 317, 318,
        320, 323, 330, 331, 332, 335, 338, 340, 341, 342, 348, 353, 355, 358, 359,
        361, 369, 371, 374, 376, 382, 388, 389, 390, 392, 393, 396, 398, 400, 406,
        408, 409, 411, 412, 416, 418, 420, 422, 423, 424, 425, 431, 433, 440, 442,
        444, 446, 447, 452, 454, 456, 458, 460, 461, 462, 463, 470, 472, 475, 477,
        479, 480, 481, 483, 486, 488, 489, 492, 493, 495, 496, 497
    ],
    "Suboptimal Search Queries": [
        5, 52, 53, 54, 58, 62, 65, 70, 74, 84,
        94, 95, 100, 109, 111, 122, 123, 126, 134, 136, 153, 155, 162, 163, 171,
        173, 177, 185, 188, 205, 210, 212, 218, 220, 221, 228, 229, 233, 244, 245,
        261, 265, 270, 271, 277, 279, 280, 285, 292, 298, 309, 314, 320, 327, 329,
        337, 342, 351, 358, 360, 366, 370, 378, 380, 385, 389, 390, 397, 408, 419,
        420, 425, 426, 427, 430, 437, 446, 448, 451, 455, 466, 467, 470, 473, 479,
        480, 483, 488, 489, 493, 495, 497, 499
    ],
    "Misinterpretation or Logic Errors": [
        28, 32, 197, 217, 258, 295, 311, 517  # Example IDs; adjust as needed.
    ],
    "Code Execution / Parsing Issues": [
        46, 105, 119, 144, 193, 229, 238, 260, 270, 314, 335, 355, 409, 444
    ],
    "Other": [
        # Any remaining IDs that do not fit the above categories.
    ]
}

# We'll assume each line in the JSONL file corresponds to a question with an implicit ID equal to its line number.
# This script extracts records whose line number is in WRONG_IDS.
wrong_details = {}

try:
    with open(INPUT_FILE, "r", encoding="utf-8") as fin:
        for idx, line in enumerate(fin, start=1):
            if idx not in WRONG_IDS:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            wrong_details[idx] = {
                "question": record.get("original_question", "").strip(),
                "model_answer": record.get("answer", "").strip(),
                "true_answer": record.get("true_answer", "").strip(),
                "reasoning": record.get("intermediate_steps", "").strip()
            }
except FileNotFoundError:
    print(f"Error: Could not find input file '{INPUT_FILE}'")
    print("Please place the JSONL file in the same directory as this script or update the INPUT_FILE path.")
    exit(1)

# Calculate the contribution of each category
category_contributions = {category: len([qid for qid in ids if qid in wrong_details]) for category, ids in CATEGORIES.items()}

# Write the Markdown report
with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
    fout.write("# Wrong Answers Grouped by Failure Category\n\n")
    
    # Write the category contributions
    fout.write("## Category Contributions\n\n")
    total_wrong_answers = sum(category_contributions.values())
    for category, count in category_contributions.items():
        contribution_percentage = (count / total_wrong_answers * 100) if total_wrong_answers > 0 else 0
        fout.write(f"- **{category}**: {count} wrong answers ({contribution_percentage:.2f}%)\n")
    
    fout.write("\n")  # Newline after contributions
    for category, ids in CATEGORIES.items():
        # Filter to only those IDs for which we have details
        valid_ids = [qid for qid in ids if qid in wrong_details]
        if not valid_ids:
            continue
        fout.write(f"## {category}\n\n")
        for qid in sorted(valid_ids):
            detail = wrong_details[qid]
            fout.write(f"### Question ID: {qid}\n\n")
            fout.write(f"**Full Question:** {detail['question']}\n\n")
            fout.write(f"**Model's Final Answer:** {detail['model_answer']}\n\n")
            fout.write(f"**Ground Truth Answer:** {detail['true_answer']}\n\n")
            fout.write("**Full Reasoning Trace:**\n\n")
            fout.write("```\n")
            fout.write(detail["reasoning"])
            fout.write("\n```\n\n")
    fout.write("\n")  # Final newline

print(f"Markdown report saved to {OUTPUT_FILE}")

import json
import re

def format_jsonl(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            data = json.loads(line)
            
            instruction = data.get('instruction', '')
            golden_answer = data.get('gold_answer', '')
            model_answer = data.get('model_answer', '')

            # Search for patterns <ANSWER> and </ANSWER> to extract the answer
            match = re.search(r'<ANSWER>(.*?)</ANSWER>', model_answer, re.DOTALL)  # handles <ANSWER>...</ANSWER>
            if not match:
                # Try to match only after <ANSWER> if no closing tag </ANSWER> is found
                match = re.search(r'<ANSWER>(.*)', model_answer, re.DOTALL)

            if match:
                extracted_answer = match.group(1).strip()
            else:
                extracted_answer = ""

            # Create a new object with only instruction, golden-answer, and extracted-answer
            new_data = {
                'instruction': instruction,
                'golden-answer': golden_answer,
                'extracted-answer': extracted_answer
            }

            # Write the new JSON line to the output file
            outfile.write(json.dumps(new_data) + '\n')

# Usage example:
input_file = 'eval_output0.jsonl'   # Replace with your actual file path
output_file = 'formatted_output.jsonl'  # Replace with your desired output file path
format_jsonl(input_file, output_file)
import json


def process_jsonl(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        skipped_count = 0
        for line in infile:
            # Parse each JSON line
            data = json.loads(line.strip())
            
            # Skip this datapoint if there's an error
            if 'error' in data:
                skipped_count += 1
                continue
            
            # Extract the question from the instruction
            instruction_parts = data['instruction'].split('\n')
            question = instruction_parts.pop()  # Remove and get the last line as the question
            instruction = '\n'.join(instruction_parts).strip()  # Join the remaining parts as instruction
            
            # Create new structure with four fields
            new_data = {
                'instruction': instruction,
                'question': question,
                'gold_answer': data['golden-answer'],
                'answer': data['extracted-answer']
            }
            
            # Write the new structure to the output file
            json.dump(new_data, outfile)
            outfile.write('\n')
    
    print(f"Processed file. Skipped {skipped_count} datapoints due to errors.")

# Usage
"""input_file = 'formatted_output.jsonl'
output_file = 'answer_finetuned.jsonl'
process_jsonl(input_file, output_file)"""

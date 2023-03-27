import json
import argparse
def bio_to_jsonl(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        sentence = ""
        entities = []
        for line in f_in:
            line = line.strip()
            if not line:
                if sentence:
                    json_data = {
                        "text": sentence,
                        "spans": entities
                    }
                    f_out.write(json.dumps(json_data) + "\n")
                    sentence = ""
                    entities = []
            else:
                parts = line.split(" ")
                if(len(parts) == 2):
                    word = parts[0]
                    label = parts[1]
                    if label.startswith("B-"):
                        entity = {"start": len(sentence) , "end": len(sentence) + len(word), "type": label[2:]}
                        entities.append(entity)
                    elif label.startswith("I-"):
                        entities[-1]["end"] = len(sentence) + len(word)
                        
                    elif label.startswith("L-"):
                        entities[-1]["end"] = len(sentence) + len(word)
                    sentence += word + " "
        if sentence:
            json_data = {
                "text": sentence.strip(),
                "spans": entities
            }
            f_out.write(json.dumps(json_data) + "\n")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a BIO file to JSONL format.')
    parser.add_argument('input_file', type=str, help='Path to the input BIO file')
    parser.add_argument('output_file', type=str, help='Path to the output JSONL file')
    args = parser.parse_args()

    bio_to_jsonl(args.input_file, args.output_file)

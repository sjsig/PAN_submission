import os
import json
def generate_output(output_dir, results_dir, lang):
    
    result_file = os.path.join(results_dir, f'{lang}.json')
    with open(result_file) as json_file:
        results = json.load(json_file)
    print(results["predictions"])
    print(results["uids"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, default="./")
    parser.add_argument('--results_dir', type=str, default="./results")
    args = parser.parse_args()

    generate_output(args.output_dir, args.results_dir, 'en')

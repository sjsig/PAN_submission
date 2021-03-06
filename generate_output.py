import os
import json
import argparse 

def generate_output(output_dir, results_dir, lang):
    output_dir = os.path.join(output_dir, lang)
    if(not os.path.exists(args.output_dir)):
        os.makedirs(args.output_dir)
    
    result_file = os.path.join(results_dir, f'{lang}.json')
    with open(result_file) as json_file:
        results = json.load(json_file)
    print(results["predictions"])
    print(results["uids"])

    for a in range(len(results["uids"])):
        author_file = os.path.join(output_dir, f'{results["uids"][a]}.xml')
        with open(author_file, 'w') as the_file:
            the_file.write(f"<author id=\"{results['uids'][a]}\" lang=\"{lang}\" type=\"{results['predictions'][a]}\"/>")
        the_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, default="./")
    parser.add_argument('--results_dir', type=str, default="./results")
    args = parser.parse_args()

    

    generate_output(args.output_dir, args.results_dir, 'en')

from pathlib import Path
import os
import json

def makeTrainingFiles(path):
    json_files = [a_json for a_json in os.listdir(path) if a_json.endswith('.json')]
    for file in json_files:
        with open(path + '/' + file, 'r') as fp:
            dictList = json.load(fp)
            for dict in dictList:
                for sentence in dict['body']:
                    # print('Need to change to and from key recognition')

                    if dict['from'] == 'Jeb Bush':
                        filename = 'data/fromJeb.txt'
                    else:
                        filename = 'data/toJeb.txt'
                    with open(filename, 'a') as file:
                        file.write(sentence)


def main():
    output_file = Path("output")
    output_file_string = "output"
    if output_file.is_dir():
        makeTrainingFiles(output_file_string)
    else:
        print('No valid output folder available')

if __name__ == '__main__':
    main()

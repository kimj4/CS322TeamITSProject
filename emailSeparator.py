'''
This file aims to run through all the emails in the output/ folder and extract
emails and separate them into two bins: jeb, non-jeb
Save this file in two different json files.
'''

import os
import json

def separate():
    directory_name = 'output'
    directory = os.fsencode(directory_name)
    output_directory = 'separatedOutput'

    data = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            try:
                with open('output/' + filename, 'r') as f:
                    data.extend(json.load(f))
            except:
                continue

    jebs = [x for x in data if ('jeb' in x['from'].lower()) ]
    nonjebs = [x for x in data if ('jeb' not in x['from'].lower())]
    # print(len(jebs))
    print(len(data))

    with open('separatedOutput/jeb.json', 'w') as f:
        json.dump(jebs, f, indent=4)

    with open('separatedOutput/nonjeb.json', 'w') as f:
        json.dump(nonjebs, f, indent=4)
    # for e in data:
    #     if 'jeb' in e['from'].lower():
    #         jebs.append(e)


def main():
    separate()

if __name__ == '__main__':
    main()

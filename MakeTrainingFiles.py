from pathlib import Path
import os, os.path
import json
import multiprocessing
import math

def makeTrainingFiles(path, from_output_name, to_output_name, start, end):
    '''
    gets the bodies of each email within the start end range where
    start.json to end.json where start and end are integers
    '''
    json_files = [str(x) + '.json' for x in range(start,end + 1)]
    # json_files = [a_json for a_json in os.listdir(path) if a_json.endswith('.json')]
    from_jeb_string = ''
    to_jeb_string = ''
    for file in json_files:
        if os.path.isfile(path + '/' + file):
            with open(path + '/' + file, 'r') as fp:
                dictList = json.load(fp)
                for dict in dictList:
                    sentence = dict['body']
                    # print(sentence)
                    # print('Need to change to and from key recognition')

                    if dict['from'] == 'Jeb Bush':
                        from_jeb_string += '\n' + dict['body']
                    else:
                        to_jeb_string += '\n' + dict['body']
    with open('data/' + from_output_name + '.txt', 'w+') as file:
        file.write(from_jeb_string)
    with open('data/' + to_output_name + '.txt', 'w+') as file:
        file.write(to_jeb_string)

    print('[{}, {}] is done'.format(start, end))

    return

def list_distribution(num_items, total):
    per_item = math.ceil((1.0 * total) / num_items)
    l = []
    for i in range(num_items):
        if total >= per_item:
            l.append(per_item)
            total -= per_item
        else:
            l.append(total)
            total = 0
    if total > 0:
        print('ERROR in list_distribution: ')
    return l

def launch_on_multiple_cores(source_path_name, from_output_name, to_output_name):
    '''
    copies the body into a bunch of temp files and combines them into one at the
    end.
    '''
    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool( cpu_count )
    tasks = []
    max_t = cpu_count

    # file names are tmp_toJeb_0
    temp_to_file_names = ['tmp_' + from_output_name + '_' + str(x) for x in range(cpu_count)]
    # file names are tmp_fromJeb_0
    temp_from_file_names = ['tmp_' + to_output_name + '_' + str(x) for x in range(cpu_count)]

    num_total_in_dir = len([name for name in os.listdir(source_path_name) if os.path.isfile(source_path_name + '/' + name)])
    # print(num_total_in_dir)
    nums_to_proc = list_distribution(cpu_count, num_total_in_dir)

    tNum = 0
    cur_start = 0
    while tNum < max_t:
        # print(cur_start, cur_start + nums_to_proc[tNum] - 1)
        tasks.append( (source_path_name, temp_from_file_names[tNum], temp_to_file_names[tNum], cur_start, cur_start + nums_to_proc[tNum] - 1) )
        cur_start = cur_start + nums_to_proc[tNum]
        tNum += 1

    results = []
    for t in tasks:
        results.append( pool.apply_async( makeTrainingFiles, t ) )

    r = []
    for result in results:
        r.append(result.get())

    for f in temp_to_file_names:
        fname = 'data/' + f + '.txt'
        with open(fname, 'r') as f1:
            with open('data/' + to_output_name + '.txt', 'a+') as f2:
                f2.write(f1.read())
        os.remove(fname)

    for f in temp_from_file_names:
        fname = 'data/' + f + '.txt'
        with open(fname, 'r') as f1:
            with open('data/' + from_output_name + '.txt', 'a+') as f2:
                f2.write(f1.read())
        os.remove(fname)



def main():
    launch_on_multiple_cores('output', 'fromJeb', 'toJeb')

    # output_file = Path("output")
    # output_file_string = "output"
    # if output_file.is_dir():
    #     makeTrainingFiles(output_file_string)
    # else:
    #     print('No valid output folder available')

if __name__ == '__main__':
    main()

import sys

def main(args):
    with open(args[0], 'r+') as f:
        file_1 = f.read().rstrip().split('\n')
    with open(args[1], 'r+') as f:
        file_2 = f.read().rstrip().split('\n')

    result = []
    for line in file_1:
        if 'same' in args:
            if line in file_2:
                result.append(line)
        elif 'diff' in args:
            if line not in file_2:
                result.append(line)
        else:
            pass

    for r in result:
        print(r)
    print(len(result))


if __name__ == '__main__':
    main(sys.argv[1:])
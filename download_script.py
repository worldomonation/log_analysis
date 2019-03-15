import requests
import sys


def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.rstrip().split('\r\n')


def main(args):
    target = args[0]
    if 'http' in target:
        logs = download_file(target)
    elif 'file' in target:
        local_file_name = target.split('file://')[1]
        with open(local_file_name, 'r+') as local_logs:
            logs = local_logs.read().rstrip().split('\n')
    else:
        logs = []

    results = []
    search_term = args[1]
    for entry in logs:
        if search_term in entry:
            results.append(entry)

    output_file_name = args[2]
    sanitize_string = args[3] or ''
    if results and output_file_name is not None:
        with open(output_file_name, 'w+') as results_file:
            for result in results:
                if len(sanitize_string) > 1:
                    sanitized_result = result.split(sanitize_string)[1]
                elif len(sanitize_string) == 1:
                    sanitized_result = result[result.find(sanitize_string):]
                else:
                    sanitized_result = result
                results_file.write(''.join([sanitized_result, '\n']))


if __name__ == '__main__':
    main(sys.argv[1:])
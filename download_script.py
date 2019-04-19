import requests
import sys

from argparse import Action
from argparse import ArgumentParser


class SanitizeInput(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if 'http' in values or values.startswith('/'):
            setattr(namespace, self.dest, values)
        elif 'file' in values:
            setattr(namespace, self.dest, values.split('file://')[1])
        else:
            raise ValueError('Input file must be http://, https:// or file://.')


def build_parser():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', action=SanitizeInput, default=None, help='Input URL or local file path.')
    parser.add_argument('-f', '--find', action='store', default='', help='String to find in log.')
    parser.add_argument('-o', '--output', action='store', default=None, help='Output file name.')
    parser.add_argument('-s', '--split', action='store', default='', help='String to split matching log entries on.')

    return parser


def download_log_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.rstrip().split('\r\n')
    return None


def open_log_from_local_file(path):
    with open(path, 'r+') as local_logs:
        logs = local_logs.read().rstrip().split('\n')
        return logs
    return None

def main(args):
    parser = build_parser()
    parsed_args, remainder = parser.parse_known_args()

    if 'http' in parsed_args.input:
        logs = download_log_from_url(parsed_args.input)
    elif 'file' in parsed_args.input:
        logs = open_log_from_local_file(parsed_args.input)
    else:
        logs = []

    results = []
    search_term = parsed_args.find
    for entry in logs:
        if search_term in entry:
            results.append(entry)

    output_file_name = parsed_args.output
    split_on = parsed_args.split or ''
    if output_file_name is not None:
        with open(output_file_name, 'w'):
            pass
    if results:
        for result in results:
            if len(split_on) > 1:
                sanitized_result = result.split(split_on)[1]
            elif len(split_on) == 1:
                sanitized_result = result[result.find(split_on):]
            else:
                sanitized_result = result
            if output_file_name is not None:
                with open(output_file_name, 'a') as results_file:
                    results_file.write(''.join([sanitized_result, '\n']))
            else:
                print(sanitized_result)




if __name__ == '__main__':
    # parser = build_parser()
    # parsed_args, remainder = parser.parse_known_args()
    # print(parsed_args)
    main(sys.argv[1:])

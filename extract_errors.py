import re
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Extract and sort ERROR logs from app.log")
    parser.add_argument('--hour', type=int, help="Filter ERROR logs by hour (0-23)")
    return parser.parse_args()

def extract_errors(logfile, hour_filter=None):
    error_lines = []
    pattern = re.compile(r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - ERROR:.*$')

    with open(logfile, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                timestamp_str = match.group('timestamp')
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                if hour_filter is None or timestamp.hour == hour_filter:
                    error_lines.append((timestamp, line.strip()))

    return sorted(error_lines, key=lambda x: x[0])

def save_errors(errors, output_file):
    with open(output_file, 'w') as f:
        for _, line in errors:
            f.write(line + '\n')

def main():
    args = parse_args()
    logfile = 'app.log'
    output_file = 'errors.txt'
    errors = extract_errors(logfile, args.hour)
    save_errors(errors, output_file)
    print(f"Extracted {len(errors)} error(s) to {output_file}")

if __name__ == '__main__':
    main()

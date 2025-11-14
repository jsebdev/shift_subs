import sys
import re
from datetime import timedelta, datetime

def parse_time(timestamp):
    return datetime.strptime(timestamp, "%H:%M:%S,%f")

def format_time(dt):
    return dt.strftime("%H:%M:%S,%f")[:-3]  # Trim to milliseconds

def shift_timestamp_line(line, delta):
    time_match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line)
    if not time_match:
        return line
    start, end = time_match.groups()
    new_start = format_time(parse_time(start) + delta)
    new_end = format_time(parse_time(end) + delta)
    return f"{new_start} --> {new_end}"

def shift_subtitles(input_path, output_path, seconds_shift):
    delta = timedelta(seconds=seconds_shift)

    with open(input_path, 'r', encoding='utf-8', errors='replace') as infile:
        lines = infile.readlines()

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if '-->' in line:
                shifted_line = shift_timestamp_line(line.strip(), delta)
                outfile.write(shifted_line + '\n')
            else:
                outfile.write(line)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python shift_subs.py input.srt output.srt [seconds]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    shift_seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 1

    shift_subtitles(input_file, output_file, shift_seconds)


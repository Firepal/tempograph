from file_parser import parse_file
from clicktrack import make_click_track
f = parse_file("inputs/linear.tg")
for i in f:
    print(i)
print(make_click_track(f, "click.wav"))
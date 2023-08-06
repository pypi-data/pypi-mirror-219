import json
import csv


def parse_text(source):
    for line in source:
        yield {'value': line}


def parse_csv(source):
    reader = csv.DictReader(source)
    for entry in reader:
        yield entry


def json_rows(source):
    for line in source:
        yield json.loads(line)

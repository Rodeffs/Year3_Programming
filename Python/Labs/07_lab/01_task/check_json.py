from jsonschema import validate
from argparse import ArgumentParser
import json


def main():
    
    parser = ArgumentParser()
    parser.add_argument("-s", required=True, help="the json schema to check the files by")
    parser.add_argument("-f", required=True, help="the json file to check")
    args = parser.parse_args()

    with open(args.f) as file_json, open(args.s) as schema:
        try:
            validate(json.load(file_json), json.load(schema))
            print("This JSON file is valid")
        except:
            print("This JSON file is not valid")


if __name__ == "__main__":
    main()

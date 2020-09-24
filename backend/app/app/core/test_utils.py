from os import listdir
from os.path import isfile, join


def get_input_output_file_sets(dir_path: str, fixtures_condition_map: dict):
    scenarios = {}
    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            filename_parts = f.split('-')
            if len(filename_parts) == 3:
                key = filename_parts[1]
                i_or_o = filename_parts[2]
                if key not in scenarios:
                    value = []
                    value.insert(index_to_insert(i_or_o), f)
                    scenarios[key] = value
                else:
                    existing = scenarios.get(key)
                    existing.insert(index_to_insert(i_or_o), f)

    fixtures = []
    for key in scenarios:
        value = scenarios[key]
        value.append(fixtures_condition_map.get(key))
        fixtures.append(tuple(value))

    return fixtures


def index_to_insert(i_or_o: str):
    if i_or_o == "input.json":
        return 0
    elif i_or_o == "output.json":
        return 1

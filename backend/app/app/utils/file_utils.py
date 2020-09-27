import json


class FileUtils:

    @staticmethod
    def load_params_from_json(json_path) -> dict:
        with open(json_path) as f:
            x = json.load(f)
            return x

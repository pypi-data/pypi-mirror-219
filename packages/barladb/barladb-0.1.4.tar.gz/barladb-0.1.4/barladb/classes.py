import json

class Json:
    @staticmethod
    def get(filepath: str):
        with open(filepath + ".json", "r") as file:
            return json.load(file)
    @staticmethod
    def save(filepath: str, data: str):
        with open(filepath + ".json", "w") as file:
            json.dump(data, file, ensure_ascii=True, indent=2)

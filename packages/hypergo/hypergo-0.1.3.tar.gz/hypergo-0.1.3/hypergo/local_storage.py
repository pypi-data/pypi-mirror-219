from hypergo.storage import Storage


class LocalStorage(Storage):
    def load(self, file_name: str) -> str:
        with open(file_name, "r", encoding="utf-8") as file:
            content: str = file.read()
        return content

    def save(self, file_name: str, content: str) -> None:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)

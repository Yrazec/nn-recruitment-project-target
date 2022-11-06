class Parser:
    @staticmethod
    def validate_string_start(string: str) -> str:
        while True:
            if string[0].isalnum():
                break
            else:
                string = string[1:]
        return string

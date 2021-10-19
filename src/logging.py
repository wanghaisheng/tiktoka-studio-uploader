class Log:
    def __init__(self, debug: bool = False):
        self.enable_debug = debug

    def debug(self, text: str) -> None:
        if self.enable_debug:
            text.encode(encoding="UTF-8", errors="ignore")
            print(f"DEBUG: {text}")

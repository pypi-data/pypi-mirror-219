class Parser:
    def __init__(self, config: dict) -> None:
        self._config = config

        self._lines = []

        self._block = False
        self._block_len = 0

        self._listing = False

    def parse(self, path: str) -> str:
        self._lines = []
        with open(path, "r") as file:
            for line in file.readlines():
                self.parse_line(line)
        return "".join(self._lines)

    def parse_line(self, line: str):
        _line = line.lstrip()
        # NORMAL LOGIC
        if _line.startswith(self._config["inline_syntax"]):
            self._lines.append(_line.lstrip(self._config["inline_syntax"]) + "\n")
        # END NORMAL LOGIC

        # BLOCK LOGIC
        elif _line.startswith(self._config["block_syntax_start"]):
            self._block = True
            temp = _line.lstrip(self._config["block_syntax_start"])
            if len(temp) > 0:
                self._lines.append(temp)
        elif _line.strip().endswith(self._config["block_syntax_end"]) and self._block:
            self._block = False
            temp = _line.strip().rstrip(self._config["block_syntax_end"])
            if len(temp) > 0:
                self._lines.append(temp)
        elif self._block:
            if len(_line) == 0:
                self._lines.append("\n")
            else:
                self._lines.append(_line)
        # END BLOCK LOGIC

        # LISTING LOGIC
        elif _line.startswith(self._config["listing_syntax_start"]):
            self._listing = True
            self._lines.append("```")
            temp = _line.lstrip(self._config["listing_syntax_start"])
            if len(temp) > 0:
                self._lines.append(temp)
        elif (
            _line.strip().endswith(self._config["listing_syntax_end"]) and self._listing
        ):
            self._listing = False
            temp = _line.strip().rstrip(self._config["listing_syntax_end"])
            if len(temp) > 0:
                self._lines.append(temp)
            self._lines.append("```\n")
        elif self._listing:
            self._lines.append(line)  # unstripped line because of code indentation
        # END LISTING LOGIC

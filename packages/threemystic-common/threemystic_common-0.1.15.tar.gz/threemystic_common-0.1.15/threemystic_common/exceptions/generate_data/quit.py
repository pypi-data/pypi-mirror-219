
class quit_exception(Exception):
    "Raised when someone quites out of generate data"
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "User Quit"
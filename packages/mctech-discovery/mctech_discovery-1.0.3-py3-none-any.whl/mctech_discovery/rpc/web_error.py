from typing import Dict, List


class WebError(RuntimeError):
    def __init__(self,
                 message: str,
                 code: str = None,
                 desc: str = None,
                 headers: Dict[str, str] = {},
                 status: int = 400):
        super().__init__(message)
        self.code = code
        self.desc = desc
        self.headers = headers
        self.status = status
        self.details: List[str] = []

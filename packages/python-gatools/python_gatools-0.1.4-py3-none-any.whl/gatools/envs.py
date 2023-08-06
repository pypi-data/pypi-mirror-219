from pathlib import Path
from dotenv import load_dotenv

__ALL__ = ["load_fenv"]


def load_fenv(path: str, fname: str = ".env"):
    load_dotenv(Path(path).parent / fname)

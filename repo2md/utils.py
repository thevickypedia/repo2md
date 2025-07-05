import logging
import os

LANGUAGE_EXTENSIONS = {
    "python": [".py"],
    "javascript": [".js", ".jsx"],
    "typescript": [".ts", ".tsx"],
    "java": [".java"],
    "csharp": [".cs"],
    "c++": [".cpp", ".h"],
    "c": [".c", ".h"],
    "ruby": [".rb"],
    "go": [".go"],
    "php": [".php"],
    "html": [".html", ".htm"],
    "css": [".css"],
    "bash": [".sh"],
    "kotlin": [".kt", ".kts"],
    "swift": [".swift"],
    "rust": [".rs"],
    "scala": [".scala"],
    "perl": [".pl"],
    "lua": [".lua"],
    "dart": [".dart"],
    "elixir": [".ex", ".exs"],
    "haskell": [".hs"],
    "shell": [".sh", ".bash"],
    "powershell": [".ps1"],
    "sql": [".sql"],
    "pascal": [".pas"],
    "objective-c": [".m", ".h"],
    "r": [".r"],
    "julia": [".jl"],
}

IGNORE_FILES = [
    ".gitignore",
    "readme.md",
    "license",
    "requirements.txt",
    "setup.py",
    "pyproject.toml",
    "pipfile",
    "pipfile.lock",
    "package.json",
    "yarn.lock",
    ".dockerignore",
    ".pre-commit-config.yaml",
    "makefile",
    "settings.gradle",
    "build.gradle",
    "pom.xml",
    "build.sbt",
    "cargo.toml",
    "cargo.lock",
    "gradlew",
    "gradlew.bat",
    ".gitattributes",
    "changelog.md",
    ".java-version",
    "openapi.yml",
    "openapi.yaml",
    "openapi.json",
    "swagger.yml",
    "swagger.yaml",
    "swagger.json",
]

IGNORE_DIRECTORIES = [
    "__pycache__",
    ".git",
    ".idea",
    "venv",
    ".github",
    "node_modules",
    ".ds_store",
    ".vscode",
    ".pytest_cache",
    "build",
    "dist",
    "docs",
    "tests",
    "gradle",
]

IGNORE_LIST = IGNORE_DIRECTORIES + IGNORE_FILES

LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(
    fmt=logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s - Line: %(lineno)d - %(message)s",
        datefmt="%b-%d-%Y %H:%M:%S",
    )
)
if os.environ.get("DEBUG", "").lower() in ("1", "true"):
    LOGGER.setLevel(level=logging.DEBUG)
else:
    LOGGER.setLevel(level=logging.INFO)
LOGGER.addHandler(hdlr=handler)

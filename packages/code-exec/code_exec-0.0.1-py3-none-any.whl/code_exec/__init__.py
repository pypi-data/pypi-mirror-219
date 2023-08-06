from src.code_exec.checker import StaticCodeChecker
from src.code_exec.executor import CodeExecutor

DEFAULT_UNSAFE_BUILTINS = [
    "__import__",
    "exec",
    "eval",
    "quit",
    "exit",
    "breakpoint",
    "globals",
    "locales"
]

__safe_executor = CodeExecutor(
    static_checker=StaticCodeChecker(
        no_import=True,
        no_private_attr_access=True,
        unsafe_calls=DEFAULT_UNSAFE_BUILTINS,
    )
)


def safe_exec(source: str, filename=CodeExecutor.FILENAME_STRING, globals_: dict | None = None,
              locals_: dict | None = None):
    __safe_executor.exec(source=source, filename=filename, globals_=globals_, locals_=locals_,
                         blacklist=DEFAULT_UNSAFE_BUILTINS)


def safe_eval(source: str, filename=CodeExecutor.FILENAME_STRING, globals_: dict | None = None,
              locals_: dict | None = None):
    return __safe_executor.exec(source=source, filename=filename, globals_=globals_, locals_=locals_,
                                blacklist=DEFAULT_UNSAFE_BUILTINS)


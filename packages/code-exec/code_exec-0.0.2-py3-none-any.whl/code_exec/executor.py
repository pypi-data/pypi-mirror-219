import builtins
import inspect
from copy import copy

from .checker import StaticCodeChecker


class CodeExecutor(object):
    MODE_EXEC = "exec"
    MODE_EVAL = "eval"

    FILENAME_STRING = "<string>"
    FILENAME_UNKNOWN = "<unknown>"

    def __init__(self, static_checker: StaticCodeChecker | None = None):
        self._static_checker = static_checker

    @staticmethod
    def get_builtins(whitelist=None, blacklist=None):
        if whitelist:
            all_builtins = {
                k: v
                for k, v in builtins.__dict__.items() if k in whitelist
            }
        elif blacklist:
            all_builtins = {
                k: v
                for k, v in builtins.__dict__.items() if k not in blacklist
            }
        else:
            all_builtins = copy(builtins.__dict__)
        return all_builtins

    def compile(self, source, filename, mode, **kwargs):
        if self._static_checker:
            ast_ = self._static_checker.parse_and_check(source=source, filename=filename, mode=mode)
            return compile(ast_, filename=filename, mode=mode, **kwargs)
        return compile(source, filename=filename, mode=mode, **kwargs)

    def execute(self, source, filename, mode, globals_=None, locals_=None,
                whitelist=None, blacklist=None, **compile_kwargs):
        if globals_ is None:
            globals_ = {}

        if locals_ is None:
            locals_ = {}

        if globals_.get("__builtins__", None) is None:
            globals_["__builtins__"] = self.get_builtins(whitelist=whitelist, blacklist=blacklist)

        if not inspect.iscode(source):
            source = self.compile(source=source, filename=filename, mode=mode, **compile_kwargs)

        if mode == self.MODE_EXEC:
            return exec(source, globals_, locals_)
        elif mode == self.MODE_EVAL:
            return eval(source, globals_, locals_)
        else:
            raise ValueError(f"unsupported mode: {mode}")

    def exec(self, source, filename, globals_=None, locals_=None, whitelist=None, blacklist=None,
             **compile_kwargs):
        return self.execute(source=source, filename=filename, mode=self.MODE_EXEC, globals_=globals_, locals_=locals_,
                            whitelist=whitelist, blacklist=blacklist, **compile_kwargs)

    def eval(self, source, filename, globals_=None, locals_=None, whitelist=None, blacklist=None,
             **compile_kwargs):
        return self.execute(source=source, filename=filename, mode=self.MODE_EVAL, globals_=globals_, locals_=locals_,
                            whitelist=whitelist, blacklist=blacklist, **compile_kwargs)

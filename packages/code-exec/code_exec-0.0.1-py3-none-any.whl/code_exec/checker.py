import ast
from _ast import Import, ImportFrom, Attribute, Call, AST
from typing import List


class UnsafeCodeException(RuntimeError):
    pass


class StaticCodeChecker(ast.NodeVisitor):
    def __init__(self, no_private_attr_access: bool = True, no_import: bool = True,
                 unsafe_calls: List[str] | None = None):
        if unsafe_calls is None:
            unsafe_calls = []

        self._unsafe_calls = unsafe_calls
        self._no_import = no_import
        self._no_private_attr_access = no_private_attr_access

    def visit_Import(self, node: Import):
        if self._no_import:
            raise UnsafeCodeException(f"import is not allowed: lineno={node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ImportFrom):
        if self._no_import:
            raise UnsafeCodeException(f"import is not allowed: lineno={node.lineno}")
        self.generic_visit(node)

    def visit_Attribute(self, node: Attribute):
        if self._no_private_attr_access and "__" in node.attr:
            raise UnsafeCodeException(f"private attribute access is not allowed: lineno={node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node: Call):
        if isinstance(node.func, ast.Attribute):
            call_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            call_name = node.func.id
        else:
            self.generic_visit(node)
            return

        if self._no_import and call_name == "__import__":
            raise UnsafeCodeException("import is not allowed", node.lineno)

        if call_name in self._unsafe_calls:
            raise UnsafeCodeException(f"'{call_name}()' is not allowed", node.lineno)

        self.generic_visit(node)

    def parse_and_check(self, source: str, filename='<unknown>', mode='execution') -> AST:
        code_node = ast.parse(source, filename=filename, mode=mode)
        self.visit(code_node)
        return code_node

    @property
    def no_import(self):
        return self._no_import

    @no_import.setter
    def no_import(self, value):
        self._no_import = value

    @property
    def no_private_attr_access(self):
        return self._no_private_attr_access

    @no_private_attr_access.setter
    def no_private_attr_access(self, value):
        self._no_private_attr_access = value

    @property
    def unsafe_calls(self):
        return self._unsafe_calls

    @unsafe_calls.setter
    def unsafe_calls(self, calls: List[str] | None):
        if calls is None:
            self._unsafe_calls = []
        else:
            self._unsafe_calls = calls

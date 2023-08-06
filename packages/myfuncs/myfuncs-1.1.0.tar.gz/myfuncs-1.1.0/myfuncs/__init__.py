import inspect
import subprocess as subproc
import sys
from typing import Dict, List, Optional, Set, Tuple, Union, Any

from logfunc import logf


def nlprint(*args, **kwargs) -> None:
    """Identical to normal print() but also prints an extra \n"""
    print(*args, **kwargs)
    print()


def is_jwt_str(s: str) -> bool:
    """Check if a string is an encrypted JWT"""
    parts = str(s).split('.')
    return len(parts) == 3


@logf(level="info")
def runcmd(cmd: str, output: bool = True, *args, **kwargs) -> Optional[List[str]]:
    """
    Run a command in the shell.

    Args:
        cmd (str): The command to be executed.
        output (bool, optional): Specifies whether to capture and return the output of the command.
            Defaults to True.
        *args: Additional positional arguments to be passed to subprocess.run().
        **kwargs: Additional keyword arguments to be passed to subprocess.run().

    Returns:
        Optional[List[str]]: The captured output of the command as a list of lines if `output` is True.
            None if `output` is False.

    Raises:
        CalledProcessError: If the command exits with a non-zero status and `check=True`.

    """
    if output:
        return subproc.run(
            [c for c in cmd.split()],
            check=True,
            text=True,
            capture_output=True,
            *args,
            **kwargs,
        ).stdout.splitlines()
    else:
        subproc.run(
            [c for c in cmd.split()],
            check=False,
            text=False,
            capture_output=False,
            *args,
            **kwargs,
        )


class ObjInfo:
    """
    A class to gather and print properties of a python object.
    """

    obj: Any
    obj_type: str
    obj_attrs: List[str]
    obj_methods: List[str]
    obj_doc: Optional[str]
    obj_scope: str
    obj_size: int
    obj_mutability: str
    obj_identity: int
    info_attrs: List[str] = [
        "obj",
        "obj_type",
        "obj_attrs",
        "obj_methods",
        "obj_doc",
        "obj_scope",
        "obj_size",
        "obj_mutability",
        "obj_identity",
    ]

    def __init__(self, var: Any):
        """
        Initialize with the object to be inspected
        :param var: The object to inspect
        """
        self.obj = var
        self.obj_type = type(var)
        self.obj_name = var.__name__ if hasattr(var, "__name__") else "N/A"

        self.obj_attrs = sorted(
            attr for attr in dir(var) if not callable(getattr(var, attr))
        )
        self.obj_methods = sorted(
            method for method in dir(var) if callable(getattr(var, method))
        )
        self.obj_doc = inspect.getdoc(var)
        self.obj_scope = (
            "Local"
            if var in inspect.currentframe().f_back.f_locals.values()
            else "Global"
        )
        self.obj_size = sys.getsizeof(var)
        self.obj_mutability = "Mutable" if hasattr(var, "__dict__") else "Immutable"
        self.obj_identity = id(var)
        self.print_info()

    def print_info(self):
        """
        Prints the collected information of the object
        """
        curline = "Object: {} {} {} {} {}".format(
            self.obj_name,
            self.obj_type,
            self.obj_mutability,
            self.obj_scope,
            self.obj_identity,
        )
        nlprint(10 * '=', curline, 10 * '=')

        nlprint("Object __repr__/__str__:", self.obj)
        nlprint("Object Attributes:", " ".join(self.obj_attrs))
        nlprint("Object Methods:", " ".join(self.obj_methods))
        print(20 * '-', 'Object Docstring', 20 * '-')
        print("Object Documentation:", str(self.obj_doc))
        nlprint(len(20 * '-' + ' Object Docstring ' + 20 * '-') * '-')

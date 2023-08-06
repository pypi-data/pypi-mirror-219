""" shil.models
"""
import os
import typing
import subprocess

import pydantic
from fleks.util import lme

from shil.format import shfmt
from shil.console import Panel, Syntax, Text

LOGGER = lme.get_logger(__name__)

Field = pydantic.Field


class BaseModel(pydantic.BaseModel):
    """ """

    def update(self, **kwargs):
        return self.__dict__.update(**kwargs)

    class Config:
        arbitrary_types_allowed = True
        # frozen = True


class Invocation(BaseModel):
    command: typing.Optional[str] = Field()
    stdin: typing.Optional[str] = Field(help="stdin to send to command")
    strict: bool = Field(default=False, help="Fail if command fails")
    shell: typing.Optional[bool] = Field(help="Fail if command fails")
    interactive: bool = Field(default=False, help="Interactive mode")
    large_output: bool = Field(
        default=False, help="Flag for indicating that output is huge"
    )
    log_command: bool = Field(
        default=True,
        help="Flag indicating whether command should be logged when it is run",
    )
    environment: dict = Field(default={})
    log_stdin: bool = Field(default=True)
    system: bool = Field(help='Execute command in "system" mode', default=False)
    load_json: bool = Field(help="Load JSON from output", default=False)

    def __rich_console__(self, console, options):  # noqa
        """
        https://rich.readthedocs.io/en/stable/protocol.html
        """
        yield f"[dim]$[/dim] [b]{self.command}[/b]"

    def __call__(self):
        """ """
        #     if self.log_command:
        #         msg = f"running command: (system={self.system})\n  {self.command}"
        #         LOGGER.warning(msg)
        LOGGER.warning(self.command)
        result = InvocationResult(**self.dict())

        if self.system:
            assert not self.stdin and not self.interactive
            error = os.system(self.command)
            result.update(
                failed=bool(error),
                failure=bool(error),
                success=not bool(error),
                succeeded=not bool(error),
                stdout="<os.system>",
                stdin="<os.system>",
            )
            return result

        exec_kwargs = dict(
            shell=True,
            env={**{k: v for k, v in os.environ.items()}, **self.environment},
        )
        if self.stdin:
            msg = "command will receive pipe:\n{}"
            self.log_stdin and LOGGER.debug(msg.format(self.stdin))
            exec_kwargs.update(
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            LOGGER.critical([self.command, exec_kwargs])
            tmp = subprocess.run(
                self.command.split(),
                shell=self.shell,
                input=self.stdin.encode("utf-8"),
                capture_output=True,
            )
            result.update(
                pid=getattr(tmp, "pid", -1),
                stdout=tmp.stdout.decode("utf-8"),
                stderr=tmp.stderr,
                return_code=tmp.returncode,
                failed=tmp.returncode != 0,
            )
            result.update(
                failure=result.failed,
                succeeded=not result.failure,
                success=not result.failure,
            )
            return result
        else:
            if not self.interactive:
                exec_kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            exec_cmd = subprocess.Popen(self.command, **exec_kwargs)
            exec_cmd.wait()
        if exec_cmd.stdout:
            exec_cmd.hstdout = exec_cmd.stdout
            result.update(
                stdout=(
                    "<LargeOutput>"
                    if self.large_output
                    else exec_cmd.stdout.read().decode("utf-8")
                )
            )
            exec_cmd.hstdout.close()
        else:
            exec_cmd.stdout = "<Interactive>"
            result.update(stdout="<Interactive>")
        if exec_cmd.stderr:
            exec_cmd.hstderr = exec_cmd.stderr
            exec_cmd.stderr = exec_cmd.stderr.read().decode("utf-8")
            exec_cmd.hstderr.close()
            result.update(stderr=exec_cmd.stderr)
        result.pid = exec_cmd.pid
        result.failed = exec_cmd.returncode > 0
        result.succeeded = not result.failed
        result.success = result.succeeded
        result.failure = result.failed
        result.data = loaded_json = None
        if self.load_json:
            if result.failed:
                err = f"{self} did not succeed; cannot return JSON from failure"
                LOGGER.critical(err)
                LOGGER.critical(result.stderr)
                raise RuntimeError(err)
            import json

            try:
                loaded_json = json.loads(result.stdout)
            except (json.decoder.JSONDecodeError,) as exc:
                loaded_json = dict(error=str(exc))
        if self.strict and not result.succeeded:
            LOGGER.critical(f"Invocation failed and strict={self.strict}")
            # raise InvocationError
            LOGGER.critical(result.stderr)
            raise RuntimeError(result.stderr)
        return result


class InvocationResult(Invocation):
    data: typing.Optional[typing.Dict] = Field(
        default=None, help="Data loaded from JSON on stdout"
    )
    failed: bool = Field(default=None, help="")
    failure: bool = Field(default=None, help="")
    succeeded: bool = Field(default=None, help="")
    success: bool = Field(default=None, help="")
    stdout: str = Field(default=None, help="")
    stderr: str = Field(default=None, help="")
    return_code: int = Field(default=-1, help="")
    pid: int = Field(default=-1, help="")

    def __rich_console__(self, console, options):  # noqa
        """
        https://rich.readthedocs.io/en/stable/protocol.html
        """

        def status_string():
            if self.succeeded is None:
                return "??"
            else:
                return "[cyan]=> [green]ok" if self.succeeded else "[red]failed"

        fmt = shfmt(self.command)
        syntax = Syntax(
            f"{fmt}",
            # f"[dim]$[/dim] [b]{fmt}[/b]",
            "bash",
            word_wrap=True,
            line_numbers=False,
        )
        yield Panel(
            syntax,
            title=(
                f"{self.__class__.__name__} from " f"pid {self.pid} {status_string()}"
            ),
            title_align="left",
            subtitle=Text("✔", style="green")
            if self.success
            else Text("❌", style="red"),
        )

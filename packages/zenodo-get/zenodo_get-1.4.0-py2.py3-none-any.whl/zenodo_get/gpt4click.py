#!/usr/bin/env python3
from decopatch import function_decorator, DECORATED
from makefun import wraps
from pathlib import Path
import openai
import os
import sys
import pickle
from typing import Union

exclusion_list = (
    "pytest",
    "git",
    "python3",
    "fix",
    "fix3",
    "fix4",
    "geany",
    "sphinx",
    "sphinx-build",
    "firefox",
)


def fix_call(
    model: str,
    tool_name: str,
    help_msg: str,
    cli_used: str,
    error_message: str,
) -> str:
    """
    Fix a command line tools invocation by analyzing the
    tools user's manual, the invoked command line, and the resulting error message.
    The tool uses either the gpt-3.5-turbo or the gpt-4 model.

    :param model: Name of the GPT model to use.
    :type model: str
    :param tool_name: Name of the command line tool.
    :type tool_name: str
    :param help_msg: Help message of the command line tool.
    :type help_msg: str
    :param cli_used: The invoked command line.
    :type cli_used: str
    :param error_message: The resulting error message.
    :type error_message: str
    :return: Fixed command to be executed.
    :rtype: str
    """
    openai.organization = os.getenv("OPENAI_ORG_ID") or openai.organization
    openai.api_key = os.getenv("OPENAI_API_KEY") or openai.api_key

    lines = help_msg.split("\n")
    if len(lines) > 20:
        help_msg = (
            "\n".join(lines[:10])
            + "\n\n<<redacted help message>>\n\n"
            + "\n".join(lines[-10:])
        )

    content = [
        {
            "role": "system",
            "content": f"""
            You are a IT expert and you help with command line tools.
            You read CLI tool documentation and you help the users to solve their problem.
            Your answer is always very brief, concise and succint.
            You do not explain basic shell commands and how they work,
            you only try to analyze the problem, e.g. wrong argument or wrong file name.
            If error message is provided, you try to take into account this message
            to figure out the reason of the problem. If not provided, then you
            analyze the command line options and the tool desciption to find the problem.
            If fixing the parameters is possible, then you first provide very brief explanation,
            then you end your response with the fixed code, no explanation after the code.
            If fix alone is not possible, then you recommend fixed command line AND
            you highlight what to check but this recommendation is brief, concise and succint.

            Important notation: all references to incorrect values should be
            marked in the format of [bold red]`INCORRECT`[/].
            All reference to proposed, fixed values should be marked with the format:
            [bold green]`PROPOSED`[/]
            After the end of each sentence, insert a new line character.
            Longer code blocks inside "```" should not be marked.

            Here is the description of the tool you work with:

            Tool name: {tool_name}
            {help_msg}
            """,
        },
        {
            "role": "assistant",
            "content": "I understand. An example: ```ln -symboliclink file1 file2.``` "
            "Using [bold red]`-symboliclink`[/bold red] is incorrect, instead you can use [bold green]`-s`[/bold green].\n"
            "Try this:\n[green]```ln -s file1 file2```[/green]",
        },
        {
            "role": "user",
            "content": f"""
            This is the failed command line:
            ```bash
            {tool_name} {cli_used}
            ```
            """,
        },
    ]

    if error_message:
        if len(error_message) > 500:
            lines = error_message.split("\n")
            error_message = (
                "\n".join(lines[:10])
                + "<redacted error message>\n "
                + "\n".join(lines[-10:])
            )
        content.append(
            {
                "role": "user",
                "content": f"""
                The following error message was shown:
                ```text
                {error_message}
                ```
                """,
            }
        )

    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=content,
            max_tokens=512,
            top_p=0.8,
            temperature=0.7,
            user="test_user_gpt4cli",
        )
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Unfortunately, an exception happend in my processing, can't help at the moment.\n{e}"


@function_decorator
def gpt4click(
    name: str = "", model: str = "gpt-3.5-turbo-16k", f=DECORATED
) -> callable:
    """
    Decorator over a `click` command line interface.
    If the click command ends with an error, it tries to analyze the reason
    with a GPT-3.5 or GPT-4.0 model.

    :param name: name of the command line tool. By default it will look up sys.args[0]
    :type name: str
    :param model: name of the GPT model
    :type model: str
    :param f: Decorated function
    :type f: callable
    :return: New function with improved error handling
    :rtype: callable
    """
    if not name:
        name = Path(sys.argv[0]).name

    @wraps(f)
    def new_f(*args, **kwargs) -> None:
        try:
            ctx = f.make_context(name, sys.argv[1:])
            with ctx:
                f.invoke(ctx)
        except Exception as error_msg:
            error_message = repr(error_msg)
            import click

            help_msg = click.Context(f).get_help()
            cli_args = " ".join(sys.argv[1:])

            fixed_cli = fix_call(model, name, help_msg, cli_args, error_message)
            print(f"Here's the corrected command ({model=}):")
            print(fixed_cli)

    return new_f


def parse_code_snippet(txt: str) -> tuple[str, str]:
    import parse

    parsed = parse.parse("{text}```bash\n{code}```", txt)
    if parsed is None:
        return txt, ""

    text = parsed["text"].strip()
    code = parsed["code"].strip()
    text = text.replace(". ", ".\n")
    return text, code


def send_text_to_terminal(text: str) -> None:
    import subprocess

    console = Console()
    console.print(
        "You can try the [dark_sea_green4]fixed version[/] by just pressing [red]ENTER[/red]:"
    )
    subprocess.run(
        ["xdotool", "type", "--clearmodifiers", text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    from subprocess import run

    p = run(sys.argv[1:])
    if p.returncode:
        model = "gpt-3.5-turbo-16k"
        model = "gpt-3.5-turbo-0613"
        tool_name = Path(sys.argv[1]).name

        cli_args = " ".join(sys.argv[2:])

        from rich.console import Console
        from rich.text import Text

        console = Console()

        if tool_name in exclusion_list:
            console.print(
                Text.from_markup(
                    f"Unfortunately, I cannot help with this tool ([orange1]{tool_name}[/])"
                )
            )
        else:
            console.print(
                Text.from_markup(
                    f"\n\nAn error has been detected, it is under analysis with [bright_magenta]{model}[/].\n"
                )
            )
            console.print(Text.from_markup("Your original command line was:\n"))
            console.print(Text.from_markup(f"[orange1]{tool_name} {cli_args}[/]\n"))

            p1 = run([sys.argv[1], "--help"], capture_output=True)

            help_message = (p1.stdout.decode() + p1.stderr.decode()).strip()

            p2 = run(sys.argv[1:], capture_output=True)
            error_msg = p2.stderr.decode().strip()

            cache_file = Path("~/.gpt4cache.pickle")
            cache = {}
            if cache_file.exists():
                content = cache_file.read_bytes()
                if len(content) > 0:
                    cache = pickle.loads(content)

            args = (model, tool_name, help_message, cli_args, error_msg)
            if args in cache:
                result = cache[args]
            else:
                result = fix_call(model, tool_name, help_message, cli_args, error_msg)
                cache[args] = result

            cache_file.write_bytes(
                pickle.dumps(cache, protocol=pickle.HIGHEST_PROTOCOL)
            )

            text, code = parse_code_snippet(result)

            console.print(Text.from_markup(text, justify="left"))
            console.print(
                Text.from_markup(f"[bold dark_sea_green4]{code}[/]", justify="left")
            )
            if code:
                if len(code.strip().split("\n")) == 1:
                    if os.getenv("GPT4SHELL", "default").lower() == "autofill":
                        send_text_to_terminal(f"{code}")

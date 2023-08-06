# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Cookiecutter post-generation hooks.

This module contains post-generation hooks to adjust the generated project to the
different types of projects and do some final checks and configuration.
"""

import configparser as _configparser
import dataclasses as _dataclasses
import json as _json
import os
import pathlib as _pathlib
import shutil as _shutil
import subprocess as _subprocess
from collections import namedtuple
from typing import Any


def to_named_tuple(dictionary: dict[Any, Any], /) -> Any:
    """Convert a dictionary to a named tuple.

    Args:
        dictionary: The dictionary to convert.

    Returns:
        The named tuple with the same keys and values as the dictionary.
    """
    filtered = {k: v for k, v in dictionary.items() if not k.startswith("_")}
    return namedtuple("Cookiecutter", filtered.keys())(*filtered.values())


cookiecutter = to_named_tuple(_json.loads(r"""{{cookiecutter | tojson}}"""))


def main() -> None:
    """Run some post-generation steps.

    This function is called after the project has been generated and it performs
    some fixes for different types of projects and some sanity checks.
    """
    finish_setup()

    print()
    print("-" * 80)
    print()
    success(f"Your 🍪 {cookiecutter.github_repo_name} has been cut!")
    print()
    print_generated_tree()
    print("Here is a list of things that should be reviewed and FIXED:")
    print_todos()
    print()
    print(
        "After completing it you can amend the previous commit using `git commit "
        "--amend` or create a new commit for the changes using `git commit`."
    )
    print()
    print(
        "You can make sure linting and tests pass by creating a virtual "
        "environment, installing the development dependencies and running `nox`:"
    )
    print()
    print(f"cd {cookiecutter.github_repo_name}")
    print("# Requires at least python version 3.11")
    print("python3 -m venv .venv")
    print(". .venv/bin/activate")
    print("pip install .[dev-noxfile]")
    print("nox")
    print()
    print("To generate and serve the documentation:")
    print("pip install .[dev-mkdocs]")
    if cookiecutter.type == "api":
        print("# Requires docker")
    print("mkdocs serve")
    print()
    print("To initialize the GitHub pages website:")
    print("mike deploy --update-aliases next latest")
    print("mike set-default latest")
    print("git push upstream gh-pages  # or origin if you haven't forked the repo")
    print()
    print("Make sure that GitHub pages is enabled in your repository settings:")
    print(
        f"https://github.com/{cookiecutter.github_org}/{cookiecutter.github_repo_name}"
        "/settings/pages"
    )
    print("If all went well, your new website should be available soon at:")
    print(
        f"https://{cookiecutter.github_org}.github.io/{cookiecutter.github_repo_name}/"
    )
    print()
    if warnings := do_sanity_checks():
        for warning in warnings:
            warn(warning)
        print()
    note(
        "If you had any issues or find any errors in the generated files, "
        "please report them!"
    )
    note(
        "https://github.com/frequenz-floss/frequenz-repo-config-python/issues/new/choose"
    )
    print()


def finish_setup() -> None:
    """Finish the setup.

    This function is called after the project has been generated and can be used
    to perform any additional setup steps that are required for the project.
    """
    was_repo_initialized = initialize_git_repo()

    copy_replay_file()

    remove_unneeded_files()

    match cookiecutter.type:
        case "actor":
            finish_actor_setup()
        case "api":
            finish_api_setup()
        case "app":
            finish_app_setup()
        case "lib":
            finish_lib_setup()
        case "model":
            finish_model_setup()

    initialize_git_submodules()
    commit_git_changes(first_commit=was_repo_initialized)


def copy_replay_file() -> None:
    """Copy the replay file to the project root."""
    src = _pathlib.Path("~/.cookiecutter_replay/cookiecutter.json").expanduser()
    dst = _pathlib.Path(".cookiecutter-replay.json")

    if dst.exists():
        print(f"Replay file {dst} already exists. Skipping...")
        return

    if not src.exists():
        print(f"WARNING: No replay file found in {src}. Skipping...")
        return

    try:
        with src.open("r", encoding="utf8") as input_file:
            replay_data = _json.load(input_file)

        # Remove the _output_dir key from the replay data because it is an absolute path
        # that depends on the current environment and we don't want to add it as part of
        # the generated project.
        replay_data["cookiecutter"].pop("_output_dir", None)

        if template := replay_data["cookiecutter"].get("_template"):
            if not template.startswith(("gh:", "git@", "https://")):
                print(
                    f"WARNING: The replay file's `_template` ({template}) doesn't seem "
                    "to be a remote repository, it won't be saved to avoid storing a "
                    "local template in the new repository. If this is incorrect, "
                    f"please add it back manually to {dst}."
                )
                replay_data["cookiecutter"].pop("_template", None)

        with dst.open("w", encoding="utf8") as output_file:
            _json.dump(replay_data, output_file, indent=2)
    except KeyError as error:
        print(
            f"WARNING: Error parsing the replay file {src} -> {dst} ({error}). "
            "Skipping..."
        )
    # We want to catch a broad range of exceptions here because we don't want to fail
    # the whole generation process just because the replay file is broken.
    except Exception as error:  # pylint: disable=broad-except
        print(
            f"WARNING: Error copying the replay file {src} -> {dst} ({error}). "
            "Skipping..."
        )


def initialize_git_submodules() -> bool:
    """Initialize git submodules.

    If a `.gitmodules` file exists and it is not empty, it will be used to initialize
    the git submodules using `git submodule update --init --recursive`.

    If an empty `.gitmodules` file exists, it will be deleted.

    Returns:
        Whether any git submodules were initialized.
    """
    if is_golden_testing():
        # We don't use external tools when running tests because they are too flaky, as
        # different versions emit different outputs
        return False

    gitmodules_path = _pathlib.Path(".gitmodules")

    if not gitmodules_path.exists():
        return False

    if not gitmodules_path.is_file():
        warn("`.gitmodules` exists but is not a file! Ignoring...")
        return False

    if is_file_empty(gitmodules_path):
        gitmodules_path.unlink()
        return False

    gitmodules_config = _configparser.ConfigParser()
    with gitmodules_path.open("r", encoding="utf8") as file_handle:
        gitmodules_config.read_file(file_handle)

    @_dataclasses.dataclass(frozen=True)
    class Submodule:
        """A git submodule."""

        name: str
        path: str
        url: str

        def mkdir(self) -> None:
            """Create the directory for the submodule."""
            _pathlib.Path(self.path).parent.mkdir(exist_ok=True, parents=True)

    submodules: list[Submodule] = []
    for section in gitmodules_config.sections():
        heading = 'submodule "'
        trailing = '"'
        if not section.startswith(heading) or not section.endswith(trailing):
            warn(f"Can't parse `.gitmodules` section `{section}`! Ignoring...")
            continue
        if "path" not in gitmodules_config[section]:
            warn(
                f"`.gitmodules` contains section `{section}` without `path`! Ignoring..."
            )
            continue
        if "url" not in gitmodules_config[section]:
            warn(
                f"`.gitmodules` contains section `{section}` without `url`! Ignoring..."
            )
            continue
        submodule = Submodule(
            name=section[len(heading) : -len(trailing)],
            path=gitmodules_config[section]["path"],
            url=gitmodules_config[section]["url"],
        )
        # submodule.mkdir()
        submodules.append(submodule)

    if not submodules:
        warn("`.gitmodules` does not contain any valid submodules! Ignoring...")
        return False

    print()
    note("Initializing git submodules...")

    for submodule in submodules:
        try_run(
            [
                "git",
                "submodule",
                "add",
                "--name",
                submodule.name,
                submodule.url,
                submodule.path,
            ],
            verbose=True,
            warn_on_error=True,
            warn_on_bad_status=f"Failed to add submodule `{submodule.name}`!",
            note_on_failure=f"Please add submodule `{submodule.name}` manually.",
        )
    try_run(
        ["git", "submodule", "update", "--init"],
        verbose=True,
        warn_on_error=True,
        warn_on_bad_status="Failed to initialize git submodules!",
        note_on_failure="Please initialize git submodules manually.",
    )
    return True


def initialize_git_repo() -> bool:
    """Initialize a git repository.

    If the project is not a git repository, it will be initialized using
    `git init`.

    If the project is already a git repository, it will be left untouched.

    Returns:
        Whether the project was initialized as a git repository.
    """
    if is_golden_testing():
        # We don't use external tools when running tests because they are too flaky, as
        # different versions emit different outputs
        return False

    if _pathlib.Path(".git").exists():
        return False

    print()
    note("Initializing git repository...")
    try_run(
        ["git", "init"],
        verbose=True,
        warn_on_error=True,
        warn_on_bad_status="Failed to initialize the git repository!",
        note_on_failure="Please initialize the git repository manually.",
    )
    return True


def commit_git_changes(*, first_commit: bool) -> None:
    """Commit all changes in the git repository.

    If there are no changes to commit, this function does nothing.

    Args:
        first_commit: Whether this is the first commit in the git repository.
    """
    if is_golden_testing():
        # We don't use external tools when running tests because they are too flaky, as
        # different versions emit different outputs
        return

    if not try_run(["git", "status", "--porcelain"]):
        return

    print()
    try_run(
        ["git", "add", "."],
        verbose=True,
        warn_on_error=True,
        warn_on_bad_status="Failed to add all changes to the git repository!",
        note_on_failure="Please add all changes to the git repository manually.",
    )
    message = (
        "Initial commit" if first_commit else "Regenerate repository using repo-config"
    )
    try_run(
        ["git", "commit", "-s", "-m", message],
        verbose=True,
        warn_on_error=True,
        warn_on_bad_status="Failed to commit all changes to the git repository!",
        note_on_failure="Please commit all changes to the git repository manually.",
    )


def remove_unneeded_files() -> None:
    """Remove unneeded files.

    Files that are not needed for the project are removed.
    """
    if cookiecutter.license != "MIT":
        _pathlib.Path("LICENSE").unlink()

    if cookiecutter.type != "api":
        _shutil.rmtree("proto")


def is_file_empty(path: _pathlib.Path) -> bool:
    """Check if the file is empty.

    A file is also considered empty if it only contains white spaces.

    Note:
        Only the first 1024 bytes of the file are read for performance and security
        reasons, a files with the first 1024 bytes being white spaces is considered
        empty.

    Args:
        path: The path to the file to check.

    Returns:
        True if the file has only white spaces, False otherwise.
    """
    with path.open("r", encoding="utf8") as file_handle:
        contents = file_handle.read(1024).strip()
        return not contents


def print_generated_tree() -> None:
    """Print the generated files tree."""
    if is_golden_testing():
        # We don't use external tools when running tests because they are too flaky, as
        # different versions emit different outputs
        return

    result = try_run(["tree"])
    if result is not None and result.returncode == 0:
        print()


def print_todos() -> None:
    """Print all TODOs in the generated project."""
    todo_str = "TODO(cookiecutter):"
    repo = cookiecutter.github_repo_name
    cmd = rf"grep -r --color '\<{todo_str}.*' . | sort"
    try_run(
        cmd,
        warn_on_error=True,
        warn_on_bad_status=f"No `{todo_str}` found using `{cmd}`",
        note_on_failure=f"Please search for `{todo_str}` in `{repo}/` manually.",
        shell=True,
    )
    print()
    note(
        "Make sure to (create and) configure your GitHub repository too: "
        "https://github.com/frequenz-floss/frequenz-repo-config-python/"
        "wiki/Configuring-a-new-GitHub-repository"
    )


def do_sanity_checks() -> list[str]:
    """Perform sanity checks on the generated project.

    Returns:
        List of warnings.
    """
    warnings: list[str] = []

    if cookiecutter.github_org == "frequenz-floss" and cookiecutter.license != "MIT":
        warnings.append(
            "Using a non-MIT license with a frequenz-floss project is not recommended."
        )

    return warnings


def finish_actor_setup() -> None:
    """Finish the setup for an actor.

    This function is called after the project has been generated and can be used
    to perform any additional setup steps that are required for an actor.
    """


def finish_api_setup() -> None:
    """Finish the setup for an API.

    This function is called after the project has been generated and can be used
    to perform any additional setup steps that are required for an API.

    Operations performed by this function:

    * Rename `src` to `py`
    * Rename `tests` to `pytests`
    """
    recursive_overwrite_move(_pathlib.Path("src"), _pathlib.Path("py"))
    recursive_overwrite_move(_pathlib.Path("tests"), _pathlib.Path("pytests"))


def finish_app_setup() -> None:
    """Finish the setup for an app.

    This function is called after the project has been generated and can be used
    to perform any additional setup steps that are required for an app.
    """


def finish_lib_setup() -> None:
    """Finish the setup for a library.

    This function is called after the project has been generated and can be used
    to perform any additional setup steps that are required for a library.

    Operations performed by this function:

    * Avoid having a subfolder for the type

      - `lib`: `src/frequenz/{name}`
      - `rest`: `src/frequenz/{type}/{name}`
    """
    name = cookiecutter.name.lower().replace("-", "_")
    recursive_overwrite_move(
        _pathlib.Path(f"src/frequenz/{cookiecutter.type}/{name}"),
        _pathlib.Path(f"src/frequenz/{name}"),
    )
    _pathlib.Path(f"src/frequenz/{cookiecutter.type}").rmdir()


def finish_model_setup() -> None:
    """Finish the setup for a model.

    This function is called after the project has been generated and can be used
    to perform any additional setup steps that are required for a model.
    """


def try_run(
    cmd: list[str] | str,
    /,
    *,
    warn_on_error: bool = False,
    warn_on_bad_status: str | None = None,
    note_on_failure: str | None = None,
    verbose: bool = False,
    shell: bool = False,
) -> _subprocess.CompletedProcess[Any] | None:
    """Try to run a command.

    Args:
        cmd: The command to run.
        warn_on_error: Whether to warn on errors (like command not found) of fail
            silently.
        warn_on_bad_status: If not `None`, warn if the command fails with a non-zero
            status code and use this string as the warning message (the status code
            will be appended to the message).
        note_on_failure: If not `None`, print this note if the command fails (either
            because of an error or a non-zero status code).
        verbose: Whether to print the command before running it.
        shell: Whether to run the command in a shell. If `True`, `cmd` must be a
            string, otherwise it must be a list of strings.

    Returns:
        The result of the command or `None` if the command could not be run because
        of an error.
    """
    assert isinstance(cmd, str) and shell or isinstance(cmd, list) and not shell
    result = None
    failed = False
    if verbose:
        print(f"Executing: {' '.join(cmd)}")
    try:
        result = _subprocess.run(cmd, check=False, shell=shell)
    except (OSError, _subprocess.CalledProcessError) as exc:
        if warn_on_error:
            warn(f"Failed to run the search command `{' '.join(cmd)}`: {exc}")
        failed = True
    else:
        if result.returncode != 0:
            if warn_on_bad_status is not None:
                warn(f"{warn_on_bad_status} (status code: {result.returncode})")
            failed = True
    if failed and note_on_failure is not None:
        note(note_on_failure)

    return result


def is_golden_testing() -> bool:
    """Return `True` if we are running as part of a golden testing.

    Returns:
        Whether we are running as part of a golden testing.
    """
    return os.environ.get("GOLDEN_TEST", None) is not None


def recursive_overwrite_move(src: _pathlib.Path, dst: _pathlib.Path) -> None:
    """Recursively move a directory overwriting the target files if they exist.

    Useful when overwriting an existing project to update it.

    Args:
        src: The source directory.
        dst: The target directory.
    """
    _shutil.copytree(src, dst, dirs_exist_ok=True)
    _shutil.rmtree(src)


def success(message: str) -> None:
    """Print a success message.

    Args:
        message: The message to print.
    """
    print(f"\033[32m{message}\033[0m")


def note(message: str) -> None:
    """Print a note.

    Args:
        message: The message to print.
    """
    print(f"\033[36m{message}\033[0m")


def warn(message: str) -> None:
    """Print a warning.

    Args:
        message: The message to print.
    """
    print(f"\033[33mWARNING: {message}\033[0m")


main()

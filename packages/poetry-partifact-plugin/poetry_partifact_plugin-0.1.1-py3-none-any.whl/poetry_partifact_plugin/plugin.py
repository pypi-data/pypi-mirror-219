"""
Module contains a poetry plugin for handling AWS CodeArtifact authentication when using Poetry.

This module contains a PartifactPlugin class that checks if the pyproject.toml file contains
a CodeArtifact repository. If it does, the plugin sets up the necessary environment variables
for authentication before running any Install or Add Commands.
"""
import os

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from cleo.io.io import IO
from partifact.auth_token import get_token
from partifact.config import Configuration
from poetry.console.application import Application
from poetry.console.commands.add import AddCommand
from poetry.console.commands.install import InstallCommand
from poetry.console.commands.self.self_command import SelfCommand
from poetry.plugins.application_plugin import ApplicationPlugin
from tomlkit import parse as parse_toml
from tomlkit.exceptions import TOMLKitError

CONFIG_PATH = "./pyproject.toml"


class PartifactPlugin(ApplicationPlugin):
    """
    PartifactPlugin is a Poetry plugin that handles AWS CodeArtifact authentication
    before running any Install or Add Commands.
    """

    name = "PartifactPlugin"

    def activate(self, application: Application) -> None:
        """
        Activates the plugin by adding a listener to the COMMAND event.
        """
        application.event_dispatcher.add_listener(COMMAND, self._handle_pre_command)

    def _handle_pre_command(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        """
        Handles the pre-command event, authenticating to AWS CodeArtifact if necessary.

        Args:
            event: The console command event.
            event_name: The name of the event being dispatched.
            dispatcher: The event dispatcher.
        """
        command = event.command
        cleo_io = event.io

        if isinstance(command, SelfCommand):
            # don't run the plugin for self commands
            return

        if not any(isinstance(command, t) for t in [InstallCommand, AddCommand]):
            # Only run the plugin for install and add commands
            return

        try:
            parsed_toml = self._read_pyproject_file(file_path=CONFIG_PATH)
        except Exception as error:
            cleo_io.write_error_line(
                f"<error>{self.name} failed to read {CONFIG_PATH} pyproject file: \n{error}</>"
            )
            return

        if not self._pyproject_toml_has_codeartifact(parsed_toml=parsed_toml):
            # only run aws login if codeartifact is found in pyproject.toml
            return

        self._setup_aws_auth(cleo_io=cleo_io, parsed_toml=parsed_toml)

    def _get_sources(self, parsed_toml: dict) -> list:
        """
        Returns a list of all tool.poetry.source's in the parsed toml.

        Args:
            parsed_toml: The parsed TOML dictionary.

        Returns:
            A list of all tool.poetry.source's in the parsed toml.
        """
        return parsed_toml.get("tool", {}).get("poetry", {}).get("source", [])

    def _read_pyproject_file(self, file_path: str) -> dict:
        """
        Reads the pyproject.toml file contents and returns the parsed contents.

        Args:
            file_path: The path to the pyproject.toml file.

        Returns:
            A dictionary representing the parsed contents of the pyproject.toml file.

        Raises:
            RuntimeError: If the pyproject.toml file is not found or is invalid.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return parse_toml(file.read())
        except FileNotFoundError as error:
            raise RuntimeError(f"No pyproject.toml found at {file_path}") from error
        except TOMLKitError as error:
            raise RuntimeError("Invalid pyproject.toml") from error

    def _pyproject_toml_has_codeartifact(self, parsed_toml: dict) -> bool:
        """
        Determines if the pyproject.toml file has a CodeArtifact repository in it.

        Args:
            parsed_toml: The parsed TOML dictionary.

        Returns:
            True if a CodeArtifact repository is found, False otherwise.
        """
        sources = self._get_sources(parsed_toml=parsed_toml)

        for source in sources:
            if ".codeartifact." in source.get("url", ""):
                return True

        return False

    def _get_profile_name(self, parsed_toml: dict) -> str:
        """
        Retrieves the AWS profile name from the pyproject.toml file.

        Args:
            parsed_toml: The parsed TOML dictionary.

        Returns:
            A string representing the AWS profile name.

        Raises:
            RuntimeError: If a valid tool.poetry.source.name field is not found.
        """
        # if we are getting this far, we can assume at least one codeartifact source exists
        sources = self._get_sources(parsed_toml=parsed_toml)
        for source in sources:
            if ".codeartifact." in source.get("url", "") and source.get("name"):
                return source["name"]

        # if we get to here, that means the user didn't specify the name field
        raise RuntimeError("Could not find a valid tool.poetry.source.name field")

    def _setup_aws_auth(self, cleo_io: IO, parsed_toml: dict) -> None:
        """
        Sets up AWS CodeArtifact authentication by configuring the necessary environment variables.

        Args:
            cleo_io: The console I/O object.
            parsed_toml: The parsed TOML dictionary.
        """
        try:
            self._set_env_vars(parsed_toml=parsed_toml)
            cleo_io.write_line(
                f"<fg=green>{self.name} successfully configured AWS CodeArtifact</info>"
            )
        except Exception as error:
            cleo_io.write_error_line(
                f"<error>{self.name} failed to configure AWS CodeArtifact: \n\t{error}</>"
            )

    def _set_env_vars(self, parsed_toml: str) -> None:
        """
        Sets environment variables required for AWS CodeArtifact authentication.

        Args:
            parsed_toml: The parsed TOML dictionary.
            
        Raises:
            Exception: If there's an error getting the profile name.
        """
        profile_name = self._get_profile_name(parsed_toml)
        formatted_profile_name = profile_name.upper().replace("-", "_")
        config = Configuration.load(profile_name, profile=profile_name)

        # setting these env variables will allow poetry to connect to codeartifact
        # https://python-poetry.org/docs/configuration/#using-environment-variables
        os.environ[f"POETRY_HTTP_BASIC_{formatted_profile_name}_PASSWORD"] = get_token(
            config
        )
        os.environ[f"POETRY_HTTP_BASIC_{formatted_profile_name}_USERNAME"] = "aws"

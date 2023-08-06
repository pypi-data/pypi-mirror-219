from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    TextIO,
    TypeVar,
    Union,
    overload,
)

from rich import get_console
from rich.console import Console
from rich.prompt import DefaultType, InvalidResponse, PromptBase, PromptType
from rich.text import Text, TextType


class ListPrompt(PromptBase):
    choice_key: str | Callable | None
    response_type = Any
    choices: List[Any] = []

    def __init__(
        self,
        prompt: TextType = "",
        choices: List[Any] = [],
        *,
        console: Optional[Console] = None,
        password: bool = False,
        show_default: bool = True,
        show_choices: bool = True,
        choice_key: str | Callable | None = None,
    ) -> None:
        self.choice_key = choice_key
        self.console = console or get_console()
        self.prompt = (
            Text.from_markup(prompt, style="prompt")
            if isinstance(prompt, str)
            else prompt
        )
        self.password = password
        if choices is not None:
            self.choices = choices
        self.show_default = show_default
        self.show_choices = show_choices

    @classmethod
    def ask(
        cls,
        prompt: TextType = "",
        choices: List[Any] = [],
        *,
        console: Optional[Console] = None,
        password: bool = False,
        show_default: bool = True,
        show_choices: bool = True,
        default: Any = ...,
        stream: Optional[TextIO] = None,
        choice_key: Optional[Callable[[Any], str]] | Optional[str] | None = None,
    ) -> Union[DefaultType, PromptType]:
        _prompt = cls(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
            choice_key=choice_key,
        )
        return _prompt(default=default, stream=stream)

    def _handle_choice(self, choice: Any) -> str:
        if callable(self.choice_key):
            res = self.choice_key(choice)
            if type(res) != str:
                raise ValueError(
                    f"<{type(res)} incorrect type. ListPrompt.choice_key function must return string."
                )
            else:
                return res
        elif type(self.choice_key) is str and hasattr(choice, "__getitem__"):
            return choice[self.choice_key]
        else:
            return choice

    @property
    def index_choices(self) -> Dict[int, Any]:
        if not hasattr(self, "_ind_choices") or len(self._ind_choices) != len(
            self.choices
        ):
            self._ind_choices = {}
            for i, choice in enumerate(self.choices):
                if self.default != ... and (
                    self.default == choice
                    or self.default == self._handle_choice(choice)
                ):
                    self.default = i
                self._ind_choices[i] = choice
            if (
                self.default != ...
                and self.default not in self.choices
                and (
                    type(self.default) is not int
                    or (self.default > len(self.choices) or self.default < 0)
                )
            ):
                self.default = ...
        return list(self._ind_choices.items())

    def make_choices(self) -> List[str]:
        return [
            f"{self._handle_choice(choice)} [{i}]" for i, choice in self.index_choices
        ]

    def make_prompt(self, default: DefaultType) -> Text:
        """Make prompt text.

        Args:
            default (DefaultType): Default value.

        Returns:
            Text: Text to display in prompt.
        """
        prompt = self.prompt.copy()
        prompt.end = ""

        if self.show_choices and self.choices:
            _choices = "/".join(self.make_choices())
            choices = f"[{_choices}]"
            prompt.append(" ")
            prompt.append(choices, "prompt.choices")

        if default != ... and self.show_default and isinstance(default, int):
            prompt.append(" ")
            _default = self.render_default(default)
            prompt.append(_default)

        prompt.append(self.prompt_suffix)

        return prompt

    def check_choice(self, value: int) -> bool:
        assert self.choices is not None
        return value in self._ind_choices.keys()

    def process_response(self, value: str) -> list:
        try:
            value = int(value)
        except:
            value = None

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        return self._ind_choices[value]

    @overload
    def __call__(self, *, stream: Optional[TextIO] = None) -> PromptType:
        ...

    @overload
    def __call__(
        self, *, default: DefaultType, stream: Optional[TextIO] = None
    ) -> Union[PromptType, DefaultType]:
        ...

    def __call__(self, *, default: Any = ..., stream: Optional[TextIO] = None) -> Any:
        """Run the prompt loop.

        Args:
            default (Any, optional): Optional default value.

        Returns:
            PromptType: Processed value.
        """
        self.default = default
        self.index_choices
        default = self.default
        while True:
            self.pre_prompt()
            prompt = self.make_prompt(self.default)
            value = self.get_input(self.console, prompt, self.password, stream=stream)
            if value == "" and self.default != ... and type(self.default) == int:
                return self._ind_choices[self.default]
            try:
                return_value = self.process_response(value)
            except InvalidResponse as error:
                self.on_validate_error(value, error)
                continue
            else:
                return return_value


class DictPrompt(PromptBase[int]):
    response_type = Any
    choices: Dict[Any, Any] = []

    def __init__(
        self,
        prompt: TextType = "",
        choices: Dict[Any, Any] = {},
        *,
        console: Optional[Console] = None,
        password: bool = False,
        show_default: bool = True,
        show_choices: bool = True,
    ) -> None:
        self.console = console or get_console()
        self.prompt = (
            Text.from_markup(prompt, style="prompt")
            if isinstance(prompt, str)
            else prompt
        )
        self.password = password
        if choices is not None:
            self.choices = choices
        self.show_default = show_default
        self.show_choices = show_choices

    @classmethod
    def ask(
        cls,
        prompt: TextType = "",
        choices: Dict[Any, Any] = [],
        *,
        console: Optional[Console] = None,
        password: bool = False,
        show_default: bool = True,
        show_choices: bool = True,
        default: Any = ...,
        stream: Optional[TextIO] = None,
    ) -> Union[DefaultType, PromptType]:
        _prompt = cls(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )
        return _prompt(default=default, stream=stream)

    def _handle_choice(self, choice: Any) -> str:
        if type(self.choices[choice]) == str and type(choice) != str:
            return self.choices[choice]
        return str(choice)

    @property
    def index_choices(self) -> Dict[int, Any]:
        if not hasattr(self, "_ind_choices") or len(self._ind_choices) != len(
            self.choices.keys()
        ):
            self._ind_choices = {}
            for i, key in enumerate(self.choices.keys()):
                if self.default != ... and self.default == key:
                    self.default = i
                self._ind_choices[i] = key
            if (
                self.default != ...
                and self.default not in self.choices.values()
                and self.default not in self.choices.keys()
                and (
                    type(self.default) is not int
                    or (self.default > len(self.choices.keys()) or self.default < 0)
                )
            ):
                self.default = ...
        return list(self._ind_choices.items())

    def get_choice(self, ind):
        return self.choices[self._ind_choices[ind]]

    def make_choices(self) -> List[str]:
        return [
            f"{self._handle_choice(choice)} [{i}]" for i, choice in self.index_choices
        ]

    def make_prompt(self, default: DefaultType) -> Text:
        """Make prompt text.

        Args:
            default (DefaultType): Default value.

        Returns:
            Text: Text to display in prompt.
        """
        prompt = self.prompt.copy()
        prompt.end = ""

        if self.show_choices and self.choices:
            _choices = "/".join(self.make_choices())
            choices = f"[{_choices}]"
            prompt.append(" ")
            prompt.append(choices, "prompt.choices")

        if default != ... and self.show_default and isinstance(default, int):
            prompt.append(" ")
            _default = self.render_default(default)
            prompt.append(_default)

        prompt.append(self.prompt_suffix)

        return prompt

    def check_choice(self, value: int) -> bool:
        assert self.choices is not None
        return value in self._ind_choices.keys()

    def process_response(self, value: str) -> list:
        try:
            value = int(value)
        except:
            value = None

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        return self.get_choice(value)

    def __call__(self, *, default: Any = ..., stream: Optional[TextIO] = None) -> Any:
        """Run the prompt loop.

        Args:
            default (Any, optional): Optional default value.

        Returns:
            PromptType: Processed value.
        """
        self.default = default
        self.index_choices
        while True:
            self.pre_prompt()
            prompt = self.make_prompt(self.default)
            value = self.get_input(self.console, prompt, self.password, stream=stream)
            if value == "" and self.default != ... and type(self.default) == int:
                return self._ind_choices[self.default]
            try:
                return_value = self.process_response(value)
            except InvalidResponse as error:
                self.on_validate_error(value, error)
                continue
            else:
                return return_value

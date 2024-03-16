import re
from dataclasses import dataclass, field

from pysamp.dialog import Dialog
from pysamp.player import Player
from python.utils.enums.dialog_style import DialogStyle
from typing import Callable, Union, Any


@dataclass
class DialogTreeNode:
    node_name: str
    dialog_style: DialogStyle
    title: str
    content: str
    button_1: str
    button_2: str
    parent: Union["DialogTreeNode", None] = None
    active_page_number: int = 0
    max_list_length: int = 16
    jump_to: str | None = None
    exit_on_button_2: bool = False
    back_to_root: bool = False
    close_in_end: bool = False
    back_after_input: bool = False
    stay_if_none: bool = True
    save_input: bool = False
    use_same_children: bool = False
    just_action: bool = False
    children: list[Union["DialogTreeNode", None]] = field(default_factory=list)
    custom_handler: Callable[[Player, int, int, str, ...], bool | None] | None = None
    custom_handler_node_parameters: tuple[str, ...] = None
    custom_handler_parameters: tuple[Any] = None
    custom_content_handler: Callable[[Player, ...], str] | None = None
    custom_content_handler_node_parameters: tuple[str, ...] = None
    custom_content_handler_parameters: tuple[str, ...] = None
    dialog_tree: Union["DialogTree", None] = None

    __selected_page_number: int = 0
    __selected_list_item: int = 0

    dialogs: list[Dialog] = field(default_factory=list)

    def add_child(self, child: Union["DialogTreeNode", None]) -> None:
        self.children.append(child)
        if child is not None:
            child.parent = self

        if self.parent is not None:
            self.dialog_tree = self.parent.dialog_tree

    def show(self, player: Player):
        if self.dialog_tree is None:
            self.dialog_tree = self.parent.dialog_tree

        if self.parent is None:
            self.dialog_tree.node_variables = {}

        if self.just_action:
            self.handler(player, 1, 0, "")
            return

        content = self.content

        if self.custom_content_handler is not None:

            args: list[str] = self.__get_custom_content_handler_parameters()
            c_content = self.custom_content_handler(player, *args)

            if c_content == "":
                if self.parent is None or self.back_to_root:
                    self.dialog_tree.root.show(player)
                    return

                self.parent.show(player)
                return

            content += c_content

        self.dialogs = self.create_dialogs(content)

        self.dialogs[0].show(player)

    def create_dialogs(self, content: str) -> list[Dialog]:

        return [Dialog.create(self.dialog_style, f_title, f_content, self.button_1, self.button_2, self.handler)
                for f_title, f_content in self.prepare_content(self.dialog_style, self.title, content)]

    def prepare_content(self, dialog_style: DialogStyle, title: str, content: str) -> tuple[str, str]:

        pattern = r'#(.*?)#'
        header = ""

        pages: list[str] = split_content_by_limit(dialog_style, content, self.max_list_length)
        page_count = len(pages)

        if dialog_style == DialogStyle.TABLIST_HEADERS:
            header = pages[0][:pages[0].find('\n') + 2]

        for i in range(page_count):
            items = pages[i].split('\n')
            item_count = len(items)

            for j in range(item_count):
                matches = re.findall(pattern, items[j])

                for match in matches:
                    if "->" in match:
                        prop = match.split("->")[0]
                        value = match.split("->")[1]

                        property_key: str = prop + f"_{str(i)}_{str(j)}"
                        self.dialog_tree.node_variables[self.node_name] = {property_key: value}

                        items[j] = items[j].replace(f'#{match}#', value)

                    elif "~>" in match:
                        prop = match.split("~>")[0]
                        value = match.split("~>")[1]

                        property_key: str = prop + f"_{str(i)}_{str(j)}"

                        if self.node_name in self.dialog_tree.node_variables:
                            self.dialog_tree.node_variables[self.node_name][property_key] = value

                        else:
                            self.dialog_tree.node_variables[self.node_name] = {property_key: value}

                        items[j] = items[j].replace(f'#{match}#', "")

                    elif "." in match:
                        node_name = match.split(".")[0]
                        prop = match.split(".")[1]

                        node = self.dialog_tree.root.find_node_by_name(node_name)
                        prop_key: str = prop + f"_{str(node.__selected_page_number)}_{str(node.__selected_list_item)}"
                        value = self.dialog_tree.node_variables[node_name][prop_key]

                        items[j] = items[j].replace(f'#{match}#', value)

            page_title = title if page_count == 1 else title + f" ({str(i + 1)}" + " / " + f"{str(page_count)})"
            clean_content = '\n'.join(items)

            if dialog_style == DialogStyle.TABLIST_HEADERS and i != 0:
                clean_content = (header + clean_content)

            yield page_title, clean_content

    def find_node_by_name(self, node_name: str) -> Union["DialogTreeNode", None]:

        for node in self.children:
            if node.node_name.lower() == node_name.lower():
                return node

            else:
                r_node = node.find_node_by_name(node_name)

                if r_node is not None:
                    return r_node

        return None

    def handler(self, player: Player, response: int, list_item: int, input_text: str):

        if not bool(response):
            if self.exit_on_button_2 or self.parent is None:
                return

            if self.jump_to is not None:
                node = self.dialog_tree.root.find_node_by_name(self.jump_to)

                if node is not None:
                    node.show(player)
                    return

                else:
                    self.parent.show(player)
                    return

            if self.back_to_root:
                self.dialog_tree.root.show(player)
                return

            self.parent.show(player)
            return

        if self.save_input:
            self.dialog_tree.node_variables[self.node_name] = {'input_value': input_text}

        page_move = 1 if "<<<" in input_text else -1 if ">>>" in input_text else 0

        if page_move != 0:
            self.active_page_number += page_move
            self.dialogs[self.active_page_number].show(player, self.active_page_number, list_item)
            return

        self.__selected_page_number: int = self.active_page_number
        self.__selected_list_item: int = list_item

        if self.custom_handler is not None:
            args: list[str] = self.__get_custom_handler_parameters()

            custom_handler_result = self.custom_handler(player, response, list_item, input_text, *args)

            if not custom_handler_result and self.stay_if_none:
                self.show(player)
                return

        if self.just_action or self.back_after_input:
            self.parent.show(player)
            return

        if len(self.children) != 0 and list_item <= len(self.children) - 1:
            if list_item == -1:
                self.children[0].show(player)
                return

            if self.children[list_item] is None:
                if self.use_same_children:
                    self.children[0].show(player)
                    return

                if self.stay_if_none:
                    self.show(player)
                    return

            else:
                self.children[list_item].show(player)
                return

        else:
            if self.use_same_children:
                self.children[0].show(player)
                return

            if self.stay_if_none:
                self.show(player)
                return

            if self.back_to_root:
                self.dialog_tree.root.show(player)
                return

            if self.close_in_end:
                return

            self.parent.show(player)

    def __get_custom_content_handler_parameters(self):
        args: list[str] = []

        if self.custom_content_handler_parameters is not None:
            args.extend(self.custom_handler_parameters)

        if self.custom_content_handler_node_parameters is not None:
            args.extend(self.__get_parameters(self.custom_content_handler_node_parameters))

        return args

    def __get_custom_handler_parameters(self):
        args: list[str] = []

        if self.custom_handler_parameters is not None:
            args.extend(self.custom_handler_parameters)

        if self.custom_handler_node_parameters is not None:
            args.extend(self.__get_parameters(self.custom_handler_node_parameters))

        return args

    def __get_parameters(self, raw_parameters):

        args = []

        for raw_parameter in raw_parameters:
            node_name = raw_parameter.split(".")[0]
            prop = raw_parameter.split(".")[1]

            node = self.dialog_tree.root.find_node_by_name(node_name)

            prop_key: str = prop + f"_{str(node.__selected_page_number)}_{str(node.__selected_list_item)}"

            node_var = self.dialog_tree.node_variables.get(node_name)

            if node_var is not None:
                node_prop = node_var.get(prop_key)
                args.append(node_prop)

        return args


class DialogTree:
    def __init__(self, root: "DialogTreeNode"):
        self.root: "DialogTreeNode" = root
        self.node_variables: dict[str, dict[str, str]] = {}
        self.root.dialog_tree = self

    def show_root_dialog(self, player: Player) -> None:
        self.root.show(player)


# region helpers

def find_all_char(text: str, ch: str):
    for i, ltr in enumerate(text):
        if ltr == ch:
            yield i


def content_splitter(content: str, max_item) -> list[str]:
    index_list: list[int] = list(find_all_char(content, "\n"))[max_item - 1::max_item]
    start: int = 0
    acc: list[str] = []

    for i in index_list:
        chunk = content[start:i]
        start = i + 1
        acc.append(chunk)

    acc.append(content[start:])

    return acc


def split_content_by_limit(dialog_style, content: str, max_list_length: int) -> list[str]:
    if dialog_style not in [DialogStyle.MSGBOX, DialogStyle.LIST, DialogStyle.TABLIST, DialogStyle.TABLIST_HEADERS]:
        return [content]

    if len(content) >= max_list_length * 64:

        if dialog_style == DialogStyle.MSGBOX:
            return [content[:max_list_length * 64]]

        splitup = content_splitter(content, max_list_length)

        pages = len(splitup)

        for i in range(pages):

            if splitup[i][-1:] != '\n':
                splitup[i] += '\n'
            elif splitup[i][-1:] == '\n':
                splitup[i] += '\n'

            if i == 0:
                splitup[i] += f">>>"
            elif i < pages - 1:
                splitup[i] += ">>>\n<<<"
            elif i == pages - 1:
                splitup[i] += "<<<"

        return splitup

    return [content]

# endregion helpers

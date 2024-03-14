import re

from pysamp.dialog import Dialog
from pysamp.player import Player
from python.utils.enums.dialog_style import DialogStyle
from typing import Callable, Union


class DialogTreeNode:
    def __init__(self,
                 node_name: str,
                 dialog_style: DialogStyle,
                 title: str,
                 content: str,
                 button_1: str,
                 button_2: str,
                 max_list_length: int = 16,
                 jump_to: str = None,
                 exit_on_button_2: bool = False,
                 back_to_root: bool = False,
                 close_in_end: bool = False,
                 back_after_input: bool = False,
                 stay_if_none: bool = True,
                 save_input: bool = False,
                 use_same_children: bool = False,
                 custom_handler: Callable[[Player, int, int, str, ...], bool | None] | None = None,
                 custom_handler_node_parameters: tuple = None,
                 custom_content_handler: Callable[[Player, ...], str] = None,
                 custom_content_handler_node_parameters: tuple[str, ...] = None
                 ) -> None:
        self.__node_name: str = node_name
        self.__dialog_style: DialogStyle = dialog_style
        self.__title: str = title
        self.__content: str = content
        self.__button_1: str = button_1
        self.__button_2: str = button_2
        self.__max_list_length: int = max_list_length
        self.__jump_to: str | None = jump_to
        self.__exit_on_button_2: bool = exit_on_button_2
        self.__back_to_root: bool = back_to_root
        self.__close_in_end: bool = close_in_end
        self.__back_after_input: bool = back_after_input
        self.__stay_if_none: bool = stay_if_none
        self.__save_input: bool = save_input
        self.__use_same_children: bool = use_same_children
        self.__parent: "DialogTreeNode" | None = None
        self.__children: list[Union["DialogTreeNode", None]] = []
        self.__active_page_number: int = 0
        self.__custom_handler: Callable[[Player, int, int, str, ...], bool | None] | None = custom_handler
        self.__custom_content_handler: Callable[[Player, ...], str] | None = custom_content_handler
        self.__custom_content_handler_node_parameters: tuple[str, ...] = custom_content_handler_node_parameters
        self.__custom_handler_node_parameters: tuple[str] = custom_handler_node_parameters
        self.dialog_tree: "DialogTree" | None = None
        self.__selected_page_number: int = 0
        self.__selected_list_item: int = 0

        self.__dialogs: list[Dialog] = []

    def add_child(self, child: Union["DialogTreeNode", None]) -> None:
        self.__children.append(child)
        if child is not None:
            child.__parent = self

        if self.__parent is not None:
            self.dialog_tree = self.__parent.dialog_tree

    def show(self, player: Player):
        if self.dialog_tree is None:
            self.dialog_tree = self.__parent.dialog_tree

        if self.__parent is None:
            self.dialog_tree.node_variables = {}

        args: list[str] = []

        content = self.__content

        if self.__custom_content_handler is not None:
            if self.__custom_content_handler_node_parameters is not None:
                for param in self.__custom_content_handler_node_parameters:
                    node_name = param.split(".")[0]
                    prop = param.split(".")[1]

                    node = self.dialog_tree.root.__find_node_by_name(node_name)

                    prop_key: str = prop + f"_{str(node.__selected_page_number)}_{str(node.__selected_list_item)}"

                    node_var = self.dialog_tree.node_variables.get(node_name)

                    if node_var is not None:
                        node_prop = node_var.get(prop_key)
                        args.append(node_prop)

            c_content = self.__custom_content_handler(player, *args)

            if c_content == "":
                if self.__parent is None or self.__back_to_root:
                    self.dialog_tree.root.show(player)
                    return

                self.__parent.show(player)
                return

            content += c_content

        self.__dialogs = self.__create_dialogs(self.__dialog_style, self.__title, content,
                                               self.__button_1, self.__button_2, self.__max_list_length)

        self.__dialogs[0].show(player)

    def __create_dialogs(self, dialog_style: DialogStyle, title: str, content: str, button_1: str, button_2: str, max_list_length: int) -> list[Dialog]:

        return [Dialog.create(dialog_style, f_title, f_content, button_1, button_2, on_response=self.__handler)
                for f_title, f_content in self.__prepare_content(dialog_style, title, content, max_list_length)]

    def __prepare_content(self, dialog_style: DialogStyle, title: str, content: str, max_list_length: int) -> tuple[str, str]:
        pattern = r'#(.*?)#'
        header = ""

        pages: list[str] = split_content_by_limit(dialog_style, content, max_list_length)
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
                        self.dialog_tree.node_variables[self.__node_name] = {property_key: value}

                        items[j] = items[j].replace(f'#{match}#', value)

                    elif "~>" in match:
                        prop = match.split("~>")[0]
                        value = match.split("~>")[1]

                        property_key: str = prop + f"_{str(i)}_{str(j)}"

                        if self.__node_name in self.dialog_tree.node_variables:
                            self.dialog_tree.node_variables[self.__node_name][property_key] = value

                        else:
                            self.dialog_tree.node_variables[self.__node_name] = {property_key: value}

                        items[j] = items[j].replace(f'#{match}#', "")

                    elif "." in match:
                        node_name = match.split(".")[0]
                        prop = match.split(".")[1]

                        node = self.dialog_tree.root.__find_node_by_name(node_name)
                        prop_key: str = prop + f"_{str(node.__selected_page_number)}_{str(node.__selected_list_item)}"
                        value = self.dialog_tree.node_variables[node_name][prop_key]

                        items[j] = items[j].replace(f'#{match}#', value)

            page_title = title if page_count == 1 else title + f" ({str(i + 1)}" + " / " + f"{str(page_count)})"
            clean_content = '\n'.join(items)

            if dialog_style == DialogStyle.TABLIST_HEADERS and i != 0:
                clean_content = (header + clean_content)

            yield page_title, clean_content

    def __find_node_by_name(self, node_name: str) -> Union["DialogTreeNode", None]:

        for node in self.__children:
            if node.__node_name.lower() == node_name.lower():
                return node

            else:
                r_node = node.__find_node_by_name(node_name)

                if r_node is not None:
                    return r_node

        return None

    def __handler(self, player: Player, response: int, list_item: int, input_text: str):

        if not bool(response):
            if self.__exit_on_button_2 or self.__parent is None:
                return

            if self.__jump_to is not None:
                node = self.dialog_tree.root.__find_node_by_name(self.__jump_to)

                if node is not None:
                    node.show(player)
                    return

                else:
                    self.__parent.show(player)
                    return

            if self.__back_to_root:
                self.dialog_tree.root.show(player)
                return

            self.__parent.show(player)
            return

        if self.__save_input:
            self.dialog_tree.node_variables[self.__node_name] = {'input_value': input_text}

        page_move = 1 if "<<<" in input_text else -1 if ">>>" in input_text else 0

        if page_move != 0:
            self.__active_page_number += page_move
            self.__dialogs[self.__active_page_number].show(player, self.__active_page_number, list_item)
            return

        self.__selected_page_number: int = self.__active_page_number
        self.__selected_list_item: int = list_item

        if self.__custom_handler is not None:
            args: list[str] = []

            if self.__custom_handler_node_parameters is not None:
                for param in self.__custom_handler_node_parameters:
                    node_name = param.split(".")[0]
                    prop = param.split(".")[1]

                    node = self.dialog_tree.root.__find_node_by_name(node_name)

                    prop_key: str = prop + f"_{str(node.__selected_page_number)}_{str(node.__selected_list_item)}"

                    node_var = self.dialog_tree.node_variables.get(node_name)

                    if node_var is not None:
                        node_prop = node_var.get(prop_key)
                        args.append(node_prop)

            custom_handler_result = self.__custom_handler(player, response, list_item, input_text, *args)

            if not custom_handler_result and self.__stay_if_none:
                self.show(player)
                return

        if self.__back_after_input:
            self.__parent.show(player)
            return

        if len(self.__children) != 0 and list_item <= len(self.__children) - 1:
            if list_item == -1:
                self.__children[0].show(player)
                return

            if self.__children[list_item] is None:
                if self.__use_same_children:
                    self.__children[0].show(player)
                    return

                if self.__stay_if_none:
                    self.show(player)
                    return

            else:
                self.__children[list_item].show(player)
                return

        else:
            if self.__use_same_children:
                self.__children[0].show(player)
                return

            if self.__stay_if_none:
                self.show(player)
                return

            if self.__back_to_root:
                self.dialog_tree.root.show(player)
                return

            if self.__close_in_end:
                return

            self.__parent.show(player)

    def __str__(self):
        return self.__node_name


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

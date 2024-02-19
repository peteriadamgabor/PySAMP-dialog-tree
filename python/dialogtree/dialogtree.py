import re

from pysamp.dialog import Dialog
from pysamp.player import Player
from python.utils.enums.dialog_style import DialogStyle
from typing import Callable, NoReturn, Union


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
                 back_to_root: bool = True,
                 close_in_end: bool = False,
                 back_after_save: bool = False,
                 stay_if_none: bool = False,
                 custom_handler: Callable[[Player, int, int, str], NoReturn] | None = None,
                 custom_content_handler: Callable[[...], str] = None,
                 custom_content_handler_node_parameters: tuple[str] = None,
                 custom_handler_node_parameters: tuple = None):

        self.__node_name = node_name
        self.__dialog_style = dialog_style
        self.__title = title
        self.__content = content
        self.__button_1 = button_1
        self.__button_2 = button_2
        self.__max_list_length = max_list_length
        self.__jump_to = jump_to
        self.__exit_on_button_2: bool = exit_on_button_2
        self.__back_to_root: bool = back_to_root
        self.__close_in_end: bool = close_in_end
        self.__back_after_save: bool = back_after_save
        self.__stay_if_none: bool = stay_if_none
        self.__parent: "DialogTreeNode" | None = None
        self.__children = []
        self.__active_page_number = 0
        self.__custom_handler: Callable[[Player, int, int, str, ...], NoReturn] | None = custom_handler
        self.__custom_content_handler: Callable[[...], str] | None = custom_content_handler
        self.__custom_content_handler_node_parameters: tuple[str] = custom_content_handler_node_parameters
        self.__custom_handler_node_parameters: tuple[str] = custom_handler_node_parameters
        self.dialog_tree: "DialogTree" | None = None

        self.__dialogs: list[Dialog] = []

    def add_child(self, child: Union["DialogTreeNode", None]):
        self.__children.append(child)

        if child is not None:
            child.__parent = self

        if self.__parent is not None:
            self.dialog_tree = self.__parent.dialog_tree

    def show(self, player: Player):

        if self.dialog_tree is None:
            self.dialog_tree = self.__parent.dialog_tree

        args: list[str] = []
        if self.__custom_content_handler is not None:
            if self.__custom_content_handler_node_parameters is not None:
                for param in self.__custom_content_handler_node_parameters:
                    node = param.split(".")[0]
                    prop = param.split(".")[1]

                    args.append(self.dialog_tree.node_variables[node][prop])

            self.__content = self.__custom_content_handler(*args)

        self.__dialogs = self.__create_dialogs(self.__dialog_style, self.__title, self.__content,
                                               self.__button_1, self.__button_2, self.__max_list_length)

        self.__dialogs[0].show(player)

    def __create_dialogs(self, dialog_style: DialogStyle, title: str, content: str, button_1: str, button_2: str,
                         max_list_length) -> list[Dialog]:

        pages: list[str] = split_content_by_limit(dialog_style, content, max_list_length)
        r_dialogs = []
        pattern = r'#(.*?)#'

        page_count = len(pages)

        header = ""

        if dialog_style == DialogStyle.TABLIST_HEADERS:
            header = pages[0][:pages[0].find('\n') + 2]

        for i in range(page_count):
            matches = re.findall(pattern, pages[i])

            for match in matches:

                if "->" in match:
                    property = match.split("->")[0]
                    value = match.split("->")[1]

                    self.dialog_tree.node_variables[self.__node_name] = {property: value}

                    pages[i] = pages[i].replace(f'#{match}#', value)

                elif "." in match:
                    node = match.split(".")[0]
                    property = match.split(".")[1]

                    value = self.dialog_tree.node_variables[node][property]

                    pages[i] = pages[i].replace(f'#{match}#', value)

            page_title = title if page_count == 1 else title + f" ({str(i + 1)}" + " / " + f"{str(page_count)})"

            if dialog_style == DialogStyle.TABLIST_HEADERS and i != 0:
                pages[i] = header + pages[i]

            r_dialogs.append(Dialog.create(dialog_style, page_title, pages[i],
                                           button_1, button_2, on_response=self.__handler))

        return r_dialogs

    def __find_root(self) -> "DialogTreeNode":
        """
        Find and return the root node of the tree.
        """
        current_node = self
        while current_node.__parent is not None:
            current_node = current_node.__parent
        return current_node

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

            self.__parent.show(player)
            return

        if ">>>" in input_text:
            self.__active_page_number += 1
            self.__dialogs[self.__active_page_number].show(player)
            return

        if "<<<" in input_text:
            self.__active_page_number -= 1
            self.__dialogs[self.__active_page_number].show(player)
            return

        if self.__custom_handler is not None:

            args: list[str] = []

            if self.__custom_handler_node_parameters is not None:
                for param in self.__custom_handler_node_parameters:
                    node = param.split(".")[0]
                    prop = param.split(".")[1]
                    args.append(self.dialog_tree.node_variables[node][prop])

            self.__custom_handler(player, response, list_item, input_text, *args)

        if self.__jump_to is not None:
            node = self.dialog_tree.root.__find_node_by_name(self.__jump_to)

            if node is not None:
                node.show(player)
                return

            self.dialog_tree.root.show(player)

        if len(self.__children) > 0:
            if list_item == -1:
                self.__children[0].show(player)
                return

            if list_item > len(self.__children) - 1:
                return

            if self.__children[list_item] is None and self.__stay_if_none:
                self.show(player)
                return

            if self.__children[list_item] is not None:
                self.__children[list_item].show(player)
                return

        if self.__back_after_save:
            self.__parent.show(player)
            return

        if self.__back_to_root:
            self.dialog_tree.root.show(player)
            return

        if self.__close_in_end:
            return

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

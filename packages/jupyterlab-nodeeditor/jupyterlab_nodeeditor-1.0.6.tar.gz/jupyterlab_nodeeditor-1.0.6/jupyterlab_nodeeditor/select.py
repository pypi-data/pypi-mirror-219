from typing import List


class option:
    def __init__(self, value, label: str) -> None:
        self.value = value
        self.label = label


class select:
    def __init__(self, options: List[option] = []):
        self.options = options

    def get_show_options(self) -> str:
        ret = []
        index = 0
        for option in self.options:
            ret.append({
                "value": index,
                "label": option.label
            })
            index += 1
        return ret

    def get_option_value(self, index):
        return self.options[index].value

    def add_option(self, option: option):
        self.options.append(option)

    def remove_option(self, value):
        length = len(self.options)
        for i in range(length):
            if (self.options[i].value == value):
                self.options.pop(i)
                return


class mselect:
    def __init__(self, options: List[option] = []):
        self.options = options

    def get_show_options(self) -> str:
        ret = []
        index = 0
        for option in self.options:
            ret.append({
                "value": index,
                "label": option.label
            })
            index += 1
        return ret

    def get_option_value(self, indexs):
        ret = []
        for index in indexs:
            ret.append(self.options[index].value)
        return ret

    def add_option(self, option: option):
        self.options.append(option)

    def remove_option(self, value):
        length = len(self.options)
        for i in range(length):
            if (self.options[i].value == value):
                self.options.pop(i)
                return

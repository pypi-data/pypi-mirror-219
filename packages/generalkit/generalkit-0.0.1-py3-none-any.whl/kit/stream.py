import operator
from functools import reduce


class Stream:

    def __init__(self, elements):
        if isinstance(elements, list):
            self.elements = list(elements)
        elif isinstance(elements, tuple):
            self.elements = tuple(elements)
        elif isinstance(elements, set):
            self.elements = set(elements)
        elif isinstance(elements, dict):
            self.elements = dict(elements)

    def max(self):
        return max(self.elements)

    def min(self):
        return min(self.elements)

    def count(self):
        return len(list(self.elements))

    def reduce(self, lambda_exp):
        return reduce(lambda_exp, self.elements)

    def sum(self):
        self.reduce(lambda x, y: x + y)

    def println(self):
        for i in self.elements:
            print(i)

    def map(self, lambda_exp):
        self.elements = type(self.elements)(map(lambda_exp, self.elements))
        return self

    def remove_left_spaces(self):
        self.map(lambda x: str(x).lstrip())
        return self

    def remove_right_spaces(self):
        self.map(lambda x: str(x).rstrip())
        return self

    def remove_left_right_spaces(self):
        self.map(lambda x: str(x).strip())
        return self

    def remove_chars(self, *string):
        for i in string:
            self.map(lambda x: str(x).replace(i, ''))
        return self

    def distinct(self):
        self.elements = type(self.elements)(set(self.elements))
        return self

    """
    for dict example: lambda a:str(a[0]).startswith('3')
    for list example: lambda a: len(a) > 3
    """

    def filter(self, lambda_exp):
        if isinstance(self.elements, dict):
            self.elements = dict(filter(lambda_exp, self.elements.items()))
        else:
            self.elements = type(self.elements)(filter(lambda_exp, self.elements))
        return self

    def sort(self, sort_key=True, reverse=False):
        if isinstance(self.elements, list):
            self.elements.sort(reverse=reverse)
        elif isinstance(self.elements, tuple) or isinstance(self.elements, set):
            elements = list(self.elements)
            elements.sort(reverse=reverse)
            self.elements = type(self.elements)(elements)
        elif isinstance(self.elements, dict):
            sort_kv = sorted(self.elements.items(), key=operator.itemgetter(0 if sort_key else 1), reverse=reverse)
            self.elements = {k: v for k, v in sort_kv}
        return self

    def add(self, elements):
        if isinstance(self.elements, list):
            self.elements.append(elements)
        elif isinstance(self.elements, tuple) or isinstance(self.elements, set):
            tmp = list(self.elements)
            tmp.append(elements)
            self.elements = type(self.elements)(tmp)
        return self

    def put(self, key, value):
        if isinstance(self.elements, dict):
            self.elements.update({key: value})
        return self

    def remove(self, elements):
        if isinstance(self.elements, list):
            self.elements.remove(elements)
        elif isinstance(self.elements, tuple) or isinstance(self.elements, set):
            tmp = list(self.elements)
            tmp.remove(elements)
            self.elements = type(self.elements)(tmp)
        elif isinstance(self.elements, dict):
            self.elements.pop(elements)
        return self

    def get(self, index=0):
        if isinstance(self.elements, list):
            return self.elements[index]
        elif isinstance(self.elements, tuple) or isinstance(self.elements, set):
            return list(self.elements)[index]
        elif isinstance(self.elements, dict):
            value = self.elements.get(index, 'no such value')
            dict_o = {}
            dict_o.update({index: value})
            return dict_o

    def collect(self):
        return self.elements

    def join(self, splitor):
        if splitor:
            return splitor.join([str(elem) for elem in self.elements])
        else:
            ' '.join([str(elem) for elem in self.elements])

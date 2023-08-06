import logging

from hukudo.xls import TableError

log = logging.getLogger(__name__)


class Table:
    def __init__(self, header: list, data: list[list]):
        self.header = header
        self.data = data

    def __bool__(self):
        """
        Tables are False if they have no data. Useful for checks like "if table: ..."
        """
        return bool(self.data)

    def dicts(self):
        result = []
        for d in self.data:
            result.append({k: v for (k, v) in zip(self.header, d)})
        return result

    def single_dict(self):
        dicts = self.dicts()
        if len(dicts) != 1:
            raise TableError('More than one result found. Please fix your query to return exactly one row.')
        return dicts[0]

    def change_columns(self, mapping: dict = None, capitalize=True):
        """
        Siehe test case.
        """
        if mapping is None:
            mapping = {}
        # header id to new value
        update_names = {self.header.index(k): v for k, v in mapping.items() if v is not None}
        # header ids to drop
        drop_indices = [self.header.index(k) for k, v in mapping.items() if v is None]
        # header id to new value
        capitalize_names = {}
        if capitalize:
            for i, name in enumerate(self.header):
                new_name = name
                if name == 'id':
                    new_name = 'ID'
                elif name not in mapping:
                    new_name = name.capitalize()
                if name != new_name:
                    capitalize_names[i] = new_name
        # last one wins. mapping has prio.
        update_rules = {}
        update_rules.update(capitalize_names)
        update_rules.update(update_names)
        for k, v in update_rules.items():
            self.header[k] = v
        self.header = [x for i, x in enumerate(self.header) if i not in drop_indices]
        for i, row in enumerate(self.data):
            self.data[i] = [x for i, x in enumerate(row) if i not in drop_indices]

import re

from app.utility.base_world import BaseWorld


class BaseObject(BaseWorld):

    def __init__(self):
        self._access = self.Access.APP

    def match(self, criteria):
        if not criteria:
            return self
        criteria_matches = []
        for k, v in criteria.items():
            if type(v) is tuple:
                for val in v:
                    if self.__getattribute__(k) == val:
                        criteria_matches.append(True)
            else:
                if self.__getattribute__(k) == v:
                    criteria_matches.append(True)
        if len(criteria_matches) == len(criteria) and all(criteria_matches):
            return self

    def update(self, field, value):
        if value and (value != self.__getattribute__(field)):
            self.__setattr__(field, value)

    @staticmethod
    def retrieve(collection, unique):
        return next((i for i in collection if i.unique == unique), None)

    @staticmethod
    def hash(s):
        return s

    @staticmethod
    def clean(d):
        for k, v in d.items():
            if v is None:
                d[k] = ''
        return d

    @property
    def access(self):
        return self._access

    @access.setter
    def access(self, value):
        self._access = value

    def replace_app_props(self, encoded_string):
        if encoded_string:
            decoded_test = self.decode_bytes(encoded_string)
            for k, v in self.get_config().items():
                if k.startswith('app.'):
                    re_variable = re.compile(r'#{(%s.*?)}' % k, flags=re.DOTALL)
                    decoded_test = re.sub(re_variable, str(v).strip(), decoded_test)
            return self.encode_string(decoded_test)

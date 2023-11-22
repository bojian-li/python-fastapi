import logging
from dotenv import load_dotenv


def toObject(objt, data):
    for key in data:
        if isinstance(data[key], dict):
            __obj = type(key, (object,), {})()
            obj = toObject(__obj,data[key])
            setattr(objt, key, obj)
        elif isinstance(data[key], list):
            _objs = []
            for index, item in enumerate(data[key]):
                __obj = type(key, (object,), {})()
                _obj = toObject(__obj, item)
                _objs.insert(index, _obj)
            setattr(objt, key, _objs)
        else:
            setattr(objt, key, data[key])

    return objt


class InputParsms:
    def to_json(self):
        return vars(self)


class ApiRequest:
    def __init__(self):
        load_dotenv()

    def set_logger(self, logger: logging):
        self.logger = logger

    # 设置申请参数
    def set_input_params(self, params):
        input = InputParsms()
        self.input = toObject(input, params)

    # 获取申请参数
    def get_input_params(self) -> InputParsms:
        return self.input

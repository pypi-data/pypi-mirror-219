import sys
from rapidfuzz import process, fuzz, utils

dict_config = sys.modules[__name__]
dict_config.fuzzycfg = {"scorer": fuzz.WRatio, "processor": utils.default_process}


class FuzzDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        tmp = {}
        for k, i in super().items():
            tmp[f"{k}{repr(k)}"] = i
        return tmp[
            process.extract(
                f"{key}{repr(key)}", list(tmp), **dict_config.fuzzycfg, limit=1
            )[0][0]
        ]

    def __getattr__(self, item):
        return self.__getitem__(item)

from enum import IntEnum

DataProcessTypes = IntEnum('DataProcessTypes', ('standardization', 'normalization'))
SetTypes = IntEnum('SetTypes', ('train', 'valid', 'test'))
TaskTypes = IntEnum('TaskTypes', ('classification', 'regression'))

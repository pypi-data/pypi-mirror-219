__version__ = "0.0.7"

_POPYROUS_IMPORT_EVERYTHING_ELSE_ = True

if _POPYROUS_IMPORT_EVERYTHING_ELSE_:
    from . matlab import *
    from . packages import *
    from . web import *
    from . zipfiles import *
    from . timeseries import *
    from . utils import *
    from . ml import *

from . import (detection, recognition,recognition_new, tools, data_generation, pipeline,pipeline_new, evaluation, datasets,
               custom_objects)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

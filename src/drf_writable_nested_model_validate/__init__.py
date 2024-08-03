__title__ = 'DRF writable nested model validate'
__version__ = '0.1.0'
__author__ = 'beda.software, giuseppe novielli' 
__license__ = 'BSD 2-Clause'
__copyright__ = 'Copyright 2014-2022 beda.software, Copyright 2024 giuseppe novielli'

# Version synonym
VERSION = __version__


from .mixins import (
    NestedCreateModelValidateMixin,
    NestedUpdateModelValidateMixin,
)
from .serializers import WritableNestedModelSerializer

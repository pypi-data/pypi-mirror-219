# read version from installed package
from importlib.metadata import version
__version__ = version("openwholeslide")

from ._slide import ImageWSI, TiffWSI
from .vectors import FloatVector, IntVector, VectorType
from .wsi import PaddingParameters, Reader, SlideRegion, SlideStack, WholeSlide
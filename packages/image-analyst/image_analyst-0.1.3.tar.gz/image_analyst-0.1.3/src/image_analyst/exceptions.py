class ModelLoadingFailedException(Exception):
    """This type represents a model loading failed exception."""


class AnalysisFailedException(Exception):
    """This type represents an analysis failed exception."""


class DetectionFailedException(Exception):
    """This type represents a detection failed exception."""


class TrackingFailedException(Exception):
    """This type represents a tracking failed exception."""


class InvalidImageException(ValueError):
    """This type represents an invalid image exception."""


class InvalidDimensionsException(ValueError):
    """This type represents an invalid dimensions exception."""


class InvalidDtypeException(ValueError):
    """This type represents an invalid image dtype exception."""


class DownloadFailedException(Exception):
    """Raised when download fails."""

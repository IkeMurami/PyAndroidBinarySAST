from pathlib import Path
from core.data.AppFileType import AppFileType


class AppLoader(object):

    path: Path
    bin_type: AppFileType

    def __init__(self) -> None:
        pass

    def load(self, path: Path, bin_type: AppFileType = AppFileType.APK):
        self.path = path
        self.bin_type = bin_type
        
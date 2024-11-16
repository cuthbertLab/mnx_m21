from music21.converter import subConverters

class MNXConverter(subConverters.SubConverter):
    registerFormats = ('mnx',)
    registerInputExtensions = ('mnx',)
    registerOutputExtensions = ('mnx',)

    def parseData(self, strData: str, number: int | None = None):
        pass

    def parseFile(self, filePath: str, number: int | None = None, **keywords):
        pass

    def write(self, obj, fmt, fp=None, subformats=None, **keywords):
        pass

import typing as t

if t.TYPE_CHECKING:
    from music21 import stream

class MNXWriter:

    def __init__(self):
        self.root = {}

    def fromScore(self, sc: stream.Score):
        pass

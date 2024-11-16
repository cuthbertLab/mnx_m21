import copy
import json
import pathlib
import typing as t

from music21 import clef
from music21 import key
from music21 import meter
from music21 import note
from music21 import stream

if t.TYPE_CHECKING:
    from music21.common.types import OffsetQL


class MNXReader:
    def __init__(self, fp: str | pathlib.Path):
        self.root = {}
        self.globalMeasures: list[stream.Measure | None] = []
        self.globals = {'measures': self.globalMeasures}
        self.stream: stream.Score = stream.Score()
        self.parsedOnePart = False
        if isinstance(fp, str):
            fp = pathlib.Path(fp)

        self.fp: pathlib.Path = fp

    def run(self):
        with open(self.fp, 'r', encoding='utf-8') as f:
            self.root = f.read()
        self.stream = self.parseData()

    def parseData(self) -> stream.Score:
        self.parseGlobal()
        self.parseParts()

        return self.stream

    def parseGlobal(self):
        self.parseGlobalMeasures()

    def parseGlobalMeasures(self):
        gm = self.root['global']['measures']
        for i, m in enumerate(gm):
            if not m:
                self.globalMeasures.append(None)
            else:
                self.globalMeasures.append(self.parseGlobalMeasure(m))

    def parseGlobalMeasure(self, gm: dict) -> stream.Measure:
        m = stream.Measure()
        if 'key' in gm:
            k = key.KeySignature()
            k.sharps = gm['key']['fifths']
            m.coreInsert(0, k)
        if 'time' in gm:
            ts = meter.TimeSignature(gm['time']['signature'])
            # t.numerator = gm['time']['beats']
            # t.denominator = gm['time']['beat-type']
            m.coreInsert(0, ts)

        m.coreElementsChanged(updateIsFlat=False)

        return m

    def parseParts(self):
        for p in self.root['parts']:
            self.parsePart(p)
            self.parsedOnePart = True

    def parsePart(self, pMNX: dict) -> stream.Part:
        p = stream.Part()
        for i, m in enumerate(pMNX['measures']):
            p.coreAppend(self.parseMeasure(i, m))
        p.coreElementsChanged()
        return p

    def parseMeasure(self, measureIndex: int, mMNX: dict) -> stream.Measure:
        m = stream.Measure()
        if self.globalMeasures[measureIndex]:
            for el in self.globalMeasures[measureIndex]:
                if self.parsedOnePart:
                    m.coreInsert(0.0, copy.deepcopy(el))
                else:
                    m.coreInsert(0.0, el)

        con = mMNX['content']
        for i, c in enumerate(con):
            ty = c['type']
            if ty == 'clef':
                clefObj = clef.clefFromString(c['sign'] + str(c['line']))
                m.coreInsert(0, clefObj)
            elif ty == 'sequence':
                pass
                

        m.coreElementsChanged()
        return m

    # def parseSequence(self, seq: list[dict], s: stream.Measure | stream.Voice, index: OffsetQL = 0.0):
    #     for i, c in enumerate(seq):
    #         if c['type'] == 'note':
    #             m.coreAppend(self.parseNote(
    #                 measureIndex, i, c['pitch'], c['duration'], c['voice']))
    #         elif c['type'] == 'rest':
    #             m.coreAppend(self.parseRest(
    #                 measureIndex, i, c['duration'], c['voice']))
    #         elif c['type'] == 'clef':
    #             m.coreAppend(self.parseClef(
    #                 measureIndex, i, c['sign'], c['line']))
    #         elif c['type'] == 'key':
    #             m.coreAppend(self.parseKey(
    #                 measureIndex, i, c['fifths']))
    #         elif c['type'] == 'time':
    #             m.coreAppend(self.parseTime(
    #                 measureIndex, i, c['signature']))
    #         elif c['type'] == 'barline':
    #             m.coreAppend(self.parseBarline(
    #                 measureIndex, i, c['style']))
    #         else:
    #             raise ValueError(f'Unknown type: {c["type"]}')

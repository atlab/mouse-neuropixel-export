from enty import Schema
from . import dataclass, PickleAdapter

schema = Schema(
    prefix='ephys',
    base_dir='/mnt/at-export01/mouse_neuropixel_export/schemas/ephys',
    make_dir=True,
    append_class_sub_dir=True
)

@schema
class ProbeInsertion(PickleAdapter):
    @dataclass
    class Key:
        animal_id: int


@schema
class Session(PickleAdapter):
    @dataclass
    class Key:
        animal_id: int
        session: int
        scan_idx: int


@schema
class EphysFileMetadata(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class EphysRecording(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class Clustering(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class Curation(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class CuratedClustering(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class PeakWaveForm(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class WaveForm(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass


@schema
class QualityMetrics(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        pass
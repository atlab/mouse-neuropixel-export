from enty import Schema
from . import dataclass, PickleAdapter

schema = Schema(
    prefix='metadata',
    base_dir='/mnt/at-export01/mouse_neuropixel_export/schemas/metadata',
    make_dir=True,
    append_class_sub_dir=True
)

@schema
class ScanKey(PickleAdapter):
    @dataclass
    class Key():
        animal_id: int
        session: int
        scan_idx: int


@schema
class StimKey(PickleAdapter):
    @dataclass
    class Key():
        collection_id: int
        image_class: str


@schema
class ScanStimKey(PickleAdapter):
    @dataclass
    class Key(StimKey.Key, ScanKey.Key):
        pass
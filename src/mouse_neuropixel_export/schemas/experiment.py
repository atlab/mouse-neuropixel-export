from enty import Schema
from . import dataclass, PickleAdapter

schema = Schema(
    prefix='exp',
    base_dir='/mnt/at-export01/mouse_neuropixel_export/schemas/experiment',
    make_dir=True,
    append_class_sub_dir=True
)

@schema
class Session(PickleAdapter):
    @dataclass
    class Key():
        animal_id: int
        session: int


@schema
class Scan(PickleAdapter):
    @dataclass
    class Key(Session.Key):
        scan_idx : int
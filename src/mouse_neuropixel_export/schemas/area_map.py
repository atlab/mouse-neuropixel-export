from enty import Schema
from . import dataclass, PickleAdapter

schema = Schema(
    prefix='area_map',
    base_dir='/mnt/at-export01/mouse_neuropixel_export/schemas/area_map',
    make_dir=True,
    append_class_sub_dir=True
)

@schema
class AreaPerUnit(PickleAdapter):
    @dataclass
    class Key():
        animal_id: int
        session: int
        scan_idx: int
import datetime
from collections import Counter
from dataclasses import dataclass, field
from itertools import chain


@dataclass
class Device:
    BinType: str
    NullBin: str | int
    ProductId: str | None = None
    LotId: str | None = None
    WaferSize: float | None = None
    CreateDate: datetime.datetime | None = None
    DeviceSizeX: float | None = None
    DeviceSizeY: float | None = None
    SupplierName: str | None = None
    OriginLocation: int | None = None
    MapType: str = 'Array'
    Orientation: float = 0
    reference_xy: tuple[int, int] | None = None

    bin_pass: dict[int | str, bool] = field(default_factory=dict)  # Is this bin passing?
    map: list[list[int]] | list[list[str]] = field(default_factory=list)   # The actual map
    data_misc: dict[str, str] = field(default_factory=dict)    # <Data attribs>
    supplier_data: dict[str, str] = field(default_factory=dict)    # <SupplierData attribs>

    misc: dict[str, str] = field(default_factory=dict)  # Any unexpected fields go here

    @property
    def Rows(self) -> int:
        return len(self.map)

    @property
    def Columns(self) -> int:
        if self.Rows == 0:
            return 0
        return len(self.map[0])

    def bin_counts(self) -> Counter:
        return Counter(chain(*self.map))


@dataclass
class Map:
    xmlns: str = 'http://www.semi.org'
    FormatRevision: str = "SEMI G85 0703"
    SubstrateType: str | None = None
    SubstrateId: str | None = None

    devices: list[Device] = field(default_factory=list)
    misc: dict[str, str] = field(default_factory=dict)  # Any unexpected fields go here


from __future__ import annotations

from typing import Any, Union, Dict, List, Callable, Tuple, Type
from collections.abc import Iterable
from pathlib import Path
from collections import OrderedDict
from loguru import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .layout import DataLayout

from ..common import get_class_name
from pydlmeta.identifier.types import DatasetFormat


class Dataset:

    def __init__(self,
                 raw_dataset: Union[Iterable, Iterable[Path], object],
                 format: DatasetFormat = DatasetFormat.NON_SPECIFIED):
        """
        Do not put identify_format in Dataset. Make sure
        (MVC) control and model are separated .
        """
        if isinstance(raw_dataset, str):
            self.src = Path(raw_dataset)
        else:
            self.src =  raw_dataset
        self.y_label: OrderedDict[str, Union[int, float, str]] = OrderedDict()
        self.layout: Union[None, DataLayout] = None

        self.shape: Union[None, Tuple[int, ...]] = None

        self.format = format

    def clone_attributes(self, dataset: Type[Dataset]) -> None:
        """
        Clone user defined attributes from input

        Iter all user-defined attributes and check if they have values.
        If the attribute of the destination object has value, then skip
        the clone.
        Args:
            dataset Type[Dataset]: The dataset object to be cloned
        """

        _to_be_cloned: List = []
        for attr_name in dataset.__dict__:

            dst_value = getattr(self, attr_name)
            src_value = getattr(dataset, attr_name)

            if (isinstance(dst_value, OrderedDict)) or (isinstance(
                    dst_value, List)):
                if len(dst_value) == 0:
                    _to_be_cloned.append([attr_name, src_value])

            elif dst_value is None:
                _to_be_cloned.append([attr_name, src_value])

        for attr_name, src_value in _to_be_cloned:
            setattr(self, attr_name, src_value)

    def dump(self) -> Dict:
        """
        WARNING: the dumped dictionary can only be used for report
        since src can be path or class name (which is not a good design)
        """
        data = {
            "src": "",
            "y_label": self.y_label,
            "shape": self.shape,
            "layout": self.layout.dump() if self.layout is not None else None,
            "format": self.format.name
        }

        if isinstance(self.src, str):
            data["src"] = self.src
        elif isinstance(self.src, Path):
            data["src"] = str(self.src)
        else:
            data["src"] = get_class_name(self.src)

        return data

    def load(self, obj: Dict):
        raise NotImplementedError()


class ONNCDataset(Dataset):

    def __init__(self):
        super().__init__([])
        self.format = DatasetFormat.ONNC_DATASET


class NDARRAYDataset(Dataset):

    def __init__(self, raw_dataset: Iterable):
        super().__init__(raw_dataset)
        self.format = DatasetFormat.NDARRAY

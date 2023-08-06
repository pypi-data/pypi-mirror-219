"""PyTorch data utility functions to be found here."""
from typing import Any, List, Sequence, Union, cast

import numpy as np
import torch

from bitfount.data.types import _DataBatch, _SingleOrMulti


def _index_tensor_handler(
    idx: Union[int, Sequence[int], torch.Tensor]
) -> Union[int, Sequence[int]]:
    """Converts pytorch tensors to integers or lists of integers for indexing."""
    if torch.is_tensor(idx):
        idx = cast(torch.Tensor, idx)
        list_idx: list = idx.tolist()
        return list_idx
    else:
        idx = cast(Union[int, Sequence[int]], idx)
        return idx


def _convert_batch_to_tensor(
    batch: _DataBatch,
) -> List[_SingleOrMulti[torch.Tensor]]:
    """Converts a batch of data containing numpy arrays to torch tensors.

    Data must be explicitly converted to torch tensors since the PyTorch DataLoader
    which does this automatically is not being used.
    """
    x: List[Any] = []
    num_x_elements_per_batch = len(
        batch[0][0]
    )  # Subset of [tabular, images, suplementary]
    for i in range(num_x_elements_per_batch):
        list_of_x_elements = [sample[0][i] for sample in batch]
        tensor_list = []
        try:
            for j in range(len(list_of_x_elements)):
                tensor = torch.tensor(list_of_x_elements[j], dtype=torch.float32)
                tensor_list.append(tensor)
            x.append(torch.stack(tensor_list))
        # A value error is raised if list elements are of different shapes. This happens
        # for instance when not all images in the array have the same shapes.
        except ValueError:
            images_list = []
            for img_num in range(len(list_of_x_elements[0])):
                stacked = torch.stack(
                    [
                        torch.tensor(batch_item[img_num], dtype=torch.float32)
                        for batch_item in list_of_x_elements
                    ]
                )
                images_list.append(stacked)
            x.append(images_list)
    y = torch.from_numpy(np.array([b[1] for b in batch]))

    return [x, y]

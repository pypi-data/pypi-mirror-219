import typing
import dataclasses
import logging
from collections import defaultdict
import numpy as np
import torch
import irisml.core

logger = logging.getLogger(__name__)

IMAGE_PLACEHOLDER = '<|image|>'
EXTRA_PLACEHOLDER = '<|extra|>'


class DatasetWithExtraInput(torch.utils.data.Dataset):
    def __init__(self, dataset, context_dataset, class_names, predictions, top_k,
                 fixed_text='', use_helper_confidence=False, context_predictions=None):
        super().__init__()
        self._dataset = dataset
        self._context_dataset = context_dataset
        self._top_k = top_k
        # get indices and values of top-k predictions
        self._inds = np.argsort(predictions, axis=1)[:, -1:-1-top_k:-1]
        self._vals = np.take_along_axis(predictions, self._inds, axis=1)
        # self._vals, self._inds = torch.topk(predictions, self._top_k, dim=1, sorted=True)
        self._use_helper_confidence = use_helper_confidence
        self._context_predictions = context_predictions
        self._class_names = class_names
        self._fixed_text = fixed_text

    def __len__(self):
        return len(self._dataset)

    def _construct(self, index):
        topk_class_ids = self._inds[index]
        # topk_confidence = self._vals[index]
        # logger.info(f'topk {topk_class_ids}')
        # logger.info(f'confidence {topk_confidence}')

        context_by_targets = defaultdict(list)
        for input, tgt in self._context_dataset:
            if tgt.item() in topk_class_ids:
                context_by_targets[tgt.item()].append(input)
        # logging.info(f'dict::: {context_by_targets}')

        text = ''
        context_images = []
        for tgt in topk_class_ids:
            img_placeholders = ', '.join([IMAGE_PLACEHOLDER] * len(context_by_targets[tgt]))
            t = f'category: "{self._class_names[tgt]}", reference image: {img_placeholders}' + '\n'
            text += t
            context_images += context_by_targets[tgt]

        if self._fixed_text:
            text = self._fixed_text.replace(EXTRA_PLACEHOLDER, text)
        logger.info(f'Index {index}, constructed prompt: {text}')
        return text, context_images

    def __getitem__(self, index):
        input, target = self._dataset[index]
        text, context_images = self._construct(index)
        images = context_images + [input]  # append the test image to the last one
        return (images, text), target


class Task(irisml.core.TaskBase):
    """Make a classification dataset with extra inputs.

    This task takes a dataset and extra inputs (same length) and returns a new dataset
    with each item added to the inputs .
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        fixed_text: str
        extra_input: typing.Union[typing.List, torch.Tensor]  # length: N
        context_dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Config:
        class_names: typing.List[str]
        top_k: int = 5
        context: bool = False
        helper_confidence: bool = False

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset

    def execute(self, inputs):
        extra_input = inputs.extra_input.cpu().numpy()
        self.config.top_k = min(self.config.top_k, len(self.config.class_names))
        # logger.info(f'extra input shape: {extra_input.shape}')
        # if inputs.extra_input else torch.rand([len(inputs.dataset), self.config.top_k])
        if len(inputs.dataset) != len(extra_input):
            raise ValueError(f"Dataset and extra inputs have different lengths: {len(inputs.dataset)} vs {len(inputs.extra_input)}")

        # TEMP: construct top-n confidence
        # def _formatter(prediction, top_k, class_names):
        #     vals, inds = torch.topk(predictions, top_k, sorted=True)
        #     template = f"The weak classifier's top {top_k} predictions are: "
        #     template += ", ".join([f"{class_names[ind]} with a confidence of {val:.2f}" for val, ind in zip(vals, inds)])
        #     logger.info(f"Constructed {template}")
        #     return template
        # extra_input = [_formatter(pred, self.config.top_k, inputs.class_names) for pred in inputs.extra_input]

        return self.Outputs(dataset=DatasetWithExtraInput(inputs.dataset, inputs.context_dataset, self.config.class_names, extra_input,
                                                          self.config.top_k, inputs.fixed_text, self.config.helper_confidence, None))

    def dry_run(self, inputs):
        return self.execute(inputs)

"""
Introducing CVAL Rest API, a powerful tool for AI developers in the computer vision field.
Our service combines the concepts of human-in-the-loop and active learning to improve the quality of
your models and minimize annotation costs for classification, detection, and segmentation cases.

With CVAL, you can iteratively improve your models by following our active learning loop.
First, manually or semi-automatically annotate a random set of images.
Next, train your model and use uncertainty and diversity methods to score the remaining images for annotation.
Then, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.
Repeat this process until you achieve an acceptable quality of the model.

Our service makes it easy to implement this workflow and improve your models quickly and efficiently.
Try our demo notebook to see how CVAL can revolutionize your computer vision projects.

To obtain a client_api_key, please send a request to k.suhorukov@digital-quarters.com
"""
from typing import List, Optional
from pydantic import validator

from pydantic import BaseModel, Field


class BBoxScores(BaseModel):
    """
    :param category_id: id of the category in FramePrediction namespace
    :param score: prediction of model on that bbox
    """
    category_id: str
    score: float


class FramePrediction(BaseModel):
    """
    :param frame_id: id of the frame
    :param predictions: bbox scores
    """
    frame_id: str = Field(max_length=32)
    predictions: Optional[List[BBoxScores]]


class DetectionSamplingOnPremise(BaseModel):
    """
    :param num_of_samples: absolute number of samples to select
    :param bbox_selection_policy:
    Which bounding box to select when there are multiple boxes on an image,
    according to their confidence. Currently supports: min, max, mean
    :selection_strategy: Currently supports: margin, least, ratio, entropy
    :param frames: prediction for th picture and the bbox
    :type frames: List[FramePrediction]
    :raises ValueError if value not in allowed
    """
    num_of_samples: int
    bbox_selection_policy: str
    selection_strategy: str
    sort_strategy: str
    frames: List[FramePrediction]

    @validator('bbox_selection_policy')
    def validate_bbox_selection_policy(cls, value):
        allowed = ['min', 'max', 'sum', 'mean']
        if value not in allowed:
            raise ValueError(f"allowed bbox_selection_policy = {allowed}")
        return value

    @validator('selection_strategy')
    def validate_selection_strategy(cls, value):
        allowed = 'margin,least,ratio,entropy,probability'.split(',')
        if value not in allowed:
            raise ValueError(f"allowed selection_strategy = {allowed}")
        return value

    @validator('sort_strategy')
    def validate_sort_strategy(cls, value):
        allowed = 'ascending,descending'.split(',')
        if value not in allowed:
            raise ValueError(f"allowed sort_strategy = {allowed}")
        return value

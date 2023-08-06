from __future__ import annotations

from typing import Any, Optional

import label_studio_sdk
from pydantic import BaseModel

LS_API_KEY = 'slingshot'
LS_URL = '<your-label-studio-app-url>'


class LabelStudioAnnotation(BaseModel):
    id: int
    annotator: int
    annotation_id: int
    created_at: str
    updated_at: str
    lead_time: float
    choice: Optional[str]
    label: Any
    image: Optional[str]
    text: Optional[str]
    audio: Optional[str]


def get_label_studio_annotations(ls_client: label_studio_sdk.Client) -> list[LabelStudioAnnotation]:
    project = ls_client.get_project(id=1)
    res = project.export_tasks(export_type='JSON_MIN')
    return [LabelStudioAnnotation.parse_obj(annotation_obj) for annotation_obj in res]


def main():
    ls_client = label_studio_sdk.Client(url=LS_URL, api_key=LS_API_KEY)
    ls_annotations = get_label_studio_annotations(ls_client)
    for annotation in ls_annotations:
        raise NotImplementedError('Implement this function to update your dataset using Label Studio annotations!')


if __name__ == "__main__":
    main()

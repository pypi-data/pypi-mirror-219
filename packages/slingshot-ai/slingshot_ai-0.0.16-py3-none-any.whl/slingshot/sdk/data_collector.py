import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from .slingshot_sdk import SlingshotSDK


class DataCollector:
    def __init__(
        self, dataset_artifact_tag: str, max_samples_not_uploaded: int = 10, *, sdk: SlingshotSDK | None = None
    ):
        self.dataset_artifact_tag = dataset_artifact_tag
        # TODO: create async task to upload at least every X min iff there are pending samples
        self.last_added_timestamp = datetime.now()
        self.new_samples: list[dict[str, Any]] = []
        self.max_samples_not_uploaded = max_samples_not_uploaded
        self.sdk = sdk or SlingshotSDK()
        self.production_dataset_path = Path(tempfile.gettempdir()) / "production-data.jsonl"

    async def add_data(self, example: dict[str, Any], max_seconds_without_update: int = 600) -> None:
        self.new_samples.append(example)
        new_sample_count = len(self.new_samples)
        time_since_last_update = datetime.now() - self.last_added_timestamp
        if (
            new_sample_count >= self.max_samples_not_uploaded
            or time_since_last_update.seconds > max_seconds_without_update
        ):
            print(f"Uploading {new_sample_count} new samples to artifact 'production-collected-dataset'")
            self.last_added_timestamp = datetime.now()
            await self.upload_data()
            self.new_samples = []

    async def get_latest_artifact_from_tag(self, tag: str) -> str | None:
        artifacts = await self.sdk.list_artifacts(tag=tag)
        if not artifacts:
            return None
        return artifacts[0].blob_artifact_id

    async def update_current_dataset(self) -> None:
        artifact_id = await self.get_latest_artifact_from_tag(self.dataset_artifact_tag)
        if not artifact_id:
            return
        await self.sdk.download_artifact(artifact_id, str(self.production_dataset_path))

    async def upload_data(self) -> None:
        # TODO: How do we handle concurrency?
        with open(self.production_dataset_path, "a") as f:
            await self.update_current_dataset()
            for example in self.new_samples:
                f.write(json.dumps(example) + "\n")
        await self.sdk.upload_artifact(
            self.production_dataset_path, blob_artifact_tag=self.dataset_artifact_tag, as_zip=False
        )

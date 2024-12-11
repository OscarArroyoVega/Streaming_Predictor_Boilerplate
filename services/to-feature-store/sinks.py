import hopsworks
import pandas as pd
from quixstreams.sinks.base import BatchingSink, SinkBackpressureError, SinkBatch


class HopsworksSink(BatchingSink):
    """
    Some sink writing data to a database
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],
        feature_group_event_time: str,
    ):
        """
        Stablish a connection to the feature store Hopsworks
        """

        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version

        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._fs = project.get_feature_store()  # pointer to the feature store
        self._fg = self._fs.get_or_create_feature_group(
            name=self.feature_group_name,
            version=self.feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,
        )  # pointer to the feature group

        # call the constructor of the base class to make sure that batches are inizialized
        super().__init__()

    def write(self, batch: SinkBatch):
        # Convert the batch to a list of dictionaries
        data = [item.value for item in batch]

        data = pd.DataFrame(data)

        try:
            # Try to write data to the db
            self._fg.insert(data)
        except TimeoutError as err:
            # In case of timeout, tell the app to wait for 30s
            # and retry the writing later
            raise SinkBackpressureError(
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err

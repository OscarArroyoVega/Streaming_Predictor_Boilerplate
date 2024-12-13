from datetime import datetime, timezone

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
        feature_group_materialization_minutes: int,
        feature_group_event_time: str,
    ):
        """
        Stablish a connection to the feature store Hopsworks
        """

        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version
        self.feature_group_materialization_minutes = (
            feature_group_materialization_minutes
        )

        # Connect to the feature store, initialize the feature store and the feature group
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._fs = project.get_feature_store()  # pointer to the feature store
        self._fg = self._fs.get_or_create_feature_group(
            name=self.feature_group_name,
            version=self.feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,
        )  # pointer to the feature group

        # set materialization interval
        self._fg.materialization_job.schedule(
            cron_expression=f'0 0/{self.feature_group_materialization_minutes} * ? * * *',
            start_time=datetime.now(tz=timezone.utc),
        )
        # call the constructor of the base class to make sure that batches are inizialized
        super().__init__()

    # Write the data to the feature store
    def write(self, batch: SinkBatch):
        """
        1. Convert the batch to a list of dictionaries
        2. Convert the list of dictionaries to a pandas dataframe
        3. Write the data to the feature store
        """
        # 1. Convert the batch to a list of dictionaries
        data = [item.value for item in batch]
        # Convert the list of dictionaries to a pandas dataframe
        data = pd.DataFrame(data)
        # Write the data to the feature store
        try:
            self._fg.insert(data)
        except TimeoutError as err:
            raise SinkBackpressureError(
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err

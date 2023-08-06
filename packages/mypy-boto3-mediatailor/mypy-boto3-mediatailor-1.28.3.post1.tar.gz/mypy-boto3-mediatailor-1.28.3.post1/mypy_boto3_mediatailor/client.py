"""
Type annotations for mediatailor service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_mediatailor.client import MediaTailorClient

    session = Session()
    client: MediaTailorClient = session.client("mediatailor")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import PlaybackModeType, TierType
from .paginator import (
    GetChannelSchedulePaginator,
    ListAlertsPaginator,
    ListChannelsPaginator,
    ListLiveSourcesPaginator,
    ListPlaybackConfigurationsPaginator,
    ListPrefetchSchedulesPaginator,
    ListSourceLocationsPaginator,
    ListVodSourcesPaginator,
)
from .type_defs import (
    AccessConfigurationTypeDef,
    AdBreakTypeDef,
    AvailSuppressionTypeDef,
    BumperTypeDef,
    CdnConfigurationTypeDef,
    ConfigureLogsForChannelResponseOutputTypeDef,
    ConfigureLogsForPlaybackConfigurationResponseOutputTypeDef,
    CreateChannelResponseOutputTypeDef,
    CreateLiveSourceResponseOutputTypeDef,
    CreatePrefetchScheduleResponseOutputTypeDef,
    CreateProgramResponseOutputTypeDef,
    CreateSourceLocationResponseOutputTypeDef,
    CreateVodSourceResponseOutputTypeDef,
    DashConfigurationForPutTypeDef,
    DefaultSegmentDeliveryConfigurationTypeDef,
    DescribeChannelResponseOutputTypeDef,
    DescribeLiveSourceResponseOutputTypeDef,
    DescribeProgramResponseOutputTypeDef,
    DescribeSourceLocationResponseOutputTypeDef,
    DescribeVodSourceResponseOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetChannelPolicyResponseOutputTypeDef,
    GetChannelScheduleResponseOutputTypeDef,
    GetPlaybackConfigurationResponseOutputTypeDef,
    GetPrefetchScheduleResponseOutputTypeDef,
    HttpConfigurationTypeDef,
    HttpPackageConfigurationTypeDef,
    ListAlertsResponseOutputTypeDef,
    ListChannelsResponseOutputTypeDef,
    ListLiveSourcesResponseOutputTypeDef,
    ListPlaybackConfigurationsResponseOutputTypeDef,
    ListPrefetchSchedulesResponseOutputTypeDef,
    ListSourceLocationsResponseOutputTypeDef,
    ListTagsForResourceResponseOutputTypeDef,
    ListVodSourcesResponseOutputTypeDef,
    LivePreRollConfigurationTypeDef,
    ManifestProcessingRulesTypeDef,
    PrefetchConsumptionTypeDef,
    PrefetchRetrievalTypeDef,
    PutPlaybackConfigurationResponseOutputTypeDef,
    RequestOutputItemTypeDef,
    ScheduleConfigurationTypeDef,
    SegmentDeliveryConfigurationTypeDef,
    SlateSourceTypeDef,
    UpdateChannelResponseOutputTypeDef,
    UpdateLiveSourceResponseOutputTypeDef,
    UpdateProgramResponseOutputTypeDef,
    UpdateProgramScheduleConfigurationTypeDef,
    UpdateSourceLocationResponseOutputTypeDef,
    UpdateVodSourceResponseOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaTailorClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]


class MediaTailorClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaTailorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#close)
        """

    def configure_logs_for_channel(
        self, *, ChannelName: str, LogTypes: Sequence[Literal["AS_RUN"]]
    ) -> ConfigureLogsForChannelResponseOutputTypeDef:
        """
        Configures Amazon CloudWatch log settings for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.configure_logs_for_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#configure_logs_for_channel)
        """

    def configure_logs_for_playback_configuration(
        self, *, PercentEnabled: int, PlaybackConfigurationName: str
    ) -> ConfigureLogsForPlaybackConfigurationResponseOutputTypeDef:
        """
        Amazon CloudWatch log settings for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.configure_logs_for_playback_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#configure_logs_for_playback_configuration)
        """

    def create_channel(
        self,
        *,
        ChannelName: str,
        Outputs: Sequence[RequestOutputItemTypeDef],
        PlaybackMode: PlaybackModeType,
        FillerSlate: SlateSourceTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        Tier: TierType = ...
    ) -> CreateChannelResponseOutputTypeDef:
        """
        Creates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#create_channel)
        """

    def create_live_source(
        self,
        *,
        HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef],
        LiveSourceName: str,
        SourceLocationName: str,
        Tags: Mapping[str, str] = ...
    ) -> CreateLiveSourceResponseOutputTypeDef:
        """
        The live source configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_live_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#create_live_source)
        """

    def create_prefetch_schedule(
        self,
        *,
        Consumption: PrefetchConsumptionTypeDef,
        Name: str,
        PlaybackConfigurationName: str,
        Retrieval: PrefetchRetrievalTypeDef,
        StreamId: str = ...
    ) -> CreatePrefetchScheduleResponseOutputTypeDef:
        """
        Creates a prefetch schedule for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_prefetch_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#create_prefetch_schedule)
        """

    def create_program(
        self,
        *,
        ChannelName: str,
        ProgramName: str,
        ScheduleConfiguration: ScheduleConfigurationTypeDef,
        SourceLocationName: str,
        AdBreaks: Sequence[AdBreakTypeDef] = ...,
        LiveSourceName: str = ...,
        VodSourceName: str = ...
    ) -> CreateProgramResponseOutputTypeDef:
        """
        Creates a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_program)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#create_program)
        """

    def create_source_location(
        self,
        *,
        HttpConfiguration: HttpConfigurationTypeDef,
        SourceLocationName: str,
        AccessConfiguration: AccessConfigurationTypeDef = ...,
        DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef = ...,
        SegmentDeliveryConfigurations: Sequence[SegmentDeliveryConfigurationTypeDef] = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateSourceLocationResponseOutputTypeDef:
        """
        Creates a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_source_location)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#create_source_location)
        """

    def create_vod_source(
        self,
        *,
        HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef],
        SourceLocationName: str,
        VodSourceName: str,
        Tags: Mapping[str, str] = ...
    ) -> CreateVodSourceResponseOutputTypeDef:
        """
        The VOD source configuration parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.create_vod_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#create_vod_source)
        """

    def delete_channel(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Deletes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_channel)
        """

    def delete_channel_policy(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        The channel policy to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_channel_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_channel_policy)
        """

    def delete_live_source(self, *, LiveSourceName: str, SourceLocationName: str) -> Dict[str, Any]:
        """
        The live source to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_live_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_live_source)
        """

    def delete_playback_configuration(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_playback_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_playback_configuration)
        """

    def delete_prefetch_schedule(
        self, *, Name: str, PlaybackConfigurationName: str
    ) -> Dict[str, Any]:
        """
        Deletes a prefetch schedule for a specific playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_prefetch_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_prefetch_schedule)
        """

    def delete_program(self, *, ChannelName: str, ProgramName: str) -> Dict[str, Any]:
        """
        Deletes a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_program)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_program)
        """

    def delete_source_location(self, *, SourceLocationName: str) -> Dict[str, Any]:
        """
        Deletes a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_source_location)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_source_location)
        """

    def delete_vod_source(self, *, SourceLocationName: str, VodSourceName: str) -> Dict[str, Any]:
        """
        The video on demand (VOD) source to delete.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.delete_vod_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#delete_vod_source)
        """

    def describe_channel(self, *, ChannelName: str) -> DescribeChannelResponseOutputTypeDef:
        """
        Describes a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#describe_channel)
        """

    def describe_live_source(
        self, *, LiveSourceName: str, SourceLocationName: str
    ) -> DescribeLiveSourceResponseOutputTypeDef:
        """
        The live source to describe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_live_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#describe_live_source)
        """

    def describe_program(
        self, *, ChannelName: str, ProgramName: str
    ) -> DescribeProgramResponseOutputTypeDef:
        """
        Describes a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_program)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#describe_program)
        """

    def describe_source_location(
        self, *, SourceLocationName: str
    ) -> DescribeSourceLocationResponseOutputTypeDef:
        """
        Describes a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_source_location)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#describe_source_location)
        """

    def describe_vod_source(
        self, *, SourceLocationName: str, VodSourceName: str
    ) -> DescribeVodSourceResponseOutputTypeDef:
        """
        Provides details about a specific video on demand (VOD) source in a specific
        source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.describe_vod_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#describe_vod_source)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#generate_presigned_url)
        """

    def get_channel_policy(self, *, ChannelName: str) -> GetChannelPolicyResponseOutputTypeDef:
        """
        Returns the channel's IAM policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_channel_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_channel_policy)
        """

    def get_channel_schedule(
        self,
        *,
        ChannelName: str,
        DurationMinutes: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> GetChannelScheduleResponseOutputTypeDef:
        """
        Retrieves information about your channel's schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_channel_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_channel_schedule)
        """

    def get_playback_configuration(
        self, *, Name: str
    ) -> GetPlaybackConfigurationResponseOutputTypeDef:
        """
        Retrieves a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_playback_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_playback_configuration)
        """

    def get_prefetch_schedule(
        self, *, Name: str, PlaybackConfigurationName: str
    ) -> GetPrefetchScheduleResponseOutputTypeDef:
        """
        Retrieves a prefetch schedule for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_prefetch_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_prefetch_schedule)
        """

    def list_alerts(
        self, *, ResourceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAlertsResponseOutputTypeDef:
        """
        Lists the alerts that are associated with a MediaTailor channel assembly
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_alerts)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_alerts)
        """

    def list_channels(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListChannelsResponseOutputTypeDef:
        """
        Retrieves information about the channels that are associated with the current
        AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_channels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_channels)
        """

    def list_live_sources(
        self, *, SourceLocationName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListLiveSourcesResponseOutputTypeDef:
        """
        Lists the live sources contained in a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_live_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_live_sources)
        """

    def list_playback_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPlaybackConfigurationsResponseOutputTypeDef:
        """
        Retrieves existing playback configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_playback_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_playback_configurations)
        """

    def list_prefetch_schedules(
        self,
        *,
        PlaybackConfigurationName: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        StreamId: str = ...
    ) -> ListPrefetchSchedulesResponseOutputTypeDef:
        """
        Lists the prefetch schedules for a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_prefetch_schedules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_prefetch_schedules)
        """

    def list_source_locations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSourceLocationsResponseOutputTypeDef:
        """
        Lists the source locations for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_source_locations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_source_locations)
        """

    def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseOutputTypeDef:
        """
        A list of tags that are associated with this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_tags_for_resource)
        """

    def list_vod_sources(
        self, *, SourceLocationName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListVodSourcesResponseOutputTypeDef:
        """
        Lists the VOD sources contained in a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.list_vod_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#list_vod_sources)
        """

    def put_channel_policy(self, *, ChannelName: str, Policy: str) -> Dict[str, Any]:
        """
        Creates an IAM policy for the channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.put_channel_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#put_channel_policy)
        """

    def put_playback_configuration(
        self,
        *,
        Name: str,
        AdDecisionServerUrl: str = ...,
        AvailSuppression: AvailSuppressionTypeDef = ...,
        Bumper: BumperTypeDef = ...,
        CdnConfiguration: CdnConfigurationTypeDef = ...,
        ConfigurationAliases: Mapping[str, Mapping[str, str]] = ...,
        DashConfiguration: DashConfigurationForPutTypeDef = ...,
        LivePreRollConfiguration: LivePreRollConfigurationTypeDef = ...,
        ManifestProcessingRules: ManifestProcessingRulesTypeDef = ...,
        PersonalizationThresholdSeconds: int = ...,
        SlateAdUrl: str = ...,
        Tags: Mapping[str, str] = ...,
        TranscodeProfileName: str = ...,
        VideoContentSourceUrl: str = ...
    ) -> PutPlaybackConfigurationResponseOutputTypeDef:
        """
        Creates a playback configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.put_playback_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#put_playback_configuration)
        """

    def start_channel(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Starts a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.start_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#start_channel)
        """

    def stop_channel(self, *, ChannelName: str) -> Dict[str, Any]:
        """
        Stops a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.stop_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#stop_channel)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The resource to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        The resource to untag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#untag_resource)
        """

    def update_channel(
        self,
        *,
        ChannelName: str,
        Outputs: Sequence[RequestOutputItemTypeDef],
        FillerSlate: SlateSourceTypeDef = ...
    ) -> UpdateChannelResponseOutputTypeDef:
        """
        Updates a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#update_channel)
        """

    def update_live_source(
        self,
        *,
        HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef],
        LiveSourceName: str,
        SourceLocationName: str
    ) -> UpdateLiveSourceResponseOutputTypeDef:
        """
        Updates a live source's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_live_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#update_live_source)
        """

    def update_program(
        self,
        *,
        ChannelName: str,
        ProgramName: str,
        ScheduleConfiguration: UpdateProgramScheduleConfigurationTypeDef,
        AdBreaks: Sequence[AdBreakTypeDef] = ...
    ) -> UpdateProgramResponseOutputTypeDef:
        """
        Updates a program within a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_program)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#update_program)
        """

    def update_source_location(
        self,
        *,
        HttpConfiguration: HttpConfigurationTypeDef,
        SourceLocationName: str,
        AccessConfiguration: AccessConfigurationTypeDef = ...,
        DefaultSegmentDeliveryConfiguration: DefaultSegmentDeliveryConfigurationTypeDef = ...,
        SegmentDeliveryConfigurations: Sequence[SegmentDeliveryConfigurationTypeDef] = ...
    ) -> UpdateSourceLocationResponseOutputTypeDef:
        """
        Updates a source location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_source_location)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#update_source_location)
        """

    def update_vod_source(
        self,
        *,
        HttpPackageConfigurations: Sequence[HttpPackageConfigurationTypeDef],
        SourceLocationName: str,
        VodSourceName: str
    ) -> UpdateVodSourceResponseOutputTypeDef:
        """
        Updates a VOD source's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.update_vod_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#update_vod_source)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_channel_schedule"]
    ) -> GetChannelSchedulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_alerts"]) -> ListAlertsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_live_sources"]
    ) -> ListLiveSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_playback_configurations"]
    ) -> ListPlaybackConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_prefetch_schedules"]
    ) -> ListPrefetchSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_locations"]
    ) -> ListSourceLocationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_vod_sources"]) -> ListVodSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor.html#MediaTailor.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mediatailor/client/#get_paginator)
        """

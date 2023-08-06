""" GraphQL representation of MCLIJob"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.models.run_config import RunConfig
from mcli.utils.utils_run_status import RunStatus


@dataclass
class Node(DeserializableModel):
    """Node linked to a run
    """

    rank: int
    name: str

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Node:
        return Node(rank=response.get('rank', 0), name=response.get('name', 'Unknown'))

    def to_dict(self):
        return {"rank": str(self.rank), "name": self.name}


@dataclass
class Resumption:
    """Data from a run resumption. The first instantiation of a Run will
         have a Resumption with index `0`
    """

    index: int
    cluster: str
    gpus: int
    cpus: int
    gpu_type: str
    node_count: int
    status: RunStatus
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Resumption:
        return Resumption(
            index=response['executionIndex'],
            cluster=response['clusterName'],
            gpus=response['gpus'],
            cpus=response['cpus'],
            gpu_type=response['gpuType'],
            node_count=response['nodes'],
            status=RunStatus.from_string(response['status']),
            started_at=convert_datetime(response['startTime']) if response['startTime'] else None,
            ended_at=convert_datetime(response['endTime']) if response['endTime'] else None,
        )

    def to_dict(self):
        return {
            "index": self.index,
            "cluster": self.cluster,
            "gpus": str(self.gpus),
            "cpus": str(self.cpus),
            "gpu_type": self.gpu_type,
            "node_count": str(self.node_count),
            "status": str(self.status),
            "started_at": str(self.started_at),
            "ended_at": str(self.ended_at),
        }


@dataclass
class RunLifecycle:
    """Status of a run at a moment in time
    """

    resumption_id: int
    status: RunStatus
    started_at: datetime
    ended_at: Optional[datetime] = None
    reason: Optional[str] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunLifecycle:
        return RunLifecycle(
            resumption_id=response['executionIndex'],
            status=RunStatus.from_string(response['status']),
            started_at=convert_datetime(response['startTime']),
            ended_at=convert_datetime(response['endTime']) if response['endTime'] else None,
            reason=response.get('reason'),
        )

    def to_dict(self):
        return {
            "resumption_id": str(self.resumption_id),
            "status": self.status,
            "started_at": str(self.started_at),
            "ended_at": str(self.ended_at),
            "reason": self.reason
        }


@dataclass
class Run(DeserializableModel):
    """A run that has been launched on the MosaicML platform

    Args:
        run_uid (`str`): Unique identifier for the run
        name (`str`): User-defined name of the run
        status (:class:`~mcli.utils.utils_run_status.RunStatus`): Status of the run at a moment in time
        created_at (`datetime`): Date and time when the run was created
        updated_at (`datetime`): Date and time when the run was last updated
        config (:class:`~mcli.models.run_config.RunConfig`): The
            :class:`run configuration <mcli.models.run_config.RunConfig>` that was used to launch to the run

        started_at (`Optional[datetime]`): Date and time when the run entered
            the `STARTED` :class:`~mcli.utils.utils_run_status.RunStatus`
        completed_at (`Optional[datetime]`): Date and time when the run entered
            the `COMPLETED` :class:`~mcli.utils.utils_run_status.RunStatus`
    """

    run_uid: str
    name: str
    status: RunStatus
    created_at: datetime
    updated_at: datetime
    created_by: str
    priority: str
    preemptible: bool
    retry_on_system_failure: bool
    cluster: str
    gpus: int
    gpu_type: str
    cpus: int
    node_count: int

    latest_resumption: Resumption
    max_retries: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    reason: Optional[str] = None
    nodes: List[Node] = field(default_factory=list)
    submitted_config: Optional[RunConfig] = None
    metadata: Optional[Dict[str, Any]] = None
    last_resumption_id: Optional[str] = None
    resumptions: List[Resumption] = field(default_factory=list)
    lifecycle: List[RunLifecycle] = field(default_factory=list)
    image: Optional[str] = None

    _required_properties: Tuple[str] = tuple([
        'id',
        'name',
        'status',
        'createdAt',
        'completedAt',
        'updatedAt',
        'reason',
        'createdByEmail',
        'priority',
        'preemptible',
        'retryOnSystemFailure',
        'resumptions',
    ])

    def _get_time_in_status(self, status: RunStatus) -> float:
        """Returns the time spent in a given status

        Args:
            status (:class:`~mcli.utils.utils_run_status.RunStatus`): The status to get the time for

        Returns:
            The time (seconds) spent in the given status
        """
        res = 0
        if self.lifecycle:
            for status_update in self.lifecycle:
                if status_update.status == status:
                    ended = status_update.ended_at
                    if not ended:
                        ended = datetime.now(tz=status_update.started_at.tzinfo)
                    res += (ended - status_update.started_at).total_seconds()
        return res

    @property
    def display_name(self) -> str:
        """The name of the run to display in the CLI

        Returns:
            The name of the run
        """
        if self.retry_on_system_failure:
            return f'{self.name} 🐕'

        return self.name

    @property
    def cumulative_pending_time(self) -> float:
        """Cumulative time spent in the PENDING state

        Returns:
            The cumulative time (seconds) spent in the PENDING state
        """
        return self._get_time_in_status(RunStatus.PENDING)

    @property
    def cumulative_running_time(self) -> float:
        """Cumulative time spent in the RUNNING state

        Returns:
            The cumulative time (seconds) spent in the RUNNING state
        """
        return self._get_time_in_status(RunStatus.RUNNING)

    @property
    def resumption_count(self) -> int:
        """Number of times the run has been resumed

        Returns:
            The number of times the run has been resumed
        """
        return len(self.resumptions)

    def clone(
        self,
        name: Optional[str] = None,
        image: Optional[str] = None,
        cluster: Optional[str] = None,
        instance: Optional[str] = None,
        nodes: Optional[int] = None,
        gpu_type: Optional[str] = None,
        gpus: Optional[int] = None,
        priority: Optional[str] = None,
        preemptible: Optional[bool] = None,
        max_retries: Optional[int] = None,
    ) -> Run:
        """
        Submits a new run with the same configuration as this run

        Args:
            name (str): Override the name of the run
            image (str): Override the image of the run
            cluster (str): Override the cluster of the run
            instance (str): Override the instance of the run
            nodes (int): Override the number of nodes of the run
            gpu_type (str): Override the GPU type of the run
            gpus (int): Override the number of GPUs of the run
            priority (str): Override the priority of the run
            preemptible (bool): Override whether the run can be stopped and re-queued by higher priority jobs
            max_retries (int): Override the max number of times the run can be retried

        Returns:
            New :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs import create_run

        submitted_config = self.submitted_config
        if submitted_config is None:
            refreshed_run = self.refresh()
            submitted_config = refreshed_run.submitted_config

        if not submitted_config:
            raise MAPIException(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f'Could not find the submitted run config for run {self.name}',
            )

        if name:
            submitted_config.name = name
        if image:
            submitted_config.image = image
        if cluster:
            submitted_config.compute['cluster'] = cluster
        if instance:
            submitted_config.compute['instance'] = instance
        if nodes is not None:
            submitted_config.compute['nodes'] = nodes
        if gpu_type:
            submitted_config.compute['gpu_type'] = gpu_type
        if gpus is not None:
            submitted_config.compute['gpus'] = gpus
        if priority:
            submitted_config.scheduling['priority'] = priority
        if preemptible is not None:
            submitted_config.scheduling['preemptible'] = preemptible
        if max_retries is not None:
            submitted_config.scheduling['max_retries'] = max_retries

        return create_run(submitted_config)

    def refresh(self) -> Run:
        """
        Refreshes the data on the run object

        Returns:
            Refreshed :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs import get_run

        return get_run(self)

    def stop(self) -> Run:
        """
        Stops the run

        Returns:
            Stopped :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs import stop_run

        return stop_run(self)

    def delete(self) -> Run:
        """
        Deletes the run

        Returns:
            Deleted :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs import delete_run
        return delete_run(self)

    def update(self,
               preemptible: Optional[bool] = None,
               priority: Optional[str] = None,
               max_retries: Optional[int] = None,
               retry_on_system_failure: Optional[bool] = None) -> Run:
        """
        Updates the run's data

        Args:
            preemptible (bool): Update whether the run can be stopped and re-queued by higher priority jobs;
                default is False
            priority (str): Update the priority of the run to `low`, `medium`, or `high`; default is `medium`
            max_retries (int): Update the max number of times the run can be retried; default is 0
            retry_on_system_failure (bool): Update whether the run should be retried on system failure
                (i.e. a node failure); default is False

        Returns:
            Updated :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs import update_run
        return update_run(
            self,
            preemptible=preemptible,
            priority=priority,
            max_retries=max_retries,
            retry_on_system_failure=retry_on_system_failure,
        )

    def update_metadata(self, metadata: Dict[str, Any]) -> Run:
        """
        Updates the run's metadata

        Args:
            metadata (`Dict[str, Any]`): The metadata to update the run with. This will be merged with
                the existing metadata. Keys not specified in this dictionary will not be modified.

        Returns:
            Updated :class:`~mcli.api.model.run.Run` object
        """
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs import update_run_metadata

        return update_run_metadata(self, metadata)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Run:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize Run object: {", ".join(missing)}',
            )

        started_at = None
        if response['startedAt'] is not None:
            started_at = convert_datetime(response['startedAt'])

        completed_at = None
        if response['completedAt'] is not None:
            completed_at = convert_datetime(response['completedAt'])

        resumptions = [Resumption.from_mapi_response(r) for r in response['resumptions']]
        latest_resumption = resumptions[-1]

        args = {
            'run_uid': response['id'],
            'name': response['name'],
            'created_at': convert_datetime(response['createdAt']),
            'started_at': started_at,
            'completed_at': completed_at,
            'updated_at': convert_datetime(response['updatedAt']),
            'status': RunStatus.from_string(response['status']),
            'reason': response['reason'],
            'created_by': response['createdByEmail'],
            'priority': response['priority'],
            'max_retries': response.get('maxRetries'),
            'preemptible': response['preemptible'],
            'resumptions': resumptions,
            'latest_resumption': latest_resumption,
            'retry_on_system_failure': response['retryOnSystemFailure'],
            'cluster': latest_resumption.cluster,
            'gpus': latest_resumption.gpus,
            'gpu_type': latest_resumption.gpu_type,
            'cpus': latest_resumption.cpus,
            'node_count': latest_resumption.node_count,
        }

        details = response.get('details', {})
        if details:
            submitted_run_input = details.get('originalRunInput')
            args['submitted_config'] = RunConfig.from_mapi_response(
                submitted_run_input) if submitted_run_input is not None else None

            args['metadata'] = details.get('metadata')
            args['last_resumption_id'] = details.get('lastExecutionId')
            args['lifecycle'] = [RunLifecycle.from_mapi_response(l) for l in details.get('lifecycle', [])]
            args['nodes'] = [Node.from_mapi_response(n) for n in details.get('nodes', [])]
            args['image'] = details.get('image')

        return cls(**args)

"""Implementation of mcli describe run"""
from __future__ import annotations

import logging
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generator, List, Optional, Tuple, TypeVar

from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from mcli.api.exceptions import cli_error_handler
from mcli.api.model.run import Node, Run, RunLifecycle, RunStatus
from mcli.cli.common.run_filters import get_runs_with_filters
from mcli.cli.m_get.display import (MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table,
                                    format_timestamp)
from mcli.models.run_config import ComputeConfig
from mcli.utils.utils_logging import FormatString, console, format_string, print_timedelta, seconds_to_str

logger = logging.getLogger(__name__)

DISPLAY_RUN_STATUSES = ['PENDING', 'RUNNING', 'COMPLETED']


class DisplayRunStatus(Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'


class DescribeRunDetailColumns(Enum):
    NAME = 'name'
    RUN_ID = 'run_uid'
    LAST_RESUMPTION_ID = 'last_resumption_id'
    CLUSTER = 'cluster'
    GPU_TYPE = 'gpu_type'
    GPU_NUM = 'gpu_num'
    CPUS = 'cpus'
    IMAGE = 'image'
    PRIORITY = 'priority'
    STATUS = 'status'
    PREEMPTIBLE = 'preemptible'
    REASON = 'reason'
    WATCHDOG = 'watchdog'


class DescribeRunOriginalInputColumns(Enum):
    SUBMITTED_CONFIG = 'submitted_config'


RUN_DETAIL_DISPLAY_NAMES = [
    'Run Name', 'Run ID', 'Last Resumption ID', 'Cluster', 'Image', 'Priority', 'Status', 'Preemptible', 'Reason',
    'Watchdog'
]
RUN_LIFECYCLE_DISPLAY_NAMES = ['Status', 'Reached At', 'Duration', 'Reason']
RUN_NODES_DISPLAY_NAMES = ['Node Name']
SUBMITTED_CONFIG = ['Run Config']


@dataclass
class DescribeRunDetailDisplayItem(MCLIDisplayItem):
    """Tuple that extracts detailed run data for display purposes"""
    name: str
    run_uid: str
    last_resumption_id: str
    cluster: str
    image: str
    last_resumption_id: str
    priority: str
    status: str
    preemptible: bool
    reason: str
    watchdog: str

    @classmethod
    def from_run(cls, run: Run) -> DescribeRunDetailDisplayItem:
        extracted: Dict[str, Any] = {
            DescribeRunDetailColumns.NAME.value: run.name,
            DescribeRunDetailColumns.RUN_ID.value: run.run_uid,
            DescribeRunDetailColumns.LAST_RESUMPTION_ID.value: run.last_resumption_id,
            DescribeRunDetailColumns.CLUSTER.value: run.cluster,
            DescribeRunDetailColumns.IMAGE.value: run.image,
            DescribeRunDetailColumns.PRIORITY.value: run.priority.lower().capitalize(),
            DescribeRunDetailColumns.STATUS.value: run.status.name.lower().capitalize(),
            DescribeRunDetailColumns.PREEMPTIBLE.value: run.preemptible,
            DescribeRunDetailColumns.REASON.value: run.reason,
            DescribeRunDetailColumns.WATCHDOG.value: run.retry_on_system_failure,
        }
        return DescribeRunDetailDisplayItem(**extracted)


@dataclass
class DescribeRunLifecycleDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for run lifecycle display purposes"""
    resumption: str
    status: str
    reached_at: str
    duration: str
    reason: str


@dataclass
class DescribeRunMetadataDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run metadata for display purposes"""

    key: str
    value: str


@dataclass
class MCLIDescribeRunNodeDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for run node display purposes"""
    rank: int
    name: str


# Displays
class MCLIDescribeRunDetailsDisplay(MCLIGetDisplay):
    """ Vertical table view of run details """

    def __init__(self, models: List[Run]):
        self.models = sorted(models, key=lambda x: x.created_at, reverse=True)
        self.include_reason_in_display = any(m.reason for m in models)

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, columns: List[str], data: List[Tuple[Any, ...]], names: List[str]) -> Optional[Table]:
        column_names = RUN_DETAIL_DISPLAY_NAMES
        if not self.include_reason_in_display:
            column_names = deepcopy(RUN_DETAIL_DISPLAY_NAMES)
            column_names.remove('Reason')
        return create_vertical_display_table(data=data, columns=column_names)

    def __iter__(self) -> Generator[DescribeRunDetailDisplayItem, None, None]:
        for model in self.models:
            item = DescribeRunDetailDisplayItem.from_run(model)
            yield item


def format_lifecycle_event(run_name, event: RunLifecycle) -> str:
    # TODO: move lifecycle event parsing to MAPI
    if event.status == RunStatus.COMPLETED:
        return 'Run completed successfully'
    elif event.status == RunStatus.FAILED:
        return f'Run failed with exit code {event.reason}.\n' + \
            f'See logs with `mcli logs {run_name} --resumption {event.resumption_id}`'
    elif event.status == RunStatus.STOPPED:
        if event.reason == 'Preempted':
            return 'Run was preempted'
        elif event.reason == 'Node Failure':
            return 'Run was stopped due to node failure'
    elif event.status == RunStatus.RUNNING:
        if event.resumption_id == 0:
            return 'Run started'
        else:
            return 'Run resumed'
    elif event.status == RunStatus.PENDING:
        if event.resumption_id == 0:
            return 'Run created'
        else:
            return 'Run placed back in the scheduling queue'
    # We don't want to inundate the user with all Run Statuses,
    # so let's hide other statuses for now
    return ''


def format_event_log(run_name: str, lifecycle: List[RunLifecycle]) -> Table:
    grid = Table(title='Event Log', expand=False, padding=(0, 2, 0, 2))
    grid.add_column(header='Time', justify='left')
    grid.add_column(header='Resumption', justify='left')
    grid.add_column(header='Event', justify='left')

    lifecycle = sorted(lifecycle, key=lambda x: (x.resumption_id, x.started_at))
    current_attempt = 0
    for event in lifecycle:
        if event.resumption_id != current_attempt:
            grid.add_section()
            current_attempt = event.resumption_id
        text = format_lifecycle_event(run_name=run_name, event=event)
        if len(text) > 0:
            grid.add_row(format_timestamp(event.started_at), str(event.resumption_id), text)
    return grid


def create_lifecycle_event_panel(event: RunLifecycle) -> Panel:
    duration = print_timedelta(event.ended_at - event.started_at) if event.ended_at else '-'
    panel_string = event.status.name.lower().capitalize()
    return Panel(f"At: {format_timestamp(event.started_at)}\nFor: {duration}", expand=False, title=panel_string)


class MCLIDescribeRunLifecycleDisplay():
    """ Panel view of run lifecycle """

    def __init__(self, model: List[RunLifecycle], created_at: datetime):
        self.created_at = created_at
        self.model = model
        self.include_reason_in_display = any(m.reason for m in model)

    def print(self):
        # Build the visual panels for Run Lifecycle
        current_resumption = 0
        all_columns = []
        curr_columns = []
        for event in self.model:
            if current_resumption != event.resumption_id:
                all_columns.append(Columns(curr_columns))
                curr_columns = [create_lifecycle_event_panel(event)]
                current_resumption = event.resumption_id
            else:
                curr_columns.append(create_lifecycle_event_panel(event))
        # add the last resumption's events
        all_columns.append(Columns(curr_columns))

        # Print the lifecycle events in descending order
        for idx in range(len(all_columns) - 1, -1, -1):
            panel_list = all_columns[idx]
            # Since the resumption index is monotonically increasing and starts at 0,
            # we can use the index of the array as the resumption_id
            resumption_string = "Initial Run:" if idx == 0 else f"Resumption {idx}:"
            print(resumption_string)
            rprint(panel_list)
            print()


class MCLIDescribeRunMetadataDisplay(MCLIGetDisplay):
    """ Vertical table view of run metadata """

    def __init__(self, metadata: Dict[str, Any]):
        self.columns = sorted(metadata.keys())
        self.metadata = metadata

    @property
    def index_label(self) -> str:
        return "key"

    def __iter__(self) -> Generator[DescribeRunMetadataDisplayItem, None, None]:
        for k in self.columns:
            item = DescribeRunMetadataDisplayItem(key=k, value=self.metadata[k])
            yield item


class MCLIDescribeRunNodeDisplay(MCLIGetDisplay):
    """ Horizontal table view of run node """

    def __init__(self, nodes: List[Node]):
        self.nodes = sorted(nodes, key=lambda x: x.rank)

    @property
    def custom_column_names(self) -> List[str]:
        return RUN_NODES_DISPLAY_NAMES

    def __iter__(self) -> Generator[MCLIDescribeRunNodeDisplayItem, None, None]:
        for n in self.nodes:
            yield MCLIDescribeRunNodeDisplayItem(n.rank, n.name)

    @property
    def index_label(self) -> str:
        return 'rank'


T = TypeVar('T')


def compute_or_deprecated(compute: ComputeConfig, key: str, deprecated: T) -> Optional[T]:
    from_compute = compute.get(key, None)
    if from_compute is not None:
        return from_compute
    return deprecated


@dataclass
class DescribeComputeRequests():
    """Describer for compute requests"""
    cluster: Optional[str] = None
    gpu_type: Optional[str] = None
    gpus: Optional[int] = None
    cpus: Optional[int] = None
    nodes: Optional[int] = None

    # TODO: add instance type

    @property
    def display_names(self) -> Dict[str, str]:
        # Return display name mapping for table
        return {
            'cluster': 'Cluster',
            'gpu_type': 'GPU Type',
            'gpus': 'GPUs',
            'cpus': 'CPUs',
            'nodes': 'Nodes',
        }

    @classmethod
    def from_run(cls, run: Run) -> DescribeComputeRequests:
        return DescribeComputeRequests(
            cluster=run.cluster,
            gpu_type=run.gpu_type,
            gpus=run.gpus,
            cpus=run.cpus,
            nodes=run.node_count,
        )

    def to_table(self) -> Table:
        data = {self.display_names.get(k, k.capitalize()): str(v) for k, v in asdict(self).items() if v is not None}
        columns = list(data.keys())
        values = [tuple(data.values())]
        return create_vertical_display_table(data=values, columns=columns)


@cli_error_handler("mcli describe run")
def describe_run(run_name: Optional[str], output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Run
    """
    del kwargs

    latest = not run_name
    name_filter = [run_name] if run_name else []

    runs = get_runs_with_filters(name_filter=name_filter, latest=latest, include_details=True)

    if len(runs) == 0:
        print(f'No runs found with name: {run_name}')
        return
    run = runs[0]

    # Run details section
    print(format_string('Run Details', FormatString.BOLD))
    metadata_display = MCLIDescribeRunDetailsDisplay([run])
    metadata_display.print(output)
    print()

    # Compute requests section
    print(format_string('Compute Requests', FormatString.BOLD))
    compute_display = DescribeComputeRequests.from_run(run)
    console.print(compute_display.to_table())
    print()

    if run.metadata:
        print(format_string('Run Metadata', FormatString.BOLD))
        metadata_display = MCLIDescribeRunMetadataDisplay(run.metadata)
        metadata_display.print(output)
        print()

    if run.nodes:
        print(format_string('Run Nodes', FormatString.BOLD))
        node_display = MCLIDescribeRunNodeDisplay(run.nodes)
        node_display.print(output)
        print()
    # Run lifecycle section
    print(format_string('Run Lifecycle', FormatString.BOLD))
    lifecycle_display = MCLIDescribeRunLifecycleDisplay(run.lifecycle, run.created_at)
    lifecycle_display.print()
    print()
    print(f'Number of Resumptions: {run.resumption_count}')
    print(f'Total time spent in Pending: {seconds_to_str(run.cumulative_pending_time)}')
    print(f'Total time spent in Running: {seconds_to_str(run.cumulative_running_time)}')
    print()

    # Run event log section
    console.print(format_event_log(run.name, run.lifecycle))
    print()

    # Run original input section
    print(format_string('Submitted YAML', FormatString.BOLD))
    print(run.submitted_config)

    # TODO: cleanup code to print directly to console after parsing
    # wrap command string within a literal `representer` - dump long str as block

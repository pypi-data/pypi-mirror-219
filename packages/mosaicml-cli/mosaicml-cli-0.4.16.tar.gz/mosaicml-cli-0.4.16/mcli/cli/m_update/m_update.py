""" mcli update Entrypoint """
import argparse
import logging
from http import HTTPStatus
from typing import Optional

from mcli.api.exceptions import MAPIException, cli_error_handler
from mcli.api.inference_deployments.api_update_inference_deployments import update_inference_deployment
from mcli.api.runs.api_update_run import update_run
from mcli.utils.utils_cli import configure_bool_arg
from mcli.utils.utils_logging import OK

logger = logging.getLogger(__name__)

# pylint: disable-next=invalid-name
UPDATE_RUN_EXAMPLE = """
Example:

# Update a run
> mcli update run example-run --priority high --max-retries 4 --no-preemptible
"""

UPDATE_DEPLOYMENT_EXAMPLE = """
Example:

# Update a deployment
> mcli update deployment mpt30b-deployment --image ../path/to/mpt30b.yaml --replicas 4
"""


def update_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


@cli_error_handler('mcli update run')
def _update_run(
    run_name: str,
    priority: Optional[str] = None,  # Default to None to not change value
    preemptible: Optional[bool] = None,  # Default to None to not change value
    max_retries: Optional[int] = None,  # Default to None to not change value
    **kwargs,
) -> int:
    del kwargs
    update_fields = any([preemptible is not None, priority is not None, max_retries is not None])
    if not update_fields:
        raise MAPIException(HTTPStatus.BAD_REQUEST, "Must specify preemptible, priority, or max_retries to update")
    update_string = ""
    if preemptible is not None:
        update_string += f"Set preemptible to {preemptible}.\n"
    if priority is not None:
        update_string += f"Set priority to {priority}.\n"
    if max_retries is not None:
        update_string += f"Set max_retries to {max_retries}.\n"
    update_run(run_name, preemptible=preemptible, priority=priority, max_retries=max_retries)

    logger.info(f'{OK} Updated {run_name}.\n{update_string}')
    return 0


@cli_error_handler('mcli update deployment')
def _update_deployment(
    deployment_name: str,
    image: Optional[str] = None,
    replicas: Optional[int] = None,
    **kwargs,
) -> int:
    del kwargs
    update_deployment_data = {}
    update_fields = any([image is not None, replicas is not None])
    if not update_fields:
        raise MAPIException(HTTPStatus.BAD_REQUEST, "Must specify image or replicas to update")
    update_string = ""
    if image is not None:
        update_deployment_data['image'] = image
        update_string += f"Set image to {image}.\n"
    if replicas is not None:
        update_deployment_data['replicas'] = replicas
        update_string += f"Set replica count to {replicas}.\n"
    update_inference_deployment(deployment_name, update_deployment_data)

    logger.info(f'{OK} Updated {deployment_name}.\n{update_string}')
    return 0


def add_update_argparser(subparser: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Add the parser for update
    """
    update_parser: argparse.ArgumentParser = subparser.add_parser(
        'update',
        help='Update a training run or inference deployment',
    )
    return _configure_argparser(parser=update_parser)


def deployment_argparser(subparser: argparse._SubParsersAction) -> None:
    deployment_parser = subparser.add_parser('deployment',
                                             description='Update the config for deployments created with mcli. '
                                             'This command can be used to update the image or number of replicas.',
                                             help='Update the image or replicas for an inference deployment',
                                             formatter_class=argparse.RawDescriptionHelpFormatter,
                                             epilog=UPDATE_DEPLOYMENT_EXAMPLE)
    deployment_parser.add_argument('deployment_name', type=str, help='The name of the deployment')
    deployment_parser.add_argument('--image', dest='image', help='Update deployment image file')
    deployment_parser.add_argument('--replicas', dest='replicas', type=int, help='Update deployment replica count')
    deployment_parser.set_defaults(func=_update_deployment)


def run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser = subparser.add_parser(
        'run',
        description='Update the scheduling config for runs created with mcli. '
        'This command can be used to update the priority, preemptible, or max_retries.',
        help='Update the scheduling config of a run',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=UPDATE_RUN_EXAMPLE,
    )
    run_parser.add_argument('run_name', type=str, help='The name of the run')
    run_parser.add_argument('--priority',
                            dest='priority',
                            help='Update run priority to `low`, `medium`, or `high` (default `medium`)')
    configure_bool_arg(parser=run_parser,
                       field='preemptible',
                       variable_name='preemptible',
                       true_description='Allows runs to be stopped and re-queued by higher priority jobs',
                       false_description='Disallows runs from being stopped and re-queued by higher priority jobs')
    run_parser.add_argument('--max-retries',
                            type=int,
                            dest='max_retries',
                            help='Update max number of times a run should be retried (default 0)')
    run_parser.set_defaults(func=_update_run)


def _configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='MCLI Updates', help='DESCRIPTION', metavar='OBJECT')
    parser.set_defaults(func=update_entrypoint, parser=parser)
    run_argparser(subparsers)
    deployment_argparser(subparsers)
    return parser

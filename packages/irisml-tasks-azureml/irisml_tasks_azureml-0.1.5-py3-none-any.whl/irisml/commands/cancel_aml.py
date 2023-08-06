import argparse
import logging
import os
from irisml.azureml import AMLJobManager
from irisml.core.commands.common import configure_logger

logger = logging.getLogger(__name__)


def main():
    configure_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('run_id')
    parser.add_argument('--subscription_id', default=os.getenv('IRISML_AML_SUBSCRIPTION_ID'))
    parser.add_argument('--workspace', default=os.getenv('IRISML_AML_WORKSPACE_NAME'))
    parser.add_argument('--experiment', default=os.getenv('IRISML_AML_EXPERIMENT_NAME', 'irisml'))

    args = parser.parse_args()

    job_manager = AMLJobManager(args.subscription_id, args.workspace, args.experiment, None, use_sp_on_remote=False, cache_url=None)
    job_manager.cancel(args.run_id)


if __name__ == '__main__':
    main()

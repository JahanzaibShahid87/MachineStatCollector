import mock_ssh_request
import config
from mock import patch
# load test settings.
config.load_settings(env="test")


def before_all(context):
    context.ssh_request_mock = init_ssh_mocker(context)


def after_all(context):
    context.ssh_request_mock_patcher.stop()


def init_ssh_mocker(context):
    context.ssh_request_mock_patcher = patch(
        'app.runner.start_collection',
        side_effect=mock_ssh_request.start_collection)
    context.ssh_request_mock = context.ssh_request_mock_patcher.start()
    return context.ssh_request_mock

from pushit import utils


def run_update(task):
    utils.run_update(task.data.update_cmd, task.data.branch)
    task.completed()

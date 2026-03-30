from tasks import null_task, user_disable_task, user_reset_task, user_copycat_task

tasks = {
    #"create": user_add_task.execute,
    "reset": user_reset_task.execute,
    "inactivate": user_disable_task.execute,
    "copycat": user_copycat_task.execute,
}


def run_task(task_name, inputs):

    task = tasks.get(task_name)
    if task:
        task(inputs)
    else:
        null_task.execute()
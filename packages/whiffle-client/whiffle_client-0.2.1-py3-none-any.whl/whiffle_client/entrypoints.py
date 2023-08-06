import click
import yaml

from whiffle_client import Client, CONFIG_FILE_PATH


@click.group()
def whiffle():
    pass


@whiffle.command()
@click.argument("number_of_tasks", default=10)
def tasks_list(number_of_tasks):
    """List tasks"""

    number_of_tasks = int(number_of_tasks)
    client = Client()
    tasks = client.get_tasks()
    click.echo(
        "{:33}{:11}{:16} {:16} progress".format(
            "task id", "status", "start time", "finish time"
        )
    )
    for task in tasks[-number_of_tasks:]:
        finished = task["finished"]
        if finished == None:
            task["finished"] = ""
        click.echo(
            "{task_id:33}{task_status:11}{received:17.16}{finished:17.16}{processed_steps}/{total_steps}".format(
                **task
            )
        )


@whiffle.command()
@click.argument("file_path")
def run(file_path) -> str:
    """Run task with given a set of parameters

    \b
    Parameters
    ----------
    file_path : str
        Path to (json|yaml) file containing parameters

    \b
    Returns
    -------
    str
        Name of the launched task
    """
    click.echo(f"run task with params: file_path={file_path}")
    client = Client()
    return client.process(file_path)


@whiffle.command()
@click.argument("key")
@click.argument("value")
def config_edit(key, value) -> str:
    """Edit configuration file

    \b
    Parameters
    ----------
    key : str
        Dot separated key value (e.g.: user.token)
    value : str
        Value to fill the configuration key with
    """
    config_key = key.split(".")
    with open(CONFIG_FILE_PATH) as file_object:
        config = yaml.safe_load(file_object)

    sub_config = config
    for sub_key in config_key[:-1]:
        if sub_key in sub_config:
            sub_config = sub_config[sub_key]
        else:
            raise KeyError(f"Key {sub_key} does not exist")
    try:
        if config_key[-1] not in sub_config:
            raise KeyError
        sub_config[config_key[-1]] = value
    except KeyError:
        raise KeyError(f"Key {config_key[-1]} does not exist")

    with open(CONFIG_FILE_PATH, "w") as file_object:
        yaml.safe_dump(config, file_object)

    click.echo(f"{key} changed to {value}")


@whiffle.command()
def config_list():
    """List configuration values"""

    with open(CONFIG_FILE_PATH) as file_object:
        config = yaml.safe_load(file_object)

    click.echo("Current configuration:\n-----\n")
    click.echo(yaml.safe_dump(config))
    click.echo("-----")


@whiffle.command()
@click.argument("task_id")
def tasks_download(task_id):
    """Download task

    \b
    Parameters
    ----------
    task_id : str
    """
    click.echo(f"downloading task output {task_id}")
    client = Client()
    client.download(task_id)


@whiffle.command()
@click.argument("task_id")
def tasks_attach(task_id):
    """Attach to task

    \b
    Parameters
    ----------
    task_id : str
    """
    click.echo(f"attaching to task {task_id}")
    client = Client()
    client.communicate(task_id)

import click

from magniv.build import build as m_build
from magniv.export import export as m_export
from magniv.run import run as m_run


@click.group()
def cli():
    pass


@cli.command()
def build():
    return m_build()


@cli.command()
@click.option("--gcp", is_flag=True)  # GCP creeates the dockerfiles and cloubuild.yaml
@click.option("--gcp-project-id")
@click.option("--gcp-dag-folder")
@click.option("--callback-hook")
@click.option("--env-file-path")
def export(gcp, gcp_project_id, gcp_dag_folder, callback_hook, env_file_path):
    return m_export(
        gcp=gcp,
        gcp_project_id=gcp_project_id,
        gcp_dag_folder=gcp_dag_folder,
        callback_hook=callback_hook,
        env_file_path=env_file_path,
    )


@cli.command()
@click.argument("filepath")
@click.argument("function_name")
def run(filepath, function_name):
    return m_run(filepath, function_name)

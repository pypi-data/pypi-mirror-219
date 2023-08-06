import mlflow
import os
import click

from mlflow_tritonserver import triton_flavor


@click.group()
def cli():
    """CLI group for the script."""
    pass


@cli.command()
@click.option(
    "--model_name",
    help="Name of the model to be published.",
)
@click.option(
    "--model_directory",
    type=click.Path(exists=True, readable=True),
    required=True,
    help="Filepath of the model to be published.",
)
@click.option(
    "--flavor",
    type=click.Choice(["triton"], case_sensitive=True),
    required=True,
    help="Flavor of the model to be published.",
)
def publish(model_name, model_directory, flavor):
    """
    Publish a model to MLflow.

    Args:
        model_name (str): Name of the model to be published.
        model_directory (str): Filepath of the model to be published.
        flavor (str): Flavor of the model to be published.

    Raises:
        Exception: If the flavor is not supported.
    """
    # Get MLflow tracking URI from environment variable
    mlflow_tracking_uri = os.environ["MLFLOW_TRACKING_URI"]
    artifact_path = "triton"

    # Set the tracking URI for MLflow
    mlflow.set_tracking_uri(uri=mlflow_tracking_uri)

    # Start a new MLflow run
    with mlflow.start_run() as run:
        # If the flavor is Triton, log the model
        if flavor == "triton":
            triton_flavor.log_model(
                triton_model_path=model_directory,
                artifact_path=artifact_path,
                registered_model_name=model_name,
            )
        else:
            # If the flavor is not supported, raise an exception
            # Enhancement: for model in other flavor (framework) that Triton
            # supports, try to format it in Triton style and provide
            # config.pbtxt file. Should this be done in the plugin?
            raise Exception("Other flavor is not supported")

        # Print the artifact URI
        print(mlflow.get_artifact_uri())


if __name__ == "__main__":
    cli()

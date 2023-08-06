import typer
import inquirer
import os

from peelml.server import app as flask_app
from peelml.model.sagemaker import SageMaker

app = typer.Typer()


@app.command()
def create():
    print("TODO: create the project scaffolding")


@app.command()
def start():
    cwd = os.getcwd()
    print(f"Current working directory is {cwd}")

    # enter project name and author name
    project: str = typer.prompt('Enter project name')
    author: str = typer.prompt('Enter author name')

    # enter document path
    doc_path = typer.prompt(
        'Enter document directory path',
        default=os.path.join(cwd, "docs"))
    os.environ['DOC_PATH'] = doc_path

    # select vector database and enter vector database path
    vectordb = inquirer.list_input(
        "Select vector database", choices=["chroma"]
    )
    vectordb_path = typer.prompt(
        'Enter vector database directory path',
        default=os.path.join(cwd, "db"))
    os.environ['VECTORDB_PATH'] = vectordb_path

    # enter sql database path
    duckdb_path = typer.prompt(
        'Enter sql duck database directory path',
        default=os.path.join(cwd, "db/duck"))
    os.environ["DUCKDB_PATH"] = duckdb_path

    # select model
    model = inquirer.list_input(
        "Select model", choices=["sagemaker", "openai", "llama_cpp"]
    )
    if model == "openai":
        openai_api_key = typer.prompt('Enter OpenAI API key')
        os.environ['OPENAI_API_KEY'] = openai_api_key
    elif model == 'llama_cpp':
        llama_cpp_path = typer.prompt('Enter llama_cpp model path')
        os.environ['LLAMA_CPP_PATH'] = llama_cpp_path
        print(f"path is {os.environ['LLAMA_CPP_PATH']}")
    elif model == 'sagemaker':
        endpoint_name = typer.prompt('Enter sagemaker endpoint name', default="")
        print(f"endpoint name is {endpoint_name}")
        if endpoint_name == "":
            print(f"creating sagemaker endpoint for {model} model")
            sagemaker = SageMaker()
            endpoint_name = sagemaker.deploy()
        os.environ['SAGEMAKER_ENDPOINT_NAME'] = endpoint_name
    else:
        raise Exception("Unknown model: {}".format(model))

    print(f"Creating project {project} by author {author}")
    print(f"Setting up local vector database at {vectordb_path}")
    print(f"Setting up local duckdb sql database at {duckdb_path}")
    print(f"Setting up {model} model")
    print("Starting server...")
    flask_app.config['vectordb'] = vectordb
    flask_app.config['model'] = model
    flask_app.run(port=5000)


@app.command()
def build():
    print("TODO: build the project")


@app.command()
def deploy():
    print("TODO: deploy the project")


def cli():
    app()


if __name__ == "__main__":
    cli()

import os
import random

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)
from flask_cors import CORS

from peelml.duck.preference_table import PreferenceTable
from peelml.llm.model_factory import ModelFactory
from peelml.vectordb.vectordb_factory import VectorDbFactory

model = None
preference_table = None
vector_db = None

app = Flask(__name__)
CORS(app)


@app.route("/")
def base():
    """
    Path for our main Svelte page.
    """
    return send_from_directory("client/build", "index.html")


@app.route("/<path:path>")
def home(path):
    """
    Path for all the static files (compiled JS/CSS, etc.).
    """
    return send_from_directory("client/build", path)


@app.route("/rand")
def ran():
    return str(random.randint(0, 100))


@app.route("/objects/get", methods=["GET"])
def get_files():
    """
    This function retrieves a list of files in the server's document directory
    and returns a JSON object containing information about each file,
    including its name, size, and type.

    HTTP REQUEST:
        GET /objects/get

    HTTP RESPONSE:
        {
            "files": [
                {
                    "name": "example.pdf",
                    "size": 123456,
                    "type": "pdf"
                },
                {
                    "name": "example.jpg",
                    "size": 654321,
                    "type": "jpg"
                },
                ...
            ]
        }

    Returns:
        Flask.Response: A Flask response object containing a JSON object with
        information about each file in the server's document directory.
    """
    print(f"[/objects/get]: getting files...")
    # create folder if it doesn't exist
    dir_path = os.environ["DOC_PATH"]
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    files = os.listdir(dir_path)

    # Create a list of dictionaries, each containing the file's name, size and type
    file_data = []
    for file in files:
        size = os.path.getsize(
            os.path.join(dir_path, file)
        )  # get size of file in bytes
        _, ext = os.path.splitext(file)  # split the file name into name and extension
        file_data.append(
            {
                "name": file,
                "size": size,
                "type": ext[1:],  # remove the period from the extension
            }
        )

    return jsonify({"files": file_data})


@app.route("/objects/upload", methods=["POST"])
def upload():
    """
    This function handles the file upload functionality of the server. It creates a folder if it doesn't exist, checks if
    any file is sent, gets all the files from the request, saves or processes the file, and returns a JSON object
    containing the status of the upload.

    HTTP REQUEST:
        POST /objects/upload

    BODY:
        form-data: {
            "file": <file>
            }

    HTTP RESPONSE:
        {
            "status": "ok",
            "filenames": ["example.pdf", "example.jpg"],
            "files": ["example.pdf", "example.jpg", ...]
        }

    Returns:
        Dict: A dictionary containing the status of the http response, the filenames of the uploaded files, and a list of
        all files in the server's document directory.
    """
    try:
        # create folder if it doesn't exist
        if not os.path.exists(os.getenv("DOC_PATH")):
            os.makedirs(os.getenv("DOC_PATH"))

        print(f"[/objects/upload]: upload files {request.files}")
        # Check if any file is sent
        if "file" not in request.files:
            return "No file part"

        # Get all the files from the request
        files = request.files.getlist("file")

        filenames = []
        # Iterate over each file
        for file in files:
            # Check if file is selected
            if file.filename == "":
                return "No selected file"

            if file:
                print(f"[/objects/upload]: saving file...")
                # Save or process the file
                file.save(os.path.join(os.environ["DOC_PATH"], file.filename))
                filenames.append(file.filename)

        # List all files in the DOC_PATH directory
        file_list = os.listdir(os.getenv("DOC_PATH"))

        return jsonify({"status": "ok", "filenames": filenames, "files": file_list})

    except Exception as ex:
        return jsonify(
            {
                "log": "Failed to receive JSON data: {}".format(ex),
                "status": "500",
            }
        )

# TODO: change to POST API
@app.route("/objects/index")
def index():
    """This function handles the index of all files saved in docs/ directory.
    It resets the LangChain for inference if it has been initialized.

    HTTP REQUEST:
        GET /objects/index

    HTTP RESPONSE:
        HTTP response if successful:
            {'log': 'Indexing complete',
            'status': '200'}
        HTTP response if unsuccessful:
            {'log': 'Indexing failed: {}'.format(ex),
            'status': '500'}

    Returns:
        Dict: A dictionary containing the status of the http response.
    """
    try:
        print(f"[/objects/index]: indexing files...")
        vector_db.index()
        return {'log': 'Indexing complete',
                    'status': '200'}
    except Exception as ex:
        return {'log': 'Indexing failed: {}'.format(ex),
                'status': '500'}

# TODO: change to GET API
@app.route("/objects/retrieve/<message>", methods=["POST"])
def inference(message):
    """
    This function takes in a message and returns the output of the LangChain's inference.
    It assumes that the LangChain has already been initialized.

    HTTP REQUEST:
        POST /objects/retrieve/<message>

    HTTP RESPONSE:
        HTTP response if successful:
            {'log': 'Inference complete',
            'status': '200',
            'question': <request message>,
            'answer': <response answer>}
        HTTP response if unsuccessful:
            {'log': 'Inference failed: {}'.format(ex),
            'status': '500'}

    Args:
        message (str): The message to be processed by the LangChain.

    Returns:
        str: The output of the LangChain's inference.
    """
    try:
        print(f"[/objects/retrieve]: model inference...")
        output = model.run(message)
        return {'log': 'Inference complete',
                'status': '200',
                'question': message,
                'answer': output}
    except Exception as ex:
        return {'log': f'Inference failed: {ex}',
                'status': '500'}


@app.route("/embedding/get", methods=["GET"])
def get_embeddings():
    """
    This function retrieves the embeddings from the specified vector database and returns them as a JSON response.

    HTTP REQUEST:
        GET /embedding/get

    HTTP RESPONSE:
        HTTP response if successful:
            {'log': 'Embeddings retrieved',
            'status': '200',
            'embeddings': <list of embeddings>}
        HTTP response if unsuccessful:
            {'log': 'Failed to get embedding: {}'.format(ex),
            'status': '500'}

    Returns:
        A JSON response containing the embeddings retrieved from the specified vector database.
    """
    try:
        print(f"[/embedding/get]: get embedding...")
        response_dict = vector_db.get_embedding()
        return jsonify(response_dict)
    except Exception as ex:
        return jsonify(
            {
                "log": "Failed to get embedding: {}".format(ex),
                "status": "500",
            }
        )

@app.route("/preference_table/insert", methods=["POST"])
def insert_preference_table():
    """
    This function inserts a question-answer pair and its corresponding vote into the preference table.
    It assumes that the preference table has already been initialized.

    HTTP REQUEST:
        POST /preference_table/insert

    HTTP POST Request Body:
        {
            "question": <question string>,
            "answer": <answer string>,
            "vote": <vote integer>
        }

    HTTP RESPONSE:
        HTTP response if successful:
            {
                "log": "insert into preference table successfully",
                "index": <index of the inserted question-answer pair>,
                "status": "200"
            }
        HTTP response if unsuccessful:
            {
                "log": "Failed to insert preference table: {}".format(ex),
                "status": "500"
            }

    Returns:
        str: The HTTP response message indicating whether the insert was successful or not.
    """
    try:
        request_body = request.get_json()
        print(f"[/preference_table/insert]: insert into preference table {request_body}...")
        id = preference_table.insert(
            question=request_body["question"],
            answer=request_body["answer"],
            vote=request_body["vote"],
        )
        return jsonify(
            {
                "log": "presist into preference table successfully",
                "index": id,
                "status": "200",
            }
        )
    except Exception as ex:
        return jsonify(
            {
                "log": "Failed to insert preference table: {}".format(ex),
                "status": "500",
            }
        )

@app.route("/preference_table/get", methods=["GET"])
def get_preference_table():
    """
    Retrieves the preference table from the global variable `preference_table`
    and returns it as a JSON object.

    HTTP REQUEST:
        GET /preference_table/get

    HTTP RESPONSE:
        HTTP response if successful:
            {'log': 'get preference table successfully',
             "preference_table": <preference dict>,
             "question_table": <question dict>,
             "answer_table": <answer dict>,
             "status": '200'}
        HTTP response if unsuccessful:
            {"log": "Failed to get preference table: {}".format(ex),
             "status": "500"}

    Returns:
        A JSON object containing the preference table, question table, answer table, and status code.
    """
    try:
        print(f"[/preference_table/get]: get preference table...")
        preference_result = preference_table.get()
        return jsonify(
            {
                "log": "get preference table successfully",
                "preference_result": preference_result,
                "status": "200",
            }
        )
    except Exception as ex:
        return jsonify(
            {
                "log": "Failed to get preference table: {}".format(ex),
                "status": "500",
            }
        )

@app.route("/preference_table/update", methods=["POST"])
def update_preference_table():
    try:
        request_body = request.get_json()
        print(f"[/preference_table/update]: update preference table {request_body}...")
        preference_table.update(
            id=request_body["id"],
            vote=request_body["vote"],
        )
        return jsonify(
            {
                "log": "update preference table successfully",
                "status": "200",
            }
        )
    except Exception as ex:
        return jsonify(
            {
                "log": "Failed to update preference table: {}".format(ex),
                "status": "500",
            }
        )


@app.before_first_request
def initialize():
    """
    This function initializes the global variables
    `vector_db`, `preference_table` and `model` before the first request is made.
    """
    global vector_db
    global preference_table
    global model

    vector_db = VectorDbFactory.create_vector_db(
        app.config["model"], app.config["vectordb"]
        )
    preference_table = PreferenceTable()
    model = ModelFactory.create_model(app.config["model"], vector_db)
    print("flask server initialize successfully")


if __name__ == "__main__":
    ######################################################
    # upate doc path, vector db path, and openai api key #
    ######################################################
    cwd = os.getcwd()
    print(f"[server]: the current path is {cwd}")
    os.environ["DOC_PATH"] = os.path.join(cwd, "peelml/docs")
    os.environ["VECTORDB_PATH"] = os.path.join(cwd, "peelml/db")
    os.environ["DUCKDB_PATH"] = os.path.join(cwd, "peelml/db/duck")
    os.environ["OPENAI_API_KEY"] = ""
    app.config["vectordb"] = "chroma"
    app.config["model"] = "openai"
    if os.environ["OPENAI_API_KEY"] == "":
        raise ValueError("OPENAI_API_KEY is not set")
    app.run(port=5000, debug=True)

# peelml

peelml away the pain of ml deployment
# Development
## 1. Setup and Build

### 1.1 build backend
```
git clone https://github.com/CambioML/peelml.git
conda create -n peelml python=3.10
conda activate peelml
cd peelml
pip install poetry
pip install git+https://github.com/UKPLab/sentence-transformers.git@179b659621c680371394d507683b25ba7faa0dd8
poetry install --no-root # no root to not install peelml as a package
```

### 1.2 build frontend
1. install [nodejs](https://nodejs.org/en)
2. npm install `npm install vite`
3. cd into client folder and `npm run build`

## 2. Run
### 2.1 Option 1: run the server and client directly without cli
Before you start running the command below, go to server.py and upate
```
os.environ["OPENAI_API_KEY"] = ""
```

After that, run the following command
```
python -m peelml.server
```

### 2.2 Option 2: run the cli command
This is a interactive cli to ask you to input required environment parameters.
It will then start the server and client for you.
```
python -m peelml.cli start
```

## 3. Install
install peelml into site-packages like a pip install
```
poetry install
peelml start
```


P.S: If you build and pip install for local test, your changes will not reflect in peelml site-packages. Therefore, you have to `pip3 uninstall peelml`, built it again, and the install.

# Use
```
pip install git+https://github.com/UKPLab/sentence-transformers.git@179b659621c680371394d507683b25ba7faa0dd8
pip install peelml
```
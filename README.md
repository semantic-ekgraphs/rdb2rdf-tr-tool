# RDB2RDF Tool
Relational Database to RDF Views Tool



## Setting and Running the Back-end

### Setting the Back-end
First of all, It is recommended to create a virtual environment.

```
python -m venv .venv
```


After setting up the virtual environment, you must install the packages using the "requirements.txt" file by running the following command:

```
python install -r requirements.txt
```


### Running the Back-end

To run the back-end application, enter the "/src" folder

```
cd /src
```

then, execute the "run-fastapi-dev.bat" file for Windows.


```
run-fastapi-dev.bat
```

To view the API documentation for the RDB2RDF tool, open the following address in any web browser:

```
http://127.0.0.1:8000/docs
```
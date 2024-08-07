import datetime
import subprocess
import json

def do_freeze():
    #send a pip freeze command to shell and hold returned value
    req = subprocess.check_output(["pip", "freeze"])
    with open("requirements.txt", "w") as _app:
        req = req.decode("utf-8") #convert returned byte value to string
        _app.write(req)
    return True


def do_add_log(type, data):
    # create a datetime string
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    data['timestamp'] = date

    logs = read_logs()

    logs[type].append(data)

    write_logs(logs)

def read_logs():
    try:
        with open(".fs", "r", encoding='utf-8') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise Exception('.fs file is missing or damaged.')

def write_logs(content):
    try:
        with open(".fs", "w", encoding='utf-8') as file:
            # add the log to the end of the file
            json.dump(content, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        raise Exception('.fs file is missing or damaged.')

def write_log_file(project, name, email):
    try:
        content = {
        "project":project,
        "author":name,
        "email":email,
        "config":{
            "python":"3.10",
            "pip":"24.10",
            "fs":"0.6.1"
            },
        "packages":[],
        "modules":[]
        }

        with open(".fs", "w", encoding='utf-8') as file:
            # add the log to the end of the file
            json.dump(content, file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise Exception('.fs file is missing or damaged.')
import subprocess

def upload_file_url(url, expires=None, secret=None):
    if expires == None:
        if secret == None:
            command = f"curl -F'url={url}' https://0x0.st"
        else:
            command = f"curl -F'url={url}' -Fsecret=https://0x0.st"
    else:
        if secret == None:
            command = f"curl -F'url={url}' -Fexpires={expires} https://0x0.st"
        else:
            command = f"curl -F'url={url}' -Fexpires={expires} -Fsecret=https://0x0.st"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Ошибка при загрузке файла:\n {e}"

def delete_file(token, url):
    command = f"curl -Ftoken={token} -Fdelete={url}"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Ошибка при удалении файла:\n {e}"

def change_expires(url, expires, token):
    command = f"curl -Ftoken={token} -Fexpires={expires} {url}"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Ошибка при изменении хранения файла:\n {e}"
    
def upload_file_path(path, expires=None, secret=None):
    if expires == None:
        if secret == None:
            command = f"curl -F'file={path}' https://0x0.st"
        else:
            command = f"curl -F'file={path}' -Fsecret=https://0x0.st"
    else:
        if secret == None:
            command = f"curl -F'file={path}' -Fexpires={expires} https://0x0.st"
        else:
            command = f"curl -F'file={path}' -Fexpires={expires} -Fsecret=https://0x0.st"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Ошибка при загрузке файла:\n {e}"

import uvicorn
import yaml
from pathlib import Path
from utils.path_dict import root_dir


if __name__ == "__main__":

    config_path = root_dir / "config.yaml"
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    mode ="https"
    if mode == "http":
        host = config[mode]["host"]
        port = config[mode]["port"]
        uvicorn.run("api_server:app", host=host, port=port , reload=True)
    elif mode =="https":
        ssl_keyfile = root_dir / "cert" / "server.key"
        ssl_certfile = root_dir / "cert" / "server.crt"
        host = config[mode]["host"]
        port = config[mode]["port"]
        uvicorn.run("api_server:app", host=host, port=port ,ssl_keyfile=ssl_keyfile,ssl_certfile=ssl_certfile, reload=True)

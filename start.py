import os
import sys
import json
from shutil import copy
import subprocess

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

root = "./"
config_path = root + "ckserver.json"
ckjson = ""

with open(root + "ckserver_template.json", mode='r') as ckfile:
    ckjson = json.loads(ckfile.read())
    ckfile.close()

try:
    user_uid = os.environ["CK_BYPASSUID"]
    admin_uid = os.environ["CK_ADMINUID"]
    private_key = os.environ["CK_PRIVATEKEY"]
    port = os.environ["PORT"]

    # Build config according to environment variables
    with open(config_path, mode='w') as config :
        ckjson["BypassUID"].append(user_uid)
        ckjson["AdminUID"] = admin_uid
        ckjson["PrivateKey"] = private_key
        ckjson["BindAddr"].append(f":{port}")

        ck_json_string =  json.dumps(ckjson, indent=4)
        print(ck_json_string, file=config)
        config.close()
    eprint("Config generated from environment variables..")
except Exception as e:
    eprint(e)
    eprint("Variables not found. Trying to make a configuration...")
    port = os.environ["PORT"]

    # Get keys for ck-server
    keys = subprocess.check_output(["ck-server", "-key"]).decode().split("\n")
    public_key = keys[0][-44:]
    private_key = keys[1][-44:]

    # Generate UIDs
    admin_uid = subprocess.check_output(["ck-server", "-uid"]).decode().strip()
    admin_uid = admin_uid[-24:]

    user_uid = subprocess.check_output(["ck-server", "-uid"]).decode().strip()
    user_uid = user_uid[-24:]

    eprint("Admin ", admin_uid)
    eprint("User ", user_uid)
    eprint("Public ", public_key)
    #print("Private key ", private_key)

    # Build json file
    ckjson["BypassUID"].append(user_uid)
    ckjson["AdminUID"] = admin_uid
    ckjson["PrivateKey"] = private_key
    ckjson["BindAddr"].append(f":{port}")

    with open(config_path, mode='w') as config :
        ck_json_string =  json.dumps(ckjson, indent=4)
        print(ck_json_string, file=config)

# Start all processes etc.

squid = subprocess.Popen(["squid"])
ck_server = subprocess.Popen(["ck-server","-c","/home/ckserver.json"])
squid.wait()
ck_server.wait()
eprint("Script exited.")
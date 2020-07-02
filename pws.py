#!/usr/bin/python
import argparse
import getpass
import gnupg
import json
import os
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--field", choices=["password", "username"], default="password",
                    help="Select which key field to obtain with --get-profile. Defaults to 'password'.\n")
parser.add_argument("--get-profile", help="Retrieve account information from a profile and store in clipboard.\n")
parser.add_argument("--new-master", action="store_true", help="Create a new, encrypted master file.")
parser.add_argument("--new-profile", help="Add a new account profile to the encrypted master file.")
parser.add_argument("--remove-profile", help="Remove a stored profile from the encrypted master file.")
args = parser.parse_args()

def create_new_encrypted_master(gpg, key, path):
    if path.is_file():
        print("The master.asc file already exists! This will delete all your data and create a new, blank file!")
        confirm = input("Are you absolutely sure you want to overwrite it? Type 'yes' to proceed.\n")
        if confirm != "yes":
            sys.exit("Quitting.")
    data_dir = path.parent
    data_dir.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    path.write_text("{}")
    stream = open(str(path), "rb")
    encrypt = gpg.encrypt_file(stream, key, output=str(path))
    stream.close()
    if not encrypt.ok:
        sys.exit("Encryption failed! Please check that you inputted a valid email in the config.")

def create_new_profile(gpg, key, profile, path):
    decrypt = decrypt_master(gpg, key, path)
    master = json.loads(str(decrypt))
    if profile in master:
        print("The "+profile+" profile already exists in the master.asc file!")
        confirm = input("Are you absolutely sure you want to change its values? Type 'yes' to proceed.\n")
        if confirm != "yes":
            sys.exit("Quitting.")
    username = input("Input username for this profile.\n")
    password = getpass.getpass(prompt="Input the password for this profile.\n")
    master[profile] = {"username" : username, "password": password}
    encrypt = gpg.encrypt(json.dumps(master).encode("utf-8"), key, output=str(path))
    if not encrypt.ok:
        sys.exit("Encryption failed! Please check that you inputted a valid email in the config.")

def decrypt_master(gpg, key, path):
    stream = open(str(path), "rb")
    decrypt = gpg.decrypt_file(stream)
    if not decrypt.ok:
        sys.exit("Decryption failed! Please check that you inputted a valid email in the config.")
    return decrypt

def get_clipboard_program(path):
    clipboard = read_config_var(path, "clipboard-copy=")
    if clipboard == "":
        sys.exit("Clipboard program not found in config file! Must be a line formatted as 'clipboard-copy=prog --args'!")
    return clipboard

def get_gpg_key(path):
    key = read_config_var(path, "gpg=")
    if key == "":
        sys.exit("Valid gpg email address not found in config file! Must a line formatted as 'gpg=user@example.com'!")
    return key

def get_profile(gpg, key, profile, field, path, clipboard):
    decrypt = decrypt_master(gpg, key, path)
    master = json.loads(str(decrypt))
    if not profile in master:
        sys.exit("The '"+profile+"' profile doesn't exist!")
    value = ""
    if field == "password":
        value = master[profile]["password"]
    elif field == "username":
        value = master[profile]["username"]
    os.system(clipboard+" "+value)

def quit_message():
    config_dir = config_path.parent
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path.touch(exist_ok=True)

def read_config_var(path, var):
    with open(str(path), "r") as f:
        for line in f:
            if line.find(var) != -1:
                value = line.split(var)[1].rstrip()
                return value
    return ""

def remove_profile(gpg, key, profile, path):
    decrypt = decrypt_master(gpg, key, path)
    master = json.loads(str(decrypt))
    if profile in master:
        confirm = input("This will delete the '"+profile+"' profile from the encrypted master. Type 'yes' to proceed.\n")
        if confirm == "yes":
            del master[profile]
            encrypt = gpg.encrypt(json.dumps(master).encode("utf-8"), key, output=str(path))
            if not encrypt.ok:
                sys.exit("Encryption failed! Please check that you inputted a valid email in the config.")
        else:
            sys.exit("Quitting.")
    else:
        sys.exit("The '"+profile+"' profile was not found.")

def main(args):
    config_path = Path.home() / ".config" / "pws" / "config"
    data_path = Path.home() / ".local" / "share" / "pws" / "master.asc"

    if not config_path.is_file():
        sys.exit("Config file in ~/.config/pws/config does not yet exist. Please create it with the right variables.")

    key = get_gpg_key(config_path)
    clipboard = get_clipboard_program(config_path)
    gpg = gnupg.GPG()
    gpg.import_keys(key)

    if not data_path.is_file():
        confirm = input("Encrypted master file does not exist. Would you like to create it now? Type 'yes' to proceed.\n")
        if confirm == 'yes':
            create_new_encrypted_master(gpg, key, data_path)
            sys.exit()

    if args.get_profile:
        get_profile(gpg, key, args.get_profile, args.field, data_path, clipboard)
    elif args.new_master:
        create_new_encrypted_master(gpg, key, data_path)
    elif args.new_profile:
        create_new_profile(gpg, key, args.new_profile, data_path)
    elif args.remove_profile:
        remove_profile(gpg, key, args.remove_profile, data_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main(args)
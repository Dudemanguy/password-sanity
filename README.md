# password-sanity
**p**ass**w**ord-**s**anity (pws) is a very simple commandline tool for managing passwords. Writing this was primarily motivated by the pure insanity that it would be to have good password practices without the help of software (hence the name) and the desire to avoid cloud crap or some complex GUI. The goal is to have safe, secure password storage for multiple accounts that is also easily retrievable with one command.

## Installation
You will need `python-gnupg` installed.

```
$ git clone https://github.com/Dudemanguy/password-sanity.git
$ cd password-sanity
# python setup.py install
```

## Setup
password-sanity relies on gpg for encryption and decryption. You will need to have generated your own gpg key pair with the private key in your keyring. There is no need to export the public key since the private key is what does the decryption it should only ever exist on one machine. Just run `gpg --full-gen-key` and follow the instructions. After you have a usable gpg key, you need to specify two variables in the `~/.config/pws/config` file (simply create it if it doesn't exist) like so:
```
gpg=user@domain.com
clipboard-copy=prog --args
```

The `gpg` field is simply the email field you specified for the gpg key created earlier. Since there is no reason to send this particular public key anywhere, it does not need to be a real email. The `clipboard-copy` field is the shell command used to copy a string to your system's clipboard. Since there is no sane way of having a cross-platform clipboard, this is the simplest way to handle it. On linux, you probably want `xclip` or `wl-copy` here.

## Usage
One the first usage, pws will prompt you to create the encrypted master file. The location is `~/.local/share/pws/master.asc`.

You can add a new account profile to the master file:  
`pws --new-profile profile-name`  

The above will autogenerate a random password of length 16 (guaranteed to have at least one digit, lowercase, uppercase, and special character). If you wish to change the password length, you can just pass the `--password-length` argument:  
`pws --new-profile profile-name --password-length 24`  
If you want to manually type a password in, use `--password-length 0`.

Modify an existing profile:  
`pws --modify-profile profile-name`  
You can pass `--password-length` and `--field` with `--modify-profile` as well.

Removing profiles:  
`pws --remove-profile profile-name`

Retrieving a profile's password and storing it in the system's clipboard:  
`pws --get-profile profile-name`

Retrieving a profile's username and storing it in the system's clipboard:  
`pws --get-profile profile-name --field username`

Creating a brand new encrypted master:  
`pws --new-master`


## Notes
The structure of the decrypted master.asc file is simply JSON. You can create your own master.asc with whatever method you like as long as it is in valid JSON and you encrypt it with the same gpg key.

## TODO
* Write some manpages

## License
GPLv3

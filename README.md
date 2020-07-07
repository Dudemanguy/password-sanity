# password-sanity
**p**ass**w**ord-**s**anity (pws) is a very simple command line tool for managing passwords. Writing this was primarily motivated by the pure insanity that it would be to have good password practices without the help of software (hence the name) and the desire to avoid cloud crap or some complex GUI. The goal is to have safe, secure password storage for multiple accounts while still being easy and convienent to use.

## Installation
There is an [AUR](https://aur.archlinux.org/packages/password-sanity-git/) package available for Arch users.

You can also install the versioned release through pip.  
`# pip install password-sanity`

Note: python-pyperclip does not support wl-clipboard yet. To work around this, you can use [wl-clipboard-x11](https://github.com/brunelli/wl-clipboard-x11) for now.

#### Installing From Source
Note that you don't have to actually install *pws*. You could just execute it directly. You will need python-gnupg and python-pyperclip.

```
$ git clone https://github.com/Dudemanguy/password-sanity.git
$ cd password-sanity
$ python setup.py sdist
# pip install dist/password-sanity-{version}.tar.gaz
```

## Setup
password-sanity relies on gpg for encryption and decryption. You will need to have generated your own gpg key pair with the private key in your keyring. Just run `gpg --full-gen-key` and follow the instructions. After you have a usable gpg key, you need to specify two variables in the `~/.config/pws/config`  (`AppData\Roaming\pws\config` for Windows) file (simply create it if it doesn't exist) like so:
```
gpg=user@domain.com
```

The `gpg` field is simply the email field you specified for the gpg key created earlier.

If you want to move to another machine, you'll need to export the private key. On the other machine, import the key and set the trust level to ultimate (needed if you want encryption/decryption to work). Be sure to move the key securely. The best practice is probably just copying it over with a usb drive and then nuking the usb with zeros after you're done. The master.asc file can be transported in any way you like since it is secure, and only you can decrypt it.

## Usage
On the first usage, pws will prompt you to create the encrypted master file. The location is `~/.local/share/pws/master.asc` (`AppData\Roaming\pws\master.asc` on Windows).

Install any available shell (bash/zsh) completions with:  
`# pws --install-completions`

You can add a new account profile to the master file:  
`pws --new-profile profile-name`  

The above will autogenerate a random password of length 16 (guaranteed to have at least one digit, lowercase, uppercase, and special character). If you wish to change the password length, you can just pass the `--password-length` argument:  
`pws --new-profile profile-name --password-length 24`  
If you want to manually type a password in, use `--password-length 0`.

Modify an existing profile:  
`pws --modify-profile profile-name`  
You can pass `--password-length` and `--field` with `--modify-profile` as well.

List all saved profiles:
`pws --list-profiles`

Removing profiles:  
`pws --remove-profile profile-name`

Retrieving a profile's password and storing it in the system's clipboard:  
`pws --get-profile profile-name`

Retrieving a profile's username and storing it in the system's clipboard:  
`pws --get-profile profile-name --field username`

Creating a brand new encrypted master:  
`pws --new-master`

Copying the master and encrypting it with a new gpg key:  
`pws --copy-master new_user@domain.com path/to/new/file.asc`


## Notes
The structure of the decrypted master.asc file is simply JSON. The highest level key fields are the names of the profiles. In each profile field, there is a `username` and `password` key with the appropriate matching value. You can create your own master.asc with whatever method you like as long as it follows this structure. Just encrypt with the same gpg key you use with pws and save it as `~/.local/share/pws/master.asc`.

Example:
```
{
	"profile1": {
		"username": "user1",
		"password": "pass1"
	},
	"profile2": {
		"username": "user2",
		"password": "pass2"
	},
	"profile3": {
		"username": "user3",
		"password": "pass3"
	}
}
```

## TODO
* Write some manpages

## License
GPLv3

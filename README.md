# pam-tester

pam-tester is a tool to verify PAM auth configurations. It is intended to run in CI settings where you want to make sure you are generating a working PAM configuration. But it can also be used in many other settings.

Features:

* support username and password auth with one factor
* check different pam stacks
* check for failed auth conditions

## Installation

You can either clone this repository and run `pam-tester.py` with your local Python. Or you can use a prebuild executable that should be usable on most current Linux distributions.

### Download

```bash
wget https://github.com/schurzi/pam-tester/releases/download/latest/pam-tester
chmod +x pam-tester
./pam-tester
```

### Build

```bash
git clone https://github.com/schurzi/pam-tester
cd pam-tester
pip install -r requirements.txt
python pam-tester.py
```

## Usage

```text
Usage: pam-tester [OPTIONS]

  A basic testing programm for PAM tests.

Options:
  --user TEXT      username for authentication.
  --password TEXT  Password of the user.
  --stack TEXT     PAM stack to test.
  --expectfail     invert return code (True if PAM stack failed, False if success).

  --help           Show this message and exit.
```

If you call this tool without any options, it will try to authenticate as `root`. The password will be queried, if you do not specify one via option. The default PAM stack `login` is used, if you want to check any other stack (indicated by the filename in `/etc/pam.d`) you have to specify this stack by name.

### Examples

```bash
useradd -m testuser
echo "Sup3rPassw0rd" | passwd testuser --stdin
# --------------------------------------------------
./pam-tester --user testuser --password Sup3rPassw0rd
# authenticating user testuser in PAM stack login, status: PAM code 0, PAM reason Success
echo $?
# 0
# --------------------------------------------------
./pam-tester --user testuser --password test
# authenticating user testuser in PAM stack login, status: PAM code 7, PAM reason Authentication failure
echo $?
# 1
# --------------------------------------------------
./pam-tester --user testuser --password Sup3rPassw0rd --expectfail
# authenticating user testuser in PAM stack login, status: PAM code 0, PAM reason Success
echo $?
# 1
# --------------------------------------------------
./pam-tester --user testuser --password test --expectfail
# authenticating user testuser in PAM stack login, status: PAM code 7, PAM reason Authentication failure
echo $?
# 0
```

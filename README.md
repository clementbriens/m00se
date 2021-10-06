# m00se
python malware project for educative purposes


## Installation

`git clone https//github.com/clementbriens/m00se`
`virtualenv env -p python3 && source env/bin/activate`
`pip install -r requirements.txt`

## Usage

Run the server file:
`python modules/c2/server.py`

Run the main m000se RAT file:
`python main.py`

## Features

### C2

- C2 communications over HTTP
- Base64 encoding of all communications
- Dead drop C2 information on pastebin or gist

TODO:

- Bases are laid for AES encryption of all comms
- Encrypt C2 information


### Recon

- Get file list
- Get process list
- Get host info

TODO:

- Get list of security processes from process list
- Kill individual processes by PID
- Network reconaissance features
- Exfiltrate files from client

### Execution

- Spawn shell

TODO:

- Download and execute payload from server

### Persistence

TODO:
- Establish persistence via registry key

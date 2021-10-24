# UPA_2021
Data Storage and Preparation project, FIT VUT 2021

## Installation
For running python script, install Python interpret. Virtual environment is recommended.

1. Download requirments using pip module:
    python -m pip install requirements.txt
2. Run cassandra server (usage of virtual machine from https://rychly-edu.gitlab.io/dbs/nosql/nixos-dbs-vm/ with VirtualBox is recommended)
3. add port-forwarding rule for host and guest port 9042 (default cassandra port) in virtualBox VM settings
4. start virtual machine and run python script in host os
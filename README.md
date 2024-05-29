# ansible-knock
Plugin for ansible for knock port before ssh

Updated to recent andisle 2.16.6

## Usage

Check https://docs.ansible.com/ansible/latest/plugins/plugins.html for information how to use plugins.

Download plugin file `ssh_pkn.py` to some path, for example `../../plugins/connection_plugins`, and then reference it in config. Set `knock_ports` in playbook variables.

### ansible.cfg
```
[defaults]
connection_plugins       = ../../plugins/connection_plugins
```

### playbook.yaml
```
---
- hosts: myhosts
  user: root
  become: yes
  become_method: sudo
  vars:
    ansible_connection: ansible.legacy.ssh_pkn
    knock_ports: [8888,9999]
  roles:
    ...
```

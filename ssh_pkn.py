# Copyright (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright 2015 Abhijit Menon-Sen <ams@2ndQuadrant.com>
# Copyright 2017 Toshio Kuratomi <tkuratomi@ansible.com>
# Copyright (c) 2017 Ansible Project
# Copyright (c) 2018, Maksim Mikhailin <mcsimz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''

    connection: ssh
    short_description: connect via ssh client binary
    description:
        - This connection plugin allows ansible to communicate to the target machines via normal ssh command line.
        - Ansible does not expose a channel to allow communication between the user and the ssh process to accept
          a password manually to decrypt an ssh key when using this connection plugin (which is the default). The
          use of ``ssh-agent`` is highly recommended.
    author: ansible (@core)
    version_added: historical

    options:

      knock_ports:
          description: Port(s) to knock before connect
          default: null
          vars:
               - name: knock_ports
                 version_added: '2.5'
      knock_delay:
          description: Delay between knock
          default: 0.5
          type: float
          vars:
               - name: knock_delay

      host:
          description: Hostname/IP to connect to.
          default: inventory_hostname
          type: string
          vars:
               - name: inventory_hostname
               - name: ansible_host
               - name: ansible_ssh_host
               - name: delegated_vars['ansible_host']
               - name: delegated_vars['ansible_ssh_host']
      host_key_checking:
          description: Determines if SSH should reject or not a connection after checking host keys.
          default: True
          type: boolean
          ini:
              - section: defaults
                key: 'host_key_checking'
              - section: ssh_connection
                key: 'host_key_checking'
                version_added: '2.5'
          env:
              - name: ANSIBLE_HOST_KEY_CHECKING
              - name: ANSIBLE_SSH_HOST_KEY_CHECKING
                version_added: '2.5'
          vars:
              - name: ansible_host_key_checking
                version_added: '2.5'
              - name: ansible_ssh_host_key_checking
                version_added: '2.5'
      password:
          description: Authentication password for the O(remote_user). Can be supplied as CLI option.
          type: string
          vars:
              - name: ansible_password
              - name: ansible_ssh_pass
              - name: ansible_ssh_password
      sshpass_prompt:
          description:
              - Password prompt that sshpass should search for. Supported by sshpass 1.06 and up.
              - Defaults to C(Enter PIN for) when pkcs11_provider is set.
          default: ''
          type: string
          ini:
              - section: 'ssh_connection'
                key: 'sshpass_prompt'
          env:
              - name: ANSIBLE_SSHPASS_PROMPT
          vars:
              - name: ansible_sshpass_prompt
          version_added: '2.10'
      ssh_args:
          description: Arguments to pass to all SSH CLI tools.
          default: '-C -o ControlMaster=auto -o ControlPersist=60s'
          type: string
          ini:
              - section: 'ssh_connection'
                key: 'ssh_args'
          env:
              - name: ANSIBLE_SSH_ARGS
          vars:
              - name: ansible_ssh_args
                version_added: '2.7'
      ssh_common_args:
          description: Common extra args for all SSH CLI tools.
          type: string
          ini:
              - section: 'ssh_connection'
                key: 'ssh_common_args'
                version_added: '2.7'
          env:
              - name: ANSIBLE_SSH_COMMON_ARGS
                version_added: '2.7'
          vars:
              - name: ansible_ssh_common_args
          cli:
              - name: ssh_common_args
          default: ''
      ssh_executable:
          default: ssh
          description:
            - This defines the location of the SSH binary. It defaults to V(ssh) which will use the first SSH binary available in $PATH.
            - This option is usually not required, it might be useful when access to system SSH is restricted,
              or when using SSH wrappers to connect to remote hosts.
          type: string
          env: [{name: ANSIBLE_SSH_EXECUTABLE}]
          ini:
          - {key: ssh_executable, section: ssh_connection}
          #const: ANSIBLE_SSH_EXECUTABLE
          version_added: "2.2"
          vars:
              - name: ansible_ssh_executable
                version_added: '2.7'
      sftp_executable:
          default: sftp
          description:
            - This defines the location of the sftp binary. It defaults to V(sftp) which will use the first binary available in $PATH.
          type: string
          env: [{name: ANSIBLE_SFTP_EXECUTABLE}]
          ini:
          - {key: sftp_executable, section: ssh_connection}
          version_added: "2.6"
          vars:
              - name: ansible_sftp_executable
                version_added: '2.7'
      scp_executable:
          default: scp
          description:
            - This defines the location of the scp binary. It defaults to V(scp) which will use the first binary available in $PATH.
          type: string
          env: [{name: ANSIBLE_SCP_EXECUTABLE}]
          ini:
          - {key: scp_executable, section: ssh_connection}
          version_added: "2.6"
          vars:
              - name: ansible_scp_executable
                version_added: '2.7'
      scp_extra_args:
          description: Extra exclusive to the C(scp) CLI
          type: string
          vars:
              - name: ansible_scp_extra_args
          env:
            - name: ANSIBLE_SCP_EXTRA_ARGS
              version_added: '2.7'
          ini:
            - key: scp_extra_args
              section: ssh_connection
              version_added: '2.7'
          cli:
            - name: scp_extra_args
          default: ''
      sftp_extra_args:
          description: Extra exclusive to the C(sftp) CLI
          type: string
          vars:
              - name: ansible_sftp_extra_args
          env:
            - name: ANSIBLE_SFTP_EXTRA_ARGS
              version_added: '2.7'
          ini:
            - key: sftp_extra_args
              section: ssh_connection
              version_added: '2.7'
          cli:
            - name: sftp_extra_args
          default: ''
      ssh_extra_args:
          description: Extra exclusive to the SSH CLI.
          type: string
          vars:
              - name: ansible_ssh_extra_args
          env:
            - name: ANSIBLE_SSH_EXTRA_ARGS
              version_added: '2.7'
          ini:
            - key: ssh_extra_args
              section: ssh_connection
              version_added: '2.7'
          cli:
            - name: ssh_extra_args
          default: ''
      reconnection_retries:
          description:
            - Number of attempts to connect.
            - Ansible retries connections only if it gets an SSH error with a return code of 255.
            - Any errors with return codes other than 255 indicate an issue with program execution.
          default: 0
          type: integer
          env:
            - name: ANSIBLE_SSH_RETRIES
          ini:
            - section: connection
              key: retries
            - section: ssh_connection
              key: retries
          vars:
            - name: ansible_ssh_retries
              version_added: '2.7'
      port:
          description: Remote port to connect to.
          type: int
          ini:
            - section: defaults
              key: remote_port
          env:
            - name: ANSIBLE_REMOTE_PORT
          vars:
            - name: ansible_port
            - name: ansible_ssh_port
          keyword:
            - name: port
      remote_user:
          description:
              - User name with which to login to the remote server, normally set by the remote_user keyword.
              - If no user is supplied, Ansible will let the SSH client binary choose the user as it normally.
          type: string
          ini:
            - section: defaults
              key: remote_user
          env:
            - name: ANSIBLE_REMOTE_USER
          vars:
            - name: ansible_user
            - name: ansible_ssh_user
          cli:
            - name: user
          keyword:
            - name: remote_user
      pipelining:
          env:
            - name: ANSIBLE_PIPELINING
            - name: ANSIBLE_SSH_PIPELINING
          ini:
            - section: defaults
              key: pipelining
            - section: connection
              key: pipelining
            - section: ssh_connection
              key: pipelining
          vars:
            - name: ansible_pipelining
            - name: ansible_ssh_pipelining

      private_key_file:
          description:
              - Path to private key file to use for authentication.
          type: string
          ini:
            - section: defaults
              key: private_key_file
          env:
            - name: ANSIBLE_PRIVATE_KEY_FILE
          vars:
            - name: ansible_private_key_file
            - name: ansible_ssh_private_key_file
          cli:
            - name: private_key_file
              option: '--private-key'

      control_path:
        description:
          - This is the location to save SSH's ControlPath sockets, it uses SSH's variable substitution.
          - Since 2.3, if null (default), ansible will generate a unique hash. Use ``%(directory)s`` to indicate where to use the control dir path setting.
          - Before 2.3 it defaulted to ``control_path=%(directory)s/ansible-ssh-%%h-%%p-%%r``.
          - Be aware that this setting is ignored if C(-o ControlPath) is set in ssh args.
        type: string
        env:
          - name: ANSIBLE_SSH_CONTROL_PATH
        ini:
          - key: control_path
            section: ssh_connection
        vars:
          - name: ansible_control_path
            version_added: '2.7'
      control_path_dir:
        default: ~/.ansible/cp
        description:
          - This sets the directory to use for ssh control path if the control path setting is null.
          - Also, provides the ``%(directory)s`` variable for the control path setting.
        type: string
        env:
          - name: ANSIBLE_SSH_CONTROL_PATH_DIR
        ini:
          - section: ssh_connection
            key: control_path_dir
        vars:
          - name: ansible_control_path_dir
            version_added: '2.7'
      sftp_batch_mode:
        default: true
        description: 'TODO: write it'
        env: [{name: ANSIBLE_SFTP_BATCH_MODE}]
        ini:
        - {key: sftp_batch_mode, section: ssh_connection}
        type: bool
        vars:
          - name: ansible_sftp_batch_mode
            version_added: '2.7'
      ssh_transfer_method:
        description: Preferred method to use when transferring files over ssh
        choices:
              sftp: This is the most reliable way to copy things with SSH.
              scp: Deprecated in OpenSSH. For OpenSSH >=9.0 you must add an additional option to enable scp C(scp_extra_args="-O").
              piped: Creates an SSH pipe with C(dd) on either side to copy the data.
              smart: Tries each method in order (sftp > scp > piped), until one succeeds or they all fail.
        default: smart
        type: string
        env: [{name: ANSIBLE_SSH_TRANSFER_METHOD}]
        ini:
            - {key: transfer_method, section: ssh_connection}
        vars:
            - name: ansible_ssh_transfer_method
              version_added: '2.12'
      scp_if_ssh:
        deprecated:
              why: In favor of the O(ssh_transfer_method) option.
              version: "2.17"
              alternatives: O(ssh_transfer_method)
        default: smart
        description:
          - "Preferred method to use when transferring files over SSH."
          - When set to V(smart), Ansible will try them until one succeeds or they all fail.
          - If set to V(True), it will force 'scp', if V(False) it will use 'sftp'.
          - For OpenSSH >=9.0 you must add an additional option to enable scp (C(scp_extra_args="-O"))
          - This setting will overridden by O(ssh_transfer_method) if set.
        env: [{name: ANSIBLE_SCP_IF_SSH}]
        ini:
        - {key: scp_if_ssh, section: ssh_connection}
        vars:
          - name: ansible_scp_if_ssh
            version_added: '2.7'
      use_tty:
        version_added: '2.5'
        default: true
        description: add -tt to ssh commands to force tty allocation.
        env: [{name: ANSIBLE_SSH_USETTY}]
        ini:
        - {key: usetty, section: ssh_connection}
        type: bool
        vars:
          - name: ansible_ssh_use_tty
            version_added: '2.7'
      timeout:
        default: 10
        description:
            - This is the default amount of time we will wait while establishing an SSH connection.
            - It also controls how long we can wait to access reading the connection once established (select on the socket).
        env:
            - name: ANSIBLE_TIMEOUT
            - name: ANSIBLE_SSH_TIMEOUT
              version_added: '2.11'
        ini:
            - key: timeout
              section: defaults
            - key: timeout
              section: ssh_connection
              version_added: '2.11'
        vars:
          - name: ansible_ssh_timeout
            version_added: '2.11'
        cli:
          - name: timeout
        type: integer
      pkcs11_provider:
        version_added: '2.12'
        default: ""
        type: string
        description:
          - "PKCS11 SmartCard provider such as opensc, example: /usr/local/lib/opensc-pkcs11.so"
          - Requires sshpass version 1.06+, sshpass must support the -P option.
        env: [{name: ANSIBLE_PKCS11_PROVIDER}]
        ini:
          - {key: pkcs11_provider, section: ssh_connection}
        vars:
          - name: ansible_ssh_pkcs11_provider
'''

import errno
import fcntl
import hashlib
import os
import pty
import subprocess
import time

from time import sleep

from functools import wraps
from ansible import constants as C
from ansible.errors import AnsibleError, AnsibleConnectionFailure, AnsibleFileNotFound
from ansible.errors import AnsibleOptionsError
from ansible.compat import selectors
from ansible.module_utils.six import PY3, text_type, binary_type
from ansible.module_utils.six.moves import shlex_quote
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.module_utils.parsing.convert_bool import BOOLEANS, boolean
from ansible.plugins.connection.ssh import Connection as ConnectionSSH
from ansible.utils.path import unfrackpath, makedirs_safe
from socket import create_connection

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class Connection(ConnectionSSH):
    ''' ssh based connections '''

    transport = 'ssh-pkn'
    has_pipelining = True

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        display.vvv("DICT: {0}".format(*kwargs))
        
        display.vvv("SSH_PKN (Port KNock) connection plugin is used for this host", host=self.host)
        
    def _connect(self):
        knock_delay = self.get_option('knock_delay')
        if knock_delay is not None:
            if not (isinstance(knock_delay,float) or isinstance(knock_delay,int)):
                raise AnsibleError("knock_delay parameter for host '{}' must be float or int!".format(host))
            display.vvv("Delay is {0} for host {1}".format(knock_delay, self.host))
        else:
            knock_delay=0.5
            
        knock_ports = self.get_option('knock_ports')
        if knock_ports is not None:
            if not isinstance(knock_ports,list):
                raise AnsibleError("knock_ports parameter for host '{}' must be list!".format(host))
            display.vvv("knock to ports {0} for host {1}".format(knock_ports, self.host))
            for port in knock_ports:
                try:
                    create_connection((self.host, port), 1)
                except:
                        pass
                display.vvv("Waiting for {0} seconds after knock".format(knock_delay), host=self.host)
                sleep(knock_delay)
        return self

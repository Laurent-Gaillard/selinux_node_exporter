Backport of SELinux policy module for Node Exporter (Prometheus)
==========================================================

<https://github.com/Laurent-Gaillard/selinux_node_exporter>

## Introduction 

This SELinux policy module is a backport of the Node Exporter module included in newer versions of the refpolicy (<https://github.com/SELinuxProject/refpolicy>). It will allow people with older versions this is the case on RHEL 7 and 8) of the policy to manage SELinux for Node Exporter easily.

When used correctly, this SELinux policy module will make the Node Exporter application run in the dedicated *node_exporter_t* SELinux domain.

The original module was customized to create a *node_exporter_port_t* port type and allow the *node_exporter_t* domain to bind / listen on to it.

## How to use this SELinux module

Once the SELinux policy module is compiled and installed in the running kernel SELinux policy, a few actions must be taken for the new policy to apply to the Node Exporter application.

### Filesystem and binary labelling

This module will work with the following conventions.

In order to run in the *node_exporter_t* SELinux confined domain, the Node Exporter binary must be assigned the **node_exporter_exec_t** type and the application must be started using systemd.
By default, this type will be assigned to the following filepaths:  

- /usr/bin/node_exporter
- /usr/sbin/node_exporter

The Node Exporter application log files top level directory must assigned the **node_exporter_log_t** type. By default, this location should be:

- /var/log/node_exporter.

Application persistent data should be located in the following directory and subdirectories and must be assigned **node_exporter_var_lib_t** type:

- /var/lib/node_exporter .

Finaly, if you want to use a pid file, it must be /run/node_exporter.pid and must be assigned type **node_exporter_runtime_t**.

#### Customizing file location

It is possible to customize above file locations to your needs using semanage equivalency rules.

For example, if you want to place the Node Exporter logs instead of /var/log/node_exporter (policy module default) into /var/log/tooling/node_exporter, you must do:  
``semanage fcontext -a -e /var/log/node_exporter /var/log/tooling/node_exporter``  
``restorecon -RvF /var/log/tooling/node_exporter``

### Networking

#### Default listening ports

By default, Node Exporter is configured to listen on TCP port 9100.  

In the refpolicy module, no port type was explicitly defined for Node Exporter. As a result for Node Exporter to work, the refpolicy module allows **node_exporter_t** domain to bind to *hplip_port_t* labeled ports.  
This means that it can also listen on all the following TCP ports:

- 1782
- 2207 - 2208
- 8290
- 8292, 9100
- 9101 - 9102
- 9220 - 9222
- 9280 - 9282
- 9290 - 9291
- 50000, 50002

This Node Exporter policy module defines the ``strict_node_exporter_network_rules`` (default: false) boolean, should you want to restrict the network permissions from the original refpolicy module.

#### Listen on customized port(s)

This Node Exporter policy module defines the dedicated port type *node_exporter_port_t*. The **node_exporter_t** domain is always allowed to bind this port type.  
To keep a clean and proper network segregation/confinement between processes, it is much safer to assign the *node_exporter_port_t* type to any TCP port Node Exporter is legitimately configured to use.  
This will also prevent any other application authorized to connect / listen to *hplip_port_t* to have permissions on a customized port.

If your Node Exporter application needs to run on a customized port, assign the *node_exporter_port_t* type to your customized TCP port with **semanage** command:
``semanage port -a -t node_exporter_port_t -p tcp <PORT>``

Beware that you should not assign the **node_exporter_port_t** type to TCP 9100 port if any of the applications running on the same host legitimately needs to connect to printing solutions based on HP protocols and technologies.

## Starting the Node Exporter application

The Node Exporter application should always and only be started as a **systemd** service using the systemctl command.

This method ensures that Node Exporter is running in a confined domain.

To create a systemd unit for Node Exporter, you can have a look at:
<https://github.com/prometheus/node_exporter/tree/master/examples/systemd>

The service or target unit files MUST be located in /etc/systemd/system or in /lib/systemd/system.

When started correctly, your Node Exporter process shallt be running like that ("ps -efZ" is your best friend):
``system_u:system_r:**node_exporter_t**:SystemLow node_exporter 9796  1  0 17:48 ?        00:00:00 /usr/sbin/node_exporter``

## Disclaimer

The code of the this SELinux policy module is provided AS-IS. People and organisation willing to use it must be fully aware that they are doing so at their own risks and expenses.

The Author(s) of this SELinux policy module SHALL NOT be held liable nor accountable, in  any way, of any malfunction or limitation of said module, nor of the resulting damage, of any kind, resulting, directly or indirectly, of the usage of this SELinux policy module.

It is strongly advised to always use the last version of the code, to check for the compatibility of the platform where it is about to be deployed, to compile the module on the target specific Linux distribution and version where it is intended to be used.

Finally, users should check regularly for updates.

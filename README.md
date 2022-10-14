Backport of SELinux policy module for Node Exporter (Prometheus)
==========================================================
https://github.com/Laurent-Gaillard/selinux_node_exporter

## Introduction

This SELinux policy module is a backport of the Node Exporter module that is included in
newer versions of the refpolicy (https://github.com/SELinuxProject/refpolicy). It will allow 
people with older versions (this is the case on RHEL 7 and 8) of the policy to manage SELinux 
for Node Exporter easily.

When used correctly, this SELinux policy module will make the Node Exporter application
run on the host in the dedicated *node_exporter_t* SELinux domain.

The original module was customized to create a *node_exporter_port_t* port type and allow 
*node_exporter_t* domain to listen to it.

## How to use this SELinux module

Once the SELinux policy module is compiled and installed in the running Kernel SELinux
policy, a few actions must be taken for the new policy to apply to the Node Exporter
application.

### Filesystem and binary labelling

This module will work with the following conventions.

The Node Exporter binary in order to run in the confined SELinux domain *node_exporter_t* must be either in:  
- /usr/bin/node_exporter
- /usr/sbin/node_exporter

The root directory for log files of the Node Exporter application is expected to be 
 /var/log/node_exporter.

The persistent data modified by the application must be in /var/lib/node_exporter and its subdirectories.

And finaly, the pid file must be /run/node_exporter.pid.

### Networking

#### Default Listening ports
By default Node Exporter is configured to listen on port 9100 (which ).
In the refpolicy module, no port type was explicitly defined for node exporter.

By default, Node Exporter listens on port 9100. 
For this to work, the original SELinux Node Exporter module supports binding on port labeled *hplip_port_t*.
This means that it can listen on all the following tcp ports: 
- 1782
- 2207
- 2208
- 8290
- 8292
- 9100
- 9101
- 9102
- 9220
- 9221
- 9222
- 9280
- 9281
- 9282
- 9290
- 9291
- 50000
- 50002

#### Listen on customized port

For that purpose, we have created a dedicated port type *node_exporter_port_t* to avoid adding ports to *hplip_port_t*.
This prevents anyother application authorized to connect / listen to *hplip_port_t* to have rights on an unwanted port.

So if you need the application to run on another port you must just add with **semanage** command your tcp port to *node_exporter_port_t* type:
> semanage port -a -t node_exporter_port_t -p tcp \<PORT\>

### Starting the Springboot application

The Springboot application should always and ony be started as a **systemd** service using
the`systemctl` command.

The service or target unit files MUST be located in /etc/systemd/system or in
/lib/systemd/system, the file name MUST start with `springboot`.
Directories to tune or override unit behaviour are supported.
Template/instantiated units are supported provided the master file is named
`springboot@.service`.

The script(s) used to start or stop the Springboot application MUST be located in the 
/opt/springboot/service/ directory. The /opt/springboot/bin/springboot_service file name
is also supported.

## Disclaimer

The code of the this SELinux policy module is provided AS-IS. People and organisation
willing to use it must be fully aware that they are doing so at their own risks and
expenses.

The Author(s) of this SELinux policy module SHALL NOT be held liable nor accountable, in
 any way, of any malfunction or limitation of said module, nor of the resulting damage, of
 any kind, resulting, directly or indirectly, of the usage of this SELinux policy module.

It is strongly advised to always use the last version of the code, to check for the 
compatibility of the platform where it is about to be deployed, to compile the module on
the target specific Linux distribution and version where it is intended to be used.

Finally, users should check regularly for updates.

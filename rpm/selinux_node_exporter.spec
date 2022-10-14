Name:		node_exporter-selinux
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	SELinux policy module for Node Exporter
License:	GPLv2
URL:		https://github.com/Laurent-Gaillard/selinux_node_exporter
BuildArch:	noarch

BuildRequires:	selinux-policy-devel
BuildRequires:	make

Requires:	selinux-policy-targeted %{?_sepol_minver_cond}
Requires:	selinux-policy-targeted %{?_sepol_maxver_cond}

Requires:	policycoreutils
Requires:	policycoreutils-python-utils
Requires:	libselinux-utils

%description
SELinux policy module to confine node_exporter application started using systemd.
The systemd service unit name must start with node_exporter, the node_exporter 
binaray must be assigned the node_exporter_exec_t SELinux type.
The node_exporter application will run in the node_exporter_t domain.

###################################

%clean
%{__rm} -rf %{buildroot}

###################################

%build

make -f /usr/share/selinux/devel/Makefile -C %{_builddir} node_exporter.pp

###################################

%install

mkdir -p -m 0755 %{buildroot}/usr/share/selinux/packages/targeted
mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}
mkdir -p -m 0755 %{buildroot}/%{_datarootdir}/%{name}

install -m 0444 %{_builddir}/node_exporter.pp %{buildroot}/usr/share/selinux/packages/targeted/
install -m 0444 %{_builddir}/{LICENSE,README.md} %{buildroot}/%{_docdir}/%{name}/

###################################

%post

semodule -i /usr/share/selinux/packages/targeted/node_exporter.pp

if selinuxenabled
then
  restorecon -RFi /usr/{bin,sbin}/node_exporter 
  restorecon -RFi /{lib,etc}/systemd/system/node_exporter*
  restorecon -RFi /var/{lib,log,run}/node_exporter
  restorecon -RFi /run/node_exporter
fi

###################################

%postun

if [ $1 -eq 0 ]
then
  semodule -r node_exporter
fi

###################################

%files
%defattr(-,root,root,-)
/usr/share/selinux/packages/targeted/node_exporter.pp
%dir %{_docdir}/%{name}
%license  %{_docdir}/%{name}/LICENSE
%doc      %{_docdir}/%{name}/README.md

Name:           mydns-toolkit
Version:        1.0
Release:        1%{?dist}
Summary:        Toolkit scripts and systemd units for MyDNS

License:        MIT
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz

%description
Toolkit scripts for MyDNS and systemd units for periodic IP notifications.

%prep
%setup -q

%build
# Nothing to build

%install
mkdir -p %{buildroot}/usr/libexec/mydns-toolkit
cp delete.sh notify.sh regist.sh %{buildroot}/usr/libexec/mydns-toolkit/
chmod 0755 %{buildroot}/usr/libexec/mydns-toolkit/*.sh

mkdir -p %{buildroot}/usr/lib/systemd/system
cp mydns-notify-ip.service mydns-notify-ip.timer %{buildroot}/usr/lib/systemd/system/

mkdir -p %{buildroot}/usr/lib/systemd/system
cp mydns-notify-ip.service mydns-notify-ip.timer %{buildroot}/usr/lib/systemd/system/

%files
/usr/libexec/mydns-toolkit/delete.sh
/usr/libexec/mydns-toolkit/notify.sh
/usr/libexec/mydns-toolkit/regist.sh
/usr/lib/systemd/system/mydns-notify-ip.service
/usr/lib/systemd/system/mydns-notify-ip.timer

%changelog
* Thu Jun 26 2025 seinolab - 1.0-1
- Initial RPM release

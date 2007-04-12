%define name	ices
%define version	2.0.1
%define release	%mkrel 5

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Source streaming for Icecast
Group:		System/Servers
License:	GPL
URL:		http://www.icecast.org
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.init.bz2
Source2:	%{name}.logrotate.bz2
BuildRequires:	libxml2-devel
BuildRequires:	libshout-devel >= 2.0-2mdk
BuildRequires:	pkgconfig
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires(pre):		rpm-helper
Requires(preun):		rpm-helper
Requires(post):		rpm-helper
Requires(postun):		rpm-helper

%description
IceS is a source client for a streaming server. The purpose of this client is
to provide an audio stream to a streaming server such that one or more
listeners can access the stream. With this layout, this source client can be
situated remotely from the icecast server.

The primary example of a streaming server used is Icecast 2, although others
could be used if certain conditions are met.

%prep
%setup -q
bzcat %{SOURCE1} > %{name}.init
bzcat %{SOURCE2} > %{name}.logrotate
perl -pi -e 's|<background>0</background>|<background>1</background>|' conf/*.xml

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 src/%{name} $RPM_BUILD_ROOT%{_bindir}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 conf/ices-playlist.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{name}.init $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{name}.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_var}/log/%{name}

%clean 
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd %{name} %{_var}/log/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README TODO doc/*.html doc/*.css conf/*.xml
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_initrddir}/%{name}
%attr(-,ices,ices) %{_var}/log/%{name}



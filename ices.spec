Name:           ices
Version:        2.0.1
Release:        %mkrel 9
Summary:        Source streaming for Icecast
Group:          System/Servers
License:        GPL
URL:            http://www.icecast.org/
Source0:        http://downloads.us.xiph.org/releases/ices/ices-2.0.1.tar.bz2
Source1:        %{name}.init
Source2:        %{name}.logrotate
BuildRequires:  alsa-lib-devel
BuildRequires:  libshout-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
Requires(pre):  rpm-helper
Requires(preun): rpm-helper
Requires(post): rpm-helper
Requires(postun): rpm-helper
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
IceS is a source client for a streaming server. The purpose of this client is
to provide an audio stream to a streaming server such that one or more
listeners can access the stream. With this layout, this source client can be
situated remotely from the icecast server.

The primary example of a streaming server used is Icecast 2, although others
could be used if certain conditions are met.

%prep
%setup -q
%{__perl} -pi -e 's|<background>0</background>|<background>1</background>|' conf/*.xml

%build
%{configure2_5x}
%{make}

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a src/%{name} $RPM_BUILD_ROOT%{_bindir}

%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__cp} -a conf/ices-playlist.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} -a %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
%{__cp} -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

%{__mkdir_p} %{buildroot}%{_var}/log/%{name}
/bin/touch %{buildroot}%{_var}/log/%{name}/ices.log

%clean 
%{__rm} -rf %{buildroot}

%pre
%_pre_useradd %{name} %{_var}/log/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING README TODO doc/*.html doc/*.css conf/*.xml
%attr(0755,root,root) %{_bindir}/%{name}
%config(noreplace) %attr(0640,root,ices) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %config(noreplace) %{_initrddir}/%{name}
%dir %{_logdir}/%{name}
%attr(0644,ices,ices) %{_logdir}/%{name}/ices.log

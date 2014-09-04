Name:           ices
Version:        2.0.1
Release:        13
Summary:        Source streaming for Icecast
Group:          System/Servers
License:        GPL
URL:            http://www.icecast.org/
Source0:        http://downloads.us.xiph.org/releases/ices/ices-2.0.1.tar.bz2
Source1:        %{name}.service
Source2:        %{name}.logrotate
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(shout)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig
Requires(pre):  rpm-helper
Requires(preun): rpm-helper
Requires(post): rpm-helper
Requires(postun): rpm-helper

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
%configure2_5x
%make

%install
%{__mkdir_p} %{buildroot}%{_bindir}
cp -a src/%{name} %{buildroot}%{_bindir}

%{__mkdir_p} %{buildroot}%{_sysconfdir}
cp -a conf/ices-playlist.xml %{buildroot}%{_sysconfdir}/%{name}.conf

%{__mkdir_p} %{buildroot}%{_unitdir}
cp -a %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__mkdir_p} %{buildroot}%{_var}/log/%{name}
/bin/touch %{buildroot}%{_var}/log/%{name}/ices.log

%pre
%_pre_useradd %{name} %{_var}/log/%{name} /bin/false

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%_postun_userdel %{name}
%systemd_postun_with_restart %{name}.service

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING README TODO doc/*.html doc/*.css conf/*.xml
%attr(0755,root,root) %{_bindir}/%{name}
%config(noreplace) %attr(0640,root,ices) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %config(noreplace) %{_unitdir}/%{name}.service
%dir %{_logdir}/%{name}
%attr(0644,ices,ices) %{_logdir}/%{name}/ices.log

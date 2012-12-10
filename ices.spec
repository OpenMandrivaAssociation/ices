Name:           ices
Version:        2.0.1
Release:        10
Summary:        Source streaming for Icecast
Group:          System/Servers
License:        GPL
URL:            http://www.icecast.org/
Source0:        http://downloads.us.xiph.org/releases/ices/ices-2.0.1.tar.bz2
Source1:        %{name}.init
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
%{configure2_5x}
%{make}

%install

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


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-10mdv2011.0
+ Revision: 619596
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.0.1-9mdv2010.0
+ Revision: 429491
- rebuild

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 2.0.1-8mdv2009.0
+ Revision: 240834
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Sep 06 2007 David Walluck <walluck@mandriva.org> 2.0.1-6mdv2008.0
+ Revision: 80581
- update logrotate file
- add logfile to package
- spec cleanup
- bunzip2 sources
- build with alsa
- set file ownerships


* Fri Jan 26 2007 Olivier Thauvin <nanardon@mandriva.org> 2.0.1-5mdv2007.0
+ Revision: 113600
- rebuild

* Thu Aug 10 2006 Olivier Thauvin <nanardon@mandriva.org> 2.0.1-4mdv2007.0
+ Revision: 54950
- rebuild
- Import ices

* Mon May 01 2006 Olivier Thauvin <nanardon@mandriva.org> 2.0.1-3mdk
- fix PreReq

* Mon May 01 2006 Olivier Thauvin <nanardon@mandriva.org> 2.0.2-2mdk
- rebuild && %%mkrel

* Wed Feb 16 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.1-1mdk
- 2.0.1

* Fri Apr 23 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.0-4mdk
- fix reload in initscript, HUP doesn't reload configuration

* Sun Apr 11 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.0-3mdk
- fix init script

* Sat Apr 10 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.0-2mdk
- buildrequires

* Sat Apr 10 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.0.0-1mdk
- new release
- logrotate


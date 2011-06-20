# Default of no MySQL, but --with mysql will enable it
%define mysql 1
%{?_with_mysql:%define mysql 1}
# Default of no PostgreSQL, but --with postgresql will enable it
%define postgresql 0
%{?_with_postgresql:%define postgresql 1}

%define realname barnyard2
%define name barnyard
%define version 1.9

Name: %{name}
Summary: Snort Log Backend 
Version: %{version}
Release: %mkrel 1
License: GPL
Group: Monitoring
Source1: %{realname}.config
Source2: %{realname}.init
Source: http://www.securixlive.com/download/%{realname}/%{realname}-%{version}.tar.gz
Url: http://www.securixlive.com/barnyard2/
BuildRequires: libpcap-devel, libpcap
BuildRoot: %{_tmppath}/%{name}-%{version}-root


%description
Barnyard has 3 modes of operation:
One-shot, continual, continual w/ checkpoint.  In one-shot mode,
barnyard will process the specified file and exit.  In continual mode,
barnyard will start with the specified file and continue to process
new data (and new spool files) as it appears.  Continual mode w/
checkpointing will also use a checkpoint file (or waldo file in the
snort world) to track where it is.  In the event the barnyard process
ends while a waldo file is in use, barnyard will resume processing at
the last entry as listed in the waldo file.


%package mysql
Summary: barnyard2 with MySQL support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{mysql}
Requires: mysql
BuildRequires: mysql-devel
%endif
%description mysql
barnyard2 binary compiled with mysql support.

%package postgresql
Summary: barnyard2 with PostgreSQL support
Group: Applications/Internet
Requires: %{name} = %{epoch}:%{version}-%{release}
%if %{postgresql}
Requires: postgresql
BuildRequires: postgresql-devel
%endif
%description postgresql
barnyard2 binary compiled with postgresql support.

%prep
%setup -q -n %{realname}-%{version}

%build
./configure --sysconfdir=%{_sysconfdir}/snort \
   %if %{postgresql}
	--with-postgresql \
   %endif
   %if %{mysql}
	--with-mysql-libraries=/usr/%{_lib} \
   %endif

%install
%makeinstall 

%{__install} -d -p $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d,snort} 
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/contrib
%{__install} -d -p $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -d -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/doc
mv etc/barnyard2.conf $RPM_BUILD_ROOT%{_sysconfdir}/snort
%{__install} -m 644 $RPM_SOURCE_DIR/barnyard2.config $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/barnyard2
%{__install} -m 755 $RPM_SOURCE_DIR/barnyard2.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/barnyard2

rm $RPM_BUILD_ROOT%{_sysconfdir}/barnyard2.conf
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/
%clean
if [ -d $RPM_BUILD_ROOT ] && [ "$RPM_BUILD_ROOT" != "/"  ] ; then
	rm -rf $RPM_BUILD_ROOT
fi

%post
%_post_service barnyard2

%preun
%_preun_service barnyard2


%files
%defattr(-,root,root)
%doc LICENSE
%attr(755,root,root) %{_bindir}/barnyard2
%attr(640,root,root) %config %{_sysconfdir}/snort/barnyard2.conf
%attr(755,root,root) %config %{_sysconfdir}/rc.d/init.d/barnyard2
%attr(644,root,root) %config %{_sysconfdir}/sysconfig/barnyard2

%changelog
* Sat Jan 16 2009 Ian Firns <firnsy@securixlive.com>
- barnyard2-1.8-beta2

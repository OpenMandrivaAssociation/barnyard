# Default of no MySQL, but --with mysql will enable it
%define mysql 1
%{?_with_mysql:%define mysql 1}
# Default of no PostgreSQL, but --with postgresql will enable it
%define postgresql 0
%{?_with_postgresql:%define postgresql 1}

%define realname barnyard2

Name:		barnyard
Summary:	Snort Log Backend 
Version:	1.9
Release:	2
License:	GPL
Group:		Monitoring
Url:		http://www.securixlive.com/barnyard2/
Source0:	http://www.securixlive.com/download/%{realname}/%{realname}-%{version}.tar.gz
Source1:	%{realname}.config
Source2:	%{realname}.init
BuildRequires:	pcap-devel


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
Summary:	barnyard2 with MySQL support
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
%if %{mysql}
Requires:	mysql
BuildRequires:	mysql-devel
%endif

%description mysql
barnyard2 binary compiled with mysql support.

%package postgresql
Summary:	barnyard2 with PostgreSQL support
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
%if %{postgresql}
Requires:	postgresql
BuildRequires:	postgresql-devel
%endif

%description postgresql
barnyard2 binary compiled with postgresql support.

%prep
%setup -q -n %{realname}-%{version}

%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}/snort \
   %if %{postgresql}
	--with-postgresql \
   %endif
   %if %{mysql}
	--with-mysql-libraries=/usr/%{_lib} \
   %endif

%install
%makeinstall_std

install -d -p %{buildroot}%{_sysconfdir}/{sysconfig,rc.d/init.d,snort} 
install -d -p %{buildroot}%{_docdir}/%{name}-%{version}/contrib
install -d -p %{buildroot}%{_mandir}/man8
install -d -p %{buildroot}%{_docdir}/%{name}-%{version}/doc
mv etc/barnyard2.conf %{buildroot}%{_sysconfdir}/snort
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/barnyard2
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/rc.d/init.d/barnyard2

rm -rf %{buildroot}%{_datadir}/doc/

%post
%_post_service barnyard2

%preun
%_preun_service barnyard2


%files
%doc LICENSE
%attr(755,root,root) %{_bindir}/barnyard2
%attr(640,root,root) %config %{_sysconfdir}/snort/barnyard2.conf
%attr(755,root,root) %config %{_sysconfdir}/rc.d/init.d/barnyard2
%attr(644,root,root) %config %{_sysconfdir}/sysconfig/barnyard2


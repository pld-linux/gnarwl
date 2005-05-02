Summary:	Gnu Neat Auto Reply With LDAP
Summary(pl):	Gnu Neat Auto Reply With LDAP - autoresponder korzystaj±cy z LDAP
Name:		gnarwl
Version:	3.3
Release:	3
License:	GPL
Group:		Applications/Mail
Source0:	http://www.oss.billiton.de/download/%{name}-%{version}.tgz
# Source0-md5:	ec2bb56301988e300741eec8190b165e
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-opt.patch
URL:		http://www.oss.billiton.de/
BuildRequires:	autoconf
BuildRequires:	gdbm-devel
BuildRequires:	groff
BuildRequires:	openldap-devel
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(gnarwl)
Provides:	user(gnarwl)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnarwl is a email auto reply/vacation tool, intented to be used on
mailservers, on which users may not (nescessarily) have
systemaccoounts, but where userinformation is stored in LDAP.

%description -l pl
Gnarwl to system automatycznego odpowiadania na listy stworzony z
my¶l± o serwerach poczty, na których u¿ytkownicy nie musz± posiadaæ
prawdziwych kont systemowych, a informacje o u¿ytkownikach znajduj±
siê w bazie LDAP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--with-homedir=/var/lib/gnarwl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 26 gnarwl
%useradd -u 26 -d /var/lib/gnarwl -s /usr/bin/gnarwl -c "Gnarwl User" -g gnarwl gnarwl

%postun
if [ "$1" = "0" ]; then
	%userremove gnarwl
	%groupremove gnarwl
fi

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,FAQ,HISTORY,INSTALL,ISPEnv2.schema,ISPEnv.schema,LICENSE,README,README.upgrade,example.ldif}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,gnarwl) %{_sysconfdir}/gnarwl.cfg
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl/block
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl/bin
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/.forward
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/blacklist.db
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/badheaders.db
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/footer.txt
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/header.txt
%{_mandir}/man*/*

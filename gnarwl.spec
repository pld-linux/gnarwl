Summary:	Gnu Neat Auto Reply With LDAP
Summary(pl):	Gnu Neat Auto Reply With LDAP
Name:		gnarwl
Version:	1.2
Release:	2
License:	GPL
Group:		Applications/Mail
Source0:	http://www.oss.billiton.de/download/%{name}-%{version}.tgz
Patch0:		%{name}-DESTDIR.patch
BuildRequires:	openldap-devel
BuildRequires:	gdbm-devel
URL:		http://www.oss.billiton.de
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnarwl is a email auto reply/vacation tool, intented to be used on
mailservers, on which users may not (nescessarily) have
systemaccoounts, but where userinformation is stored in LDAP.

%description -l pl
Gnarwl, to system automatycznego odpowiadania na listy stworzony z
my¶l± o serwerach poczty, na których u¿ytkownicy nie musz± posiadaæ
prawdziwych kont systemowych, a informacje o u¿ytkownikach znajduj±
siê w bazie LDAP.

%prep
%setup -q
%patch -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man8

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \

install doc/gnarwl.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo '|/usr/bin/gnarwl' > $RPM_BUILD_ROOT/var/lib/gnarwl/.forward

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid gnarwl`" ]; then
        if [ "`/usr/bin/getgid gnarwl`" != "26" ]; then
                echo "Warning: group gnarwl haven't gid=26. Correct this before installing gnarwl" 1>&2
                exit 1
        fi
else
	/usr/sbin/groupadd -g 26 -r -f gnarwl
fi
if [ -n "`/bin/id -u gnarwl 2>/dev/null`" ]; then
	if [ "`/bin/id -u gnarwl`" != "26" ]; then
		echo "Warning: user gnarwl haven't uid=26. Correct this before installing gnarwl"
1>&2
	exit 1
	fi
else
	/usr/sbin/useradd -u 26 -r -d /var/lib/gnarwl -s /usr/bin/gnarwl -c "Gnarwl User" -g gnarwl gnarwl 1>&2
fi

%postun
if [ "$1" = "0" ]; then
        /usr/sbin/userdel gnarwl 2> /dev/null
        /usr/sbin/groupdel gnarwl 2> /dev/null
fi

%files
%defattr(644,root,root,755)
%doc README doc/{AUTHORS,BUGS,CHANGES,README.{pitfalls,security},TO-DO,USING,billiton.schema,example.ldif}
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %attr(640,root,gnarwl) %{_sysconfdir}/gnarwl.cfg
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl/db
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/.forward
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/blacklist.txt
%{_mandir}/man*/*

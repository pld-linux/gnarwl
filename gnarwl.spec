Summary:	Gnu Neat Auto Reply With LDAP
Summary(pl):	Gnu Neat Auto Reply With LDAP - autoresponder korzystaj�cy z LDAP
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
BuildRequires:	openldap-devel
BuildRequires:	groff
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnarwl is a email auto reply/vacation tool, intented to be used on
mailservers, on which users may not (nescessarily) have
systemaccoounts, but where userinformation is stored in LDAP.

%description -l pl
Gnarwl to system automatycznego odpowiadania na listy stworzony z
my�l� o serwerach poczty, na kt�rych u�ytkownicy nie musz� posiada�
prawdziwych kont systemowych, a informacje o u�ytkownikach znajduj�
si� w bazie LDAP.

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
if [ -n "`/usr/bin/getgid gnarwl`" ]; then
        if [ "`/usr/bin/getgid gnarwl`" != "26" ]; then
                echo "Error: group gnarwl doesn't have gid=26. Correct this before installing gnarwl" 1>&2
                exit 1
        fi
else
       /usr/sbin/groupadd -g 26 -r -f gnarwl
fi
if [ -n "`/bin/id -u gnarwl 2>/dev/null`" ]; then
       if [ "`/bin/id -u gnarwl`" != "26" ]; then
               echo "Error: user gnarwl doesn't have uid=26. Correct this before installing gnarwl"
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
%doc doc/{AUTHORS,FAQ,HISTORY,INSTALL,ISPEnv2.schema,ISPEnv.schema,LICENSE,README,README.upgrade,example.ldif}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %attr(640,root,gnarwl) %{_sysconfdir}/gnarwl.cfg
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl/block
%attr(755,gnarwl,gnarwl) %dir %{_var}/lib/gnarwl/bin
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/.forward
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/blacklist.db
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/badheaders.db
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/footer.txt 
%attr(640,gnarwl,gnarwl) %{_var}/lib/gnarwl/header.txt
%{_mandir}/man*/*

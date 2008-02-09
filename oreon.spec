
#TODO
# - see nagios-oreon.spec, merge upgrade there and cvs rm oreon.spec

# - use SMARTY from PLD

%define		INSTALL_DIR_NAGIOS	%{_libdir}/nagios
%define		NAGIOS_ETC		%{_sysconfdir}/nagios
%define		PLUGINS_DIR		Plugins
%define		INSTALL_DIR_NAGIOS	%{_libdir}/nagios
%define		NAGIOS_ETC		%{_sysconfdir}/nagios
%define		NAGIOS_PLUGIN		%{_libdir}/nagios/plugins
%define		INSTALL_DIR_OREON	%{_libdir}/%{name}
%define		RRD_PERL		%{perl_vendorarch}
%define		_webapps	/etc/webapps
%define		_webapp         oreon
%define		_webconfdir     %{_webapps}/%{_webapp}
%define		_appdir         %{_datadir}/%{_webapp}

Summary:	Oreon - provide enterprise monitoring based on Nagios core.
Name:		oreon
Version:	1.4
Release:	0.1
License:	Apache v2.0
Group:		Applications/WWW
Source0:	http://download.oreon-project.org/tgz/%{name}-%{version}.tar.gz
# Source0-md5:	31d1a2948fde3e4c0e922047c4633781
Source1:	http://download.oreon-project.org/patch/%{name}-patch-%{version}-5.tgz
# Source1-md5:	08290003e1fd93134578e40a69d785f1
URL:		http://www.oreon-project.org/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRequires: 	rpm-perlprov
Requires:       nagios-common
Requires:       perl-GD
Requires:	adodb >= 4.67-1.17
Requires:	crondaemon
Requires:	libgd2
Requires:	libpng
Requires:	net-snmp-utils
Requires:	php(gd)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(snmp)
Requires:	php(xml)
Requires:	php-cli
Requires:	rrdtool
Requires:	webserver
Requires:	webserver(php)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Oreon is a network supervision and monitoring tool, it is based upon
the most effective Open Source monitoring engine : Nagios.
Oreon provides a new frontend and new functionnalities to Nagios.

It ables you to be more efficient in your network monitoring, but also
allows you to make your supervision informations readable by a largest
range of users. Indeed, a non technical user can now use the Oreon/Nagios
couple to easily understand your network infrastructure thanks to charts
and graphical representations of the gathered informations.

Although, skilled users still have access to the technicals informations 
collected by Nagios.

%package setup
Summary:        Oreon setup package
Summary(pl.UTF-8):      Pakiet do wstępnej konfiguracji Oreona
Group:          Applications/WWW
Requires:       %{name} = %{version}-%{release}

%description setup
Install this package to configure initial Oreon installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalowć w celu wsępnej konfiguracji Oreona po
pierwszej instalacji. Potem należy go odinstalowć, jako że
pozostawienie plików instalacyjnych mołoby bć niebezpieczne.

%prep
%setup -q
find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

cat > apache.conf <<'EOF'
Alias /oreon %{_appdir}
<Directory %{_appdir}>
        Allow from all
        Options None
        AllowOverride None
</Directory>
EOF

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/nagios/plugins,%{_sysconfdir}{/rc.d/init.d,/nagios},%{_bindir},%{_datadir}/%{name},%{INSTALL_DIR_OREON}/{cron/reporting/api,ODS},%{_webconfdir}}

# install nagios  plugins
for fichier in %{PLUGINS_DIR}/src/*
	do
		if [ -d "$fichier" ]; then
                      echo ""
	else
		filename=`echo $fichier  | sed -e 's|.*\/\(.*\)|\1|'`
		echo "  -> $filename OK"
	`sed -e 's|@INSTALL_DIR_NAGIOS@|'"%{INSTALL_DIR_NAGIOS}"'|g' -e 's|@NAGIOS_ETC@|'"%{NAGIOS_ETC}"'|g' -e 's|@NAGIOS_PLUGINS@|'"%{NAGIOS_PLUGIN}"'|g' -e 's|@RRDTOOL_PERL_LIB@|'"%{RRD_PERL}"'|g' -e 's|@INSTALL_DIR_OREON@|'"%{INSTALL_DIR_OREON}"'|g'  "$fichier" > "$RPM_BUILD_ROOT%{NAGIOS_PLUGIN}/$filename"`
		fi
done
                
for fichier in %{PLUGINS_DIR}/src/traps/*
	do
		filename=`echo $fichier  | sed -e 's|.*\/\(.*\)|\1|'`
		echo "-> $filename"
	`sed -e 's|@INSTALL_DIR_NAGIOS@|'"%{INSTALL_DIR_NAGIOS}"'|g' -e 's|@NAGIOS_ETC@|'"%{NAGIOS_ETC}"'|g' -e 's|@NAGIOS_PLUGINS@|'"%{NAGIOS_PLUGIN}"'|g' -e 's|@RRDTOOL_PERL_LIB@|'"%{RRD_PERL}"'|g' -e 's|@INSTALL_DIR_OREON@|'"%{INSTALL_DIR_OREON}"'|g'  "$fichier" > "$RPM_BUILD_ROOT%{NAGIOS_PLUGIN}/$filename"`
done            

cp -rf www $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -rf doc $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -rf GPL_LIB $RPM_BUILD_ROOT%{_datadir}/%{name}

#"filesGeneration" "filesUpload"  "log" "rrd" "ODS" 

#instal ods
sed -e 's|@OREON_PATH@|'"%{INSTALL_DIR_OREON}"'|g' ODS/ods.pl > $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/ODS/ods.pl
sed -e 's|@OREON_PATH@|'"%{INSTALL_DIR_OREON}"'|g' -e 's|@NAGIOS_USER@|'"$NAGIOS_USER"'|g' -e 's|@NAGIOS_GROUP@|'"$NAGIOS_GROUP"'|g' ODS_SRC_ETC/ods > $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ods
sed -e 's|@OREON_PATH@|'"%{INSTALL_DIR_OREON}"'|g' cron/inventory_update.php > $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/cron/inventory_update.php
sed -e 's|@OREON_PATH@|'"%{INSTALL_DIR_OREON}"'|g' cron/reporting/ArchiveLogInDB.php > $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/cron/reporting/ArchiveLogInDB.php
sed -e 's|@OREON_PATH@|'"%{INSTALL_DIR_OREON}"'|g' cron/parsing_status.pl > $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/cron/parsing_status.pl
sed -e 's|@OREON_PATH@|'"%{INSTALL_DIR_OREON}"'|g' cron/parsing_log.pl > $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/cron/parsing_log.pl

install cron/delete*.pl $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/cron
install cron/reporting/api/* $RPM_BUILD_ROOT%{INSTALL_DIR_OREON}/cron/reporting/api
install apache.conf $RPM_BUILD_ROOT%{_webconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_webconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%postun

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG README cron/*README.txt cron/reporting/*README.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webconfdir}/httpd.conf
#%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%attr(755,root,root) %{_libdir}/nagios/plugins/*
#%attr(754,root,root) /etc/rc.d/init.d/%{name}
#%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%exclude %{_appdir}/www/install

%files setup
%defattr(644,root,root,755)
%{_appdir}/www/install

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

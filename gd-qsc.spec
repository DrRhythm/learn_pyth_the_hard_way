%if 0%{?rhel} == 6
%define  dist .el6
%define java java-1.7.0-openjdk
%define java_dev java-1.7.0-openjdk-devel
%service_path /sbin/service
%endif

%if 0%{?rhel} == 7
%define  dist .el7
%define java java-1.8.0-openjdk
%define java_dev java-1.8.0-openjdk-devel
%service_path /usr/sbin/service
%endif

Name            : gd-qsc
Summary         : QSC
Version:
Release        : 1%{?dist}
Group           : Applications/System
License:        : (c) 2015 Go Daddy, LLC
BuildArch       : noarch
BuildRoot       : %{_builddir}/%{name}-%{version}-root
Source0:        %{name}-%{version}.tar.gz

BuildRequires   : %{java}
BuildRequires   : %{java_dev}


%description
Main RPM that contains all the subpackages that make up GoDaddy's Quick Shopping Cart


%package admin
Summary		: Admin application for QSC
Group		: Applications/System

%description admin
Web application used by external customers to manage their Quick Shopping Cart store fronts.


%package storefront
Summary		: Storefront application for QSC
Group		: Applications/System

%description storefront
Web application that serves published storefronts for Quick Shopping Cart


%package storefront-preview
Summary		: Preview storefront application for QSC
Group		: Applications/System

%description storefront-preview
Web application that serves unpublished storefronts for Quick Shopping Cart

%package support
Summary		: Storefront application for QSC
Group		: Applications/System

%description support
Web application used internally to manage Quick Shopping Cart

%package static
Summary		: Static CDN content
Group		: Applications/System

%description static
Static content to be added to CDN

%prep
%setup -q
cat << EOF >> build.properties
EOF

%build
ant -Dservlet.jar.loc=%{_servlet_jar_loc} clean clean-source tar-build

%pre
${service_path} tomcat7 stop
exit 0

%install
mkdir -p $RPM_BUILD_ROOT/var/lib/tomcat/webapps
cp dist/mercury-admin.war $RPM_BUILD_ROOT/var/lib/tomcat/webapps/mercury-admin.war
cp dist/mercury-storefront.war $RPM_BUILD_ROOT/var/lib/tomcat/webapps/mercury-storefront.war
cp dist/mercury-storefront-preview.war $RPM_BUILD_ROOT/var/lib/tomcat/webapps/mercury-storefront-preview.war
cp dist/mercury-support.war $RPM_BUILD_ROOT/var/lib/tomcat/webapps/mercury-support.war

mkdir -p $RPM_BUILD_ROOT/usr/share/qsc/static
rm -rf dist/temp/temp-static/static/xml
cp -R dist/temp/temp-static/static/* $RPM_BUILD_ROOT/usr/share/qsc/static/

%post admin
%{__mv} /var/lib/tomcat/webapps/mercury-admin.war /var/lib/tomcat/webapps/ROOT.war
rm -rf /var/lib/tomcat/webapps/ROOT

%post storefront
%{__mv} /var/lib/tomcat/webapps/mercury-storefront.war /var/lib/tomcat/webapps/ROOT.war
rm -rf /var/lib/tomcat/webapps/ROOT

%post storefront-preview
%{__mv} /var/lib/tomcat/webapps/mercury-storefront-preview.war /var/lib/tomcat/webapps/preview.war
rm -rf /var/lib/tomcat/webapps/preview

%post support
%{__mv} /var/lib/tomcat/webapps/mercury-support.war /var/lib/tomcat/webapps/ROOT.war
rm -rf /var/lib/tomcat/webapps/ROOT

%files  admin
%defattr (770,tomcat7,root,770)
/var/lib/tomcat/webapps/mercury-admin.war

%files  storefront
%defattr (770,tomcat7,root,770)
/var/lib/tomcat/webapps/mercury-storefront.war

%files  storefront-preview
%defattr (770,tomcat7,root,770)
/var/lib/tomcat/webapps/mercury-storefront-preview.war

%files support
%defattr (770,tomcat7,root,770)
/var/lib/tomcat/webapps/mercury-support.war

%files static
%defattr (644,root,root,644)
/usr/share/qsc/static/*

%changelog
* Wed Jan 31 2018 wpaden <wp@godaddy.com>
- added variables for el7 and removed el5
-
* Wed Dec 09 2015 mjaniszewski <mjaniszewski@godaddy.com>
- updated to build for el6 and java7
-
* Tue Aug 25 2015 mjaniszewski <mjaniszewski@godaddy.com>
- Removed version number to allow dynamic injection.  Removed old tomcat dependency.
-
* Wed Aug 05 2015 Jenkins <linops@godaddy.com> - 2.8.6.111-1
- Updated to 2.8.6.111-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/111/
-
* Wed Aug 05 2015 Jenkins <linops@godaddy.com> - 2.8.6.110-1
- Updated to 2.8.6.110-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/110/
-
* Wed Jun 03 2015 Jenkins <linops@godaddy.com> - 2.8.6.109-2
- Updated to 2.8.6.109-2
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/109/
-
* Tue Jun 02 2015 Jenkins <linops@godaddy.com> - 2.8.6.108-1
- Updated to 2.8.6.108-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/108/
-
* Wed Dec 17 2014 Jenkins <linops@godaddy.com> - 2.8.6.107-1
- Updated to 2.8.6.107-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/107/
-
* Tue Dec 16 2014 Jenkins <linops@godaddy.com> - 2.8.6.106-1
- Updated to 2.8.6.106-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/106/
-
* Tue Sep 23 2014 Jenkins <linops@godaddy.com> - 2.8.6.99-1
- Updated to 2.8.6.99-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/99/
-
* Tue Sep 23 2014 Jenkins <linops@godaddy.com> - 2.8.6.98-1
- Updated to 2.8.6.98-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/98/
-
* Tue Sep 23 2014 Jenkins <linops@godaddy.com> - 2.8.6.97-1
- Updated to 2.8.6.97-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/97/
-
* Mon Sep 22 2014 Jenkins <linops@godaddy.com> - 2.8.6.96-1
- Updated to 2.8.6.96-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/96/
-
* Mon Sep 22 2014 Jenkins <linops@godaddy.com> - 2.8.6.95-1
- Updated to 2.8.6.95-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/95/
-
* Mon Sep 22 2014 Jenkins <linops@godaddy.com> - 2.8.6.94-1
- Updated to 2.8.6.94-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/94/
-
* Mon Sep 22 2014 Jenkins <linops@godaddy.com> - 2.8.6.93-1
- Updated to 2.8.6.93-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/93/
-
* Wed Jun 18 2014 Jenkins <linops@godaddy.com> - 2.8.6.91-1
- Updated to 2.8.6.91-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/91/
-
* Mon Jan 20 2014 Jenkins <linops@godaddy.com> - 2.8.6.90-1
- Updated to 2.8.6.90-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/90/
-
* Wed Jan 15 2014 Jenkins <linops@godaddy.com> - 2.8.6.89-1
- Updated to 2.8.6.89-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/89/
-
* Wed Jan 15 2014 Jenkins <linops@godaddy.com> - 2.8.6.88-1
- Updated to 2.8.6.88-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/88/
-
* Wed Jan 15 2014 Jenkins <linops@godaddy.com> - 2.8.6.87-1
- Updated to 2.8.6.87-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/87/
-
* Mon Nov 18 2013 Jenkins <linops@godaddy.com> - 2.8.6.86-1
- Updated to 2.8.6.86-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/86/
-
* Wed Nov 06 2013 Jenkins <linops@godaddy.com> - 2.8.6.85-1
- Updated to 2.8.6.85-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/85/
-
* Wed Nov 06 2013 Jenkins <linops@godaddy.com> - 2.8.6.83-1
- Updated to 2.8.6.83-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/83/
-
* Mon Nov 04 2013 Jenkins <linops@godaddy.com> - 2.8.6.82-1
- Updated to 2.8.6.82-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/82/
-
* Thu Oct 24 2013 Jenkins <linops@godaddy.com> - 2.8.6.81-1
- Updated to 2.8.6.81-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/81/
-
* Thu Oct 24 2013 Jenkins <linops@godaddy.com> - 2.8.6.80-1
- Updated to 2.8.6.80-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/80/
-
* Thu Oct 10 2013 Jenkins <linops@godaddy.com> - 2.8.6.79-1
- Updated to 2.8.6.79-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/79/
-
* Wed Oct 09 2013 Jenkins <linops@godaddy.com> - 2.8.6.78-1
- Updated to 2.8.6.78-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/78/
-
* Wed Sep 04 2013 Jenkins <linops@godaddy.com> - 2.8.6.77-1
- Updated to 2.8.6.77-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/77/
-
* Wed Aug 21 2013 Jenkins <linops@godaddy.com> - 2.8.6.76-1
- Updated to 2.8.6.76-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/76/
-
* Wed Jul 24 2013 Jenkins <linops@godaddy.com> - 2.8.6.75-1
- Updated to 2.8.6.75-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/75/
-
* Mon Jul 01 2013 Jenkins <linops@godaddy.com> - 2.8.5.74-1
- Updated to 2.8.5.74-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/74/
-
* Wed Jun 26 2013 Jenkins <linops@godaddy.com> - 2.8.5.73-1
- Updated to 2.8.5.73-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/73/
-
* Mon Jun 24 2013 Jenkins <linops@godaddy.com> - 2.8.5.72-1
- Updated to 2.8.5.72-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/72/
-
* Mon Jun 24 2013 Jenkins <linops@godaddy.com> - 2.8.5.71-1
- Updated to 2.8.5.71-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/71/
-
* Sun May 26 2013 Jenkins <linops@godaddy.com> - 2.8.4.70-1
- Updated to 2.8.4.70-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/70/
-
* Tue May 07 2013 Jenkins <linops@godaddy.com> - 2.8.3.69-1
- Updated to 2.8.3.69-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/69/
-
* Fri May 03 2013 Jenkins <linops@godaddy.com> - 2.8.3.68-1
- Updated to 2.8.3.68-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/68/
-
* Thu May 02 2013 Jenkins <linops@godaddy.com> - 2.8.3.64-1
- Updated to 2.8.3.64-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/64/
-
* Thu May 02 2013 Jenkins <linops@godaddy.com> - 2.8.3.63-1
- Updated to 2.8.3.63-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/63/
-
* Wed May 01 2013 Jenkins <linops@godaddy.com> - 2.8.3.62-1
- Updated to 2.8.3.62-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/62/
-
* Wed May 01 2013 Jenkins <linops@godaddy.com> - 2.8.3.61-1
- Updated to 2.8.3.61-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/61/
-
* Tue Apr 30 2013 Jenkins <linops@godaddy.com> - 2.8.3.60-1
- Updated to 2.8.3.60-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/60/
-
* Mon Apr 29 2013 Jenkins <linops@godaddy.com> - 2.8.3.59-1
- Updated to 2.8.3.59-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/59/
-
* Wed Apr 24 2013 Jenkins <linops@godaddy.com> - 2.8.2.58-1
- Updated to 2.8.2.58-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/58/
-
* Wed Apr 24 2013 Jenkins <linops@godaddy.com> - 2.8.2.57-1
- Updated to 2.8.2.57-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/57/
-
* Wed Apr 24 2013 Jenkins <linops@godaddy.com> - 2.8.2.56-1
- Updated to 2.8.2.56-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/56/
-
* Mon Apr 22 2013 Jenkins <linops@godaddy.com> - 2.8.2.55-1
- Updated to 2.8.2.55-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/55/
-
* Mon Apr 22 2013 Jenkins <linops@godaddy.com> - 2.8.2.54-1
- Updated to 2.8.2.54-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/54/
-
* Wed Apr 17 2013 Jenkins <linops@godaddy.com> - 2.8.2.53-1
- Updated to 2.8.2.53-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/53/
-
* Tue Apr 16 2013 Jenkins <linops@godaddy.com> - 2.8.2.52-1
- Updated to 2.8.2.52-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/52/
-
* Mon Apr 15 2013 Jenkins <linops@godaddy.com> - 2.8.2.51-1
- Updated to 2.8.2.51-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/51/
-
* Fri Apr 12 2013 Jenkins <linops@godaddy.com> - 2.8.2.50-1
- Updated to 2.8.2.50-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/50/
-
* Wed Apr 10 2013 Jenkins <linops@godaddy.com> - 2.8.2.49-1
- Updated to 2.8.2.49-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/49/
-
* Tue Apr 02 2013 Jenkins <linops@godaddy.com> - 2.8.1.48-1
- Updated to 2.8.1.48-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/48/
-
* Sun Mar 31 2013 Jenkins <linops@godaddy.com> - 2.8.1.47-1
- Updated to 2.8.1.47-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/47/
-
* Fri Mar 29 2013 Jenkins <linops@godaddy.com> - 2.8.1.46-1
- Updated to 2.8.1.46-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/46/
-
* Thu Mar 28 2013 Jenkins <linops@godaddy.com> - 2.8.1.44-1
- Updated to 2.8.1.44-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/44/
-
* Mon Mar 18 2013 Jenkins <linops@godaddy.com> - 2.8.0.43-1
- Updated to 2.8.0.43-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/43/
-
* Fri Mar 15 2013 Jenkins <linops@godaddy.com> - 2.8.0.42-1
- Updated to 2.8.0.42-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/42/
-
* Wed Mar 06 2013 Jenkins <linops@godaddy.com> - 2.8.0.41-1
- Updated to 2.8.0.41-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/41/
-
* Wed Feb 27 2013 Jenkins <linops@godaddy.com> - 2.7.9.40-1
- Updated to 2.7.9.40-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/40/
-
* Thu Feb 21 2013 Jenkins <linops@godaddy.com> - 2.7.9.39-1
- Updated to 2.7.9.39-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/39/
-
* Thu Feb 21 2013 David Johansen <djohansen@godaddy.com> - 2.7.9.38-1
- Added a tomcat_vers macro, so that vers is not hardcoded
-
* Mon Jan 28 2013 Jenkins <linops@godaddy.com> - 2.7.8.36-1
- Updated to 2.7.8.36-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/36/
-
* Wed Jan 16 2013 Jenkins <linops@godaddy.com> - 2.7.8.35-1
- Updated to 2.7.8.35-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/35/
-
* Mon Jan 14 2013 Jenkins <linops@godaddy.com> - 2.7.8.34-1
- Updated to 2.7.8.34-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/34/
-
* Mon Dec 03 2012 Jenkins <linops@godaddy.com> - 2.7.7.33-1
- Updated to 2.7.7.33-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/33/
-
* Thu Nov 15 2012 Jenkins <linops@godaddy.com> - 2.7.6.32-1
- Updated to 2.7.6.32-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/32/
-
* Thu Nov 15 2012 Jenkins <linops@godaddy.com> - 2.7.6.31-1
- Updated to 2.7.6.31-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/31/
-
* Wed Nov 14 2012 Jenkins <linops@godaddy.com> - 2.7.6a.30-1
- Updated to 2.7.6a.30-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/30/
-
* Thu Nov 08 2012 Jenkins <linops@godaddy.com> - 2.7.6.29-1
- Updated to 2.7.6.29-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/29/
-
* Wed Nov 07 2012 Jenkins <linops@godaddy.com> - 2.7.6.28-1
- Updated to 2.7.6.28-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/28/
-
* Wed Nov 07 2012 Jenkins <linops@godaddy.com> - 2.7.6.27-1.el5
- Updated to 2.7.6.27-1.el5
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/27/
-
* Wed Nov 07 2012 Jenkins <linops@godaddy.com> - 2.7.6.26-1.el5
- Updated to 2.7.6.26-1.el5
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/26/
-
* Tue Nov 06 2012 Jenkins <linops@godaddy.com> - 2.7.6.10-1
- Updated to 2.7.6.10-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/10/
-
* Fri Oct 19 2012 Jenkins <linops@godaddy.com> - 2.7.5.9-1
- Updated to 2.7.5.9-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/9/
-
* Fri Oct 19 2012 Jenkins <linops@godaddy.com> - 2.7.4.8-1
- Updated to 2.7.4.8-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/8/
-
* Fri Oct 19 2012 Jenkins <linops@godaddy.com> - 2.7.4.7-1
- Updated to 2.7.4.7-1
- http://jenkins.intranet.gdg/job/gd-qsc-staging-deployment/7/
-
* Fri Sep 21 2012 -7000 David Johansen <djohansen@godddy.com> - 2.7.4-2
- Changing ROOT.war to preview.war for preview app

* Fri Sep 21 2012 -7000 David Johansen <djohansen@godddy.com> - 2.7.4-1
- Building with koji from here on.

    API Training Shop Blog About

    © 2018 GitHub, Inc. Help Support

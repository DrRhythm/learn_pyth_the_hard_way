#Define a build version including the build number, to avoid issues when rebuilding the same tag
BUILD_VERSION=${VERSION_TAG}.${BUILD_NUMBER}
BUILD_DIR=gd-qsc-${BUILD_VERSION}
export ANT_HOME=/usr/local/build/ant/apache-ant-1.8.4

#Clone QSC
git clone git@github.secureserver.net:QSC/ecommerce2 ${BUILD_DIR}

#Switch to the version tag.
cd ${BUILD_DIR}
git checkout refs/tags/${VERSION_TAG}
cd ..

#Create source tarball
tar zcf gd-qsc-${BUILD_VERSION}.tar.gz ${BUILD_DIR}/.

#Set up RPM paths
mkdir -p ./{BUILD,RPMS,SOURCES,SPECS,SRPMS}

#Copy source tarball and spec into their respective locations
cp  gd-qsc*.tar.gz ./SOURCES
cp ./${BUILD_DIR}/conf/gd-qsc.spec.noarch ./SPECS/gd-qsc.spec

#Update version number in gd-qsc.spec
sed -ie "s/\(Version:\).*/\1 $BUILD_VERSION/" ./SPECS/gd-qsc.spec

#Build SRPM
rpmbuild --define '_topdir '`pwd` --define '_servlet_jar_loc /usr/local/build/servlet_jars' -bs ./SPECS/gd-qsc.spec

#Build RPM
rpmbuild --define '_topdir '`pwd` --define '_servlet_jar_loc /usr/local/build/servlet_jars' --rebuild ./SRPMS/gd-qsc-$BUILD_VERSION-1.el7.src.rpm

RPMS=$( find ./*RPMS/ -name "*.rpm" )
for rpm in ${RPMS}; do
  curl -u ${ci_service_account_user}:${ci_service_account_password} -X PUT -F packages=@$rpm https://yum.secureserver.net/api/v0.1/repos/dev/centos/7/x86_64/qsc/upload
done

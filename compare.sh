stdout=$(sudo -u release /usr/sbin/lsof | grep java | wc -l)

if [ $stdout -lt 4000 ]
then
  echo "Number of Open Files OK"
   exit 0
else
  echo "Too many files open; restarting Thrift"
   exit 1
fi

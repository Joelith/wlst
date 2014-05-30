WL_HOME='/oracle/product/middleware/wlserver_10.3'
DOMAIN='osb_domain'
DOMAIN_PATH='/oracle/config/domains/osb_domain'
# Check if domain is built

# Start Node Manager
echo "Checking if node manager is running"
nodePid=`/bin/ps -eo pid,cmd | /bin/grep weblogic.NodeManager | /bin/grep -v grep | awk '{print $1}'`

if [ ${nodePid} ]
then
	echo "The NodeManager is already running."
else
	echo "NodeManager not running. Start NodeManager"
	$WL_HOME/common/bin/wlst.sh <<-EOF
startNodeManager(NodeManagerHome='/oracle/product/middleware/wlserver_10.3/common/nodemanager')
EOF
	nodePid=`/bin/ps -eo pid,cmd | /bin/grep weblogic.NodeManager | /bin/grep -v grep | awk '{print $1}'`
	if [ ${nodePid} ]
	then
		echo "NodeManager started"
	else
		echo "Error starting NodeManager!"
		exit
	fi
fi

# Start WebLogic
echo "Checking if Admin Server is running for ${DOMAIN}"
pid=`/bin/ps -eo pid,cmd | /bin/grep -i weblogic.AdminServer | /bin/grep -v grep | awk '{print $1}'`

if [ ${pid} ]
then
	echo "The Admin Server is already running"
else 
	echo "Admin server not running. Starting Admin Server"
	$WL_HOME/common/bin/wlst.sh <<-EOF
nmConnect('weblogic', 'welcome1', 'localhost', 5556, '$DOMAIN', '$DOMAIN_PATH', 'plain')
nmStart('AdminServer')
nmServerStatus('AdminServer')
nmDisconnect()
EOF
fi
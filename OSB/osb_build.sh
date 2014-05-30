source osb.properties
# Check if domain is built
if [ -e ${DOMAIN_HOME} ]
then
	echo "Domain exists"
else
	echo "$DOMAIN_HOME does not exist. Rebuilding domain"
	$WL_HOME/common/bin/wlst.sh build_domain.py
fi

# Start Node Manager
echo "Checking if node manager is running"
nodePid=`/bin/ps -eo pid,cmd | /bin/grep weblogic.NodeManager | /bin/grep -v grep | awk '{print $1}'`

if [ ${nodePid} ]
then
	echo "The NodeManager is already running."
else
	echo "NodeManager not running. Start NodeManager"
	$WL_HOME/common/bin/wlst.sh <<-EOF
startNodeManager(NodeManagerHome='$WL_HOME/common/nodemanager')
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
pid=`/bin/ps -eo pid,cmd | /bin/grep -i weblogic.Name=$ADMIN_SERVER | /bin/grep -v grep | awk '{print $1}'`

if [ ${pid} ]
then
	echo "The Admin Server is already running"
else 
	echo "Admin server not running. Starting Admin Server"
	$WL_HOME/common/bin/wlst.sh <<-EOF
nmConnect('$WEBLOGIC_USER', '$WEBLOGIC_PASSWORD', '$LISTEN_ADDRESS', '$NODE_MANAGER_PORT', '$DOMAIN', '$DOMAIN_HOME', 'plain')
nmStart('$ADMIN_SERVER')
nmServerStatus('$ADMIN_SERVER')
nmDisconnect()
EOF
fi
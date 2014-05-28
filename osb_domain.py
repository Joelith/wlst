#!/usr/bin/env /oracle/product/middleware/Oracle_OSB1/common/bin/wlst.sh

# ===============
#  Variable Defs
# ===============

ADMIN_SERVER 				        = 'AdminServer'
ADMIN_SERVER_PORT		        = 7001
DATABASE 					          = 'localhost:1521:XE'
DOMAIN 						          = 'osb_domain'
DOMAIN_HOME 				        = '/oracle/config/domains/' + DOMAIN
LISTEN_ADDRESS 				      = 'localhost'
MACHINE 					          = 'machine1'
MANAGED_SERVER 				      = 'osb_server1'
MANAGED_SERVER_PORT			    = 7003
MDS_USER 					          = 'DEV_MDS'
MDS_PASSWORD 				        = 'welcome1'
MW_HOME						          = '/oracle/product/middleware'
NODE_MANAGER 				        = 'nodemgr'
NODE_MANAGER_LISTEN_ADDRESS = 'localhost'
NODE_MANAGER_PASSWORD		    = 'welcome2'
NODE_MANAGER_PORT 			    = 5556
OSB_HOME					          = '/oracle/product/middleware/Oracle_OSB1'
SOAINFRA_USER 				      = 'DEV_SOAINFRA'
SOAINFRA_PASSWORD 			    = 'welcome1'
WEBLOGIC_PASSWORD			      = 'welcome1'
WL_HOME						          = '/oracle/product/middleware/wlserver_10.3'

###############################################################################
# Create the domain
###############################################################################
print('Creating the domain')

readTemplate(WL_HOME + '/common/templates/domains/wls.jar')
cd('/Security/base_domain/User/weblogic')
cmo.setPassword(WEBLOGIC_PASSWORD)
writeDomain(DOMAIN_HOME)
closeTemplate()

readDomain(DOMAIN_HOME)
addTemplate(OSB_HOME + '/common/templates/applications/wlsb.jar')
addTemplate(OSB_HOME + '/common/templates/applications/wlsb_owsm.jar')
addTemplate(MW_HOME + '/oracle_common/common/templates/applications/oracle.em_11_1_1_0_0_template.jar')

###############################################################################
# wlsbjmsrpDataSource
###############################################################################
print('Configuring Data sources')             
cd('/')
delete('wlsbjmsrpDataSource','JDBCSystemResource')
 
create('wlsbjmsrpDataSource', 'JDBCSystemResource')
cd('/JDBCSystemResource/wlsbjmsrpDataSource')
set('DescriptorFileName','jdbc/wlsbjmsrpDataSource-jdbc.xml')
set('Target',ADMIN_SERVER +  ',' + MANAGED_SERVER)
cd('/JDBCSystemResource/wlsbjmsrpDataSource/JdbcResource/wlsbjmsrpDataSource')
cmo.setName('wlsbjmsrpDataSource')
 
cd('/JDBCSystemResource/wlsbjmsrpDataSource/JdbcResource/wlsbjmsrpDataSource')
create('myJdbcDataSourceParams','JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', java.lang.String('wlsbjmsrpDataSource'))
set('GlobalTransactionsProtocol', java.lang.String('None'))
 
cd('/JDBCSystemResource/wlsbjmsrpDataSource/JdbcResource/wlsbjmsrpDataSource')
create('myJdbcDriverParams','JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('DriverName','oracle.jdbc.OracleDriver')
set('URL','jdbc:oracle:thin:@' + DATABASE)
set('PasswordEncrypted', SOAINFRA_PASSWORD)
set('UseXADataSourceInterface', 'false')
 
create('myProperties','Properties')
cd('Properties/NO_NAME_0')
create('user','Property')
cd('Property')
cd('user')
set('Value', SOAINFRA_USER)
 
cd('/JDBCSystemResource/wlsbjmsrpDataSource/JdbcResource/wlsbjmsrpDataSource')
create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/NO_NAME_0')
set('CapacityIncrement',1)
set('InitialCapacity',5)
set('MaxCapacity',25)
set('TestTableName','SQL SELECT 1 FROM DUAL')

###############################################################################
# mds-owsm
###############################################################################
 
cd('/')
delete('mds-owsm','JDBCSystemResource')
 
create('mds-owsm', 'JDBCSystemResource')
cd('/JDBCSystemResource/mds-owsm')
set('DescriptorFileName','jdbc/mds-owsm-jdbc.xml')
set('Target',ADMIN_SERVER +  ',' + MANAGED_SERVER)
cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm')
cmo.setName('mds-owsm')
 
cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm')
create('myJdbcDataSourceParams','JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', java.lang.String('jdbc/mds/owsm'))
set('GlobalTransactionsProtocol', java.lang.String('None'))
 
cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm')
create('myJdbcDriverParams','JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('DriverName','oracle.jdbc.OracleDriver')
set('URL','jdbc:oracle:thin:@' + DATABASE)
set('PasswordEncrypted', MDS_PASSWORD)
set('UseXADataSourceInterface', 'false')
 
create('myProperties','Properties')
cd('Properties/NO_NAME_0')
create('user','Property')
cd('Property')
cd('user')
set('Value', MDS_USER)
 
cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm')
create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/NO_NAME_0')
set('CapacityIncrement',1)
set('InitialCapacity',5)
set('MaxCapacity',25)
set('TestTableName','SQL SELECT 1 FROM DUAL')

###############################################################################
# Misc domain settings
###############################################################################
 
cd ('/')
cmo.setConfigBackupEnabled(True)
cmo.setArchiveConfigurationCount(25)
 
cd('/Server/' + ADMIN_SERVER)
cmo.setListenAddress(LISTEN_ADDRESS)
cmo.setListenPort(ADMIN_SERVER_PORT)
 
cd('/Server/' + MANAGED_SERVER)
cmo.setListenAddress(LISTEN_ADDRESS)
cmo.setListenPort(MANAGED_SERVER_PORT)
 
cd ('/SecurityConfiguration/' + DOMAIN)
cmo.setNodeManagerUsername(NODE_MANAGER)
cmo.setNodeManagerPasswordEncrypted(NODE_MANAGER_PASSWORD)

###############################################################################
# Create machines
###############################################################################
print('Creating machines')
cd ('/')
create(MACHINE, 'UnixMachine')
cd('/Machines/' + MACHINE)
create(MACHINE, 'NodeManager')
cd('NodeManager/' + MACHINE)
set('NMType', 'Plain')
set('ListenAddress', NODE_MANAGER_LISTEN_ADDRESS)
set('ListenPort', NODE_MANAGER_PORT)
 
cd('/Server/' + ADMIN_SERVER)
set('Machine',MACHINE)
 
cd('/Server/' + MANAGED_SERVER)
set('Machine',MACHINE)

updateDomain()
closeDomain()

#!/usr/bin/env /oracle/product/middleware/Oracle_OSB1/common/bin/wlst.sh
from java.util import Properties
from java.io import FileInputStream

# ===============
#  Variable Defs
# ===============

prop = Properties()
prop.load(FileInputStream('osb.properties'))

ADMIN_SERVER 				= prop.getProperty('ADMIN_SERVER')
ADMIN_SERVER_PORT		 	= int(prop.getProperty('ADMIN_SERVER_PORT'))
DATABASE 					= prop.getProperty('DATABASE')
DOMAIN 						= prop.getProperty('DOMAIN')
DOMAIN_HOME 				= prop.getProperty('DOMAIN_HOME')
LISTEN_ADDRESS 				= prop.getProperty('LISTEN_ADDRESS')
MACHINE 					= prop.getProperty('MACHINE')
MANAGED_SERVER 				= prop.getProperty('MANAGED_SERVER')
MANAGED_SERVER_PORT			= int(prop.getProperty('MANAGED_SERVER_PORT'))
MDS_USER 					= prop.getProperty('MDS_USER')
MDS_PASSWORD 				= prop.getProperty('MDS_PASSWORD')
MW_HOME						= prop.getProperty('MW_HOME')
NODE_MANAGER 				= prop.getProperty('NODE_MANAGER')
NODE_MANAGER_LISTEN_ADDRESS = prop.getProperty('NODE_MANAGER_LISTEN_ADDRESS')
NODE_MANAGER_PASSWORD		= prop.getProperty('NODE_MANAGER_PASSWORD')
NODE_MANAGER_PORT 			= int(prop.getProperty('NODE_MANAGER_PORT'))
OSB_HOME					= prop.getProperty('OSB_HOME')
SOAINFRA_USER 				= prop.getProperty('SOAINFRA_USER')
SOAINFRA_PASSWORD 			= prop.getProperty('SOAINFRA_PASSWORD')
WEBLOGIC_PASSWORD			= prop.getProperty('WEBLOGIC_PASSWORD')
WL_HOME						= prop.getProperty('WL_HOME')

###############################################################################
# Create the domain
###############################################################################

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

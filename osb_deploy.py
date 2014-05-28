import wlstModule
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from java.util import HashMap
from java.util import ArrayList
from java.util import HashSet

importJar = 'dvs.jar'
adminUrl = 'localhost:8001'

def importToDomain():
	try:
		sessionMBean = None
		alsbConfigurationMBean = None

		connect('weblogic', 'welcome1', 't3://' + adminUrl)
		domainRuntime()
		print 'Starting import of: ', importJar, ' on domain', adminUrl
		theBytes = readBinaryFile(importJar)

		sessionName = createSessionName()
		sessionMBean = getSessionMBean(sessionName)
		print 'Created session: ', sessionName

		alsbConfigurationMBean = findService(String(ALSBConfigurationMBean.NAME + ".").concat(sessionName), ALSBConfigurationMBean.TYPE)
		print "ALSBConfigurationMBean found", alsbConfigurationMBean

		alsbConfigurationMBean.uploadJarFile(theBytes)
		print 'Jar uploaded'

		alsbJarInfo = alsbConfigurationMBean.getImportJarInfo()
		alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
		alsbImportPlan.setPassphrase('osb')
		alsbImportPlan.setPreserveExistingEnvValues(true)
		alsbImportPlan.setPreserveExistingOperationalValues(false)

		operationMap = HashMap()
		operationMap = alsbImportPlan.getOperations()
		print 'Current importPlan'
		printOpMap(operationMap)

		importResult = alsbConfigurationMBean.importUploaded(alsbImportPlan)
		printDiagMap(importResult.getImportDiagnostics())

		if importResult.getFailed().isEmpty() == false:
			print 'One or more resources could not be imported properly'
			raise

		sessionMBean.activateSession(sessionName, "ALSBImport Operation Completed Succesfully")
		print "Deployment of: " + importJar + " successful"
	except:
		if sessionMBean != None:
			sessionMBean.discardSession(sessionName)
		raise

def printOpMap(map):
	set = map.entrySet()
	for entry in set:
		op = entry.getValue()
		print op.getOperation(),
		ref = entry.getKey()
		print ref
	print

def printDiagMap(map):
	set = map.entrySet()
	for entry in set:
		diag = entry.getValue().toString()
		print diag
	print

def readBinaryFile(fileName):
    file = open(fileName, 'rb')
    bytes = file.read()
    return bytes

def createSessionName():
	sessionName = String("OSBImportScript-"+
						  Long(System.currentTimeMillis()).toString())
	return sessionName

def getSessionMBean(sessionName):
	# obtain session management mbean to create a session.
	# This mbean instance can be used more than once to
	# create/discard/commit many sessions
	sessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)
	print sessionMBean	
	# create a session
	sessionMBean.createSession(sessionName)

	return sessionMBean

try:
	importToDomain()
except:
	dumpStack()
	raise
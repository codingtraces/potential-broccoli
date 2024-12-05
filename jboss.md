If you’re on Windows and looking for an easy alternative to install JBoss EAP 7.2.6, follow these simple steps:

Option 1: Use PowerShell to Automate Installation

	1.	Download JBoss EAP
	•	Use PowerShell to download the JBoss EAP 7.2.6 ZIP file:

$url = "https://developers.redhat.com/content-gateway/file/jboss-eap-7.2.6.zip"
$destination = "C:\jboss-eap-7.2.6.zip"
Invoke-WebRequest -Uri $url -OutFile $destination


	2.	Extract the ZIP File
	•	Extract the ZIP file to a directory (e.g., C:\jboss-eap-7.2.6):

Expand-Archive -Path "C:\jboss-eap-7.2.6.zip" -DestinationPath "C:\jboss-eap-7.2.6"


	3.	Set JBOSS_HOME Environment Variable
	•	Add the JBOSS_HOME environment variable:

[System.Environment]::SetEnvironmentVariable("JBOSS_HOME", "C:\jboss-eap-7.2.6", [System.EnvironmentVariableTarget]::Machine)


	4.	Add JBoss to the PATH
	•	Update the PATH environment variable:

$path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
$jbossBinPath = "C:\jboss-eap-7.2.6\bin"
if (-not ($path -like "*$jbossBinPath*")) {
    [System.Environment]::SetEnvironmentVariable("Path", "$path;$jbossBinPath", [System.EnvironmentVariableTarget]::Machine)
}


	5.	Verify the Installation
	•	Open a new PowerShell window and type:

echo $env:JBOSS_HOME

It should display C:\jboss-eap-7.2.6.

	6.	Start JBoss
	•	Navigate to the JBoss bin directory:

cd C:\jboss-eap-7.2.6\bin
.\standalone.bat


	•	Once started, access the management console at:

http://localhost:9990

Option 2: Manual Steps

	1.	Download the ZIP File:
	•	Go to JBoss EAP Download Page and download the file manually.
	2.	Extract and Set Environment Variables:
	•	Extract the ZIP file to a folder like C:\jboss-eap-7.2.6.
	•	Open System Properties > Advanced > Environment Variables.
	•	Add a new System Variable:
	•	Name: JBOSS_HOME
	•	Value: C:\jboss-eap-7.2.6
	•	Add C:\jboss-eap-7.2.6\bin to the Path variable in System Variables.
	3.	Start the Server:
	•	Open Command Prompt, navigate to the bin folder, and run:

standalone.bat

Option 3: Use Chocolatey (Alternative Package)

If you are okay with using WildFly (the upstream version of JBoss):
	1.	Install Chocolatey:
	•	Open PowerShell as Administrator and run:

Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))


	2.	Install WildFly:
	•	Run the command:

choco install wildfly --version=26.1.2


	•	Replace the version with your preferred WildFly version.

	3.	Start WildFly:
	•	Navigate to the installation folder (e.g., C:\ProgramData\chocolatey\lib\wildfly\tools\wildfly).
	•	Run:

standalone.bat

Conclusion

For JBoss EAP 7.2.6, you’ll likely need to use the manual or PowerShell method unless WildFly (via Chocolatey) meets your needs. If you have additional questions, let me know!
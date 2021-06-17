# TFE-AutoUpdate-TF
This script can be used to automatically update Terraform Enterprise to include the latest release of Terraform. 

When executed, the script does the following: 
1. query checkpoint api for the most recent version of Terraform available
2. query TFE for a list of currently installed versions 
3. if the installed versions do not include the latest available:
   1. obtain SHA256 sum for desired binary
   2. command TFE to download and install the newest available version

## TO-DOs
- update admin token to be read as ENV variable
- optimize method of parsing SHA256 checksum
- convert to lambda function
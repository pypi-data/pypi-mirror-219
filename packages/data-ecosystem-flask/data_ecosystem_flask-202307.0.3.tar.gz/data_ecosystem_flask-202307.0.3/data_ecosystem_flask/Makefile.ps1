# This is a PowerShell script equivalent of a Makefile
# To run a target from PowerShell, use the following syntax:
# .\Makefile.ps1 'flask-create-OCIO-PADE-DEV'
# Logout of ZScaler VPN before running this script
# .\Makefile.ps1 'setup-key-vault-dev'

param($Target)

if ($Target -eq 'flask-create-OCIO-PADE-DEV') {

    & "$env:USERPROFILE\.local\bin\virtualenvwrapper.bat"
    & ".\OCIO_PADE_DEV\Scripts\activate"
    Invoke-WebRequest "https://install.python-poetry.org" -OutFile "install.py"
    python "install.py"
    Copy-Item "$env:USERPROFILE\.local\bin\poetry" ".\OCIO_PADE_DEV\Scripts\poetry"
    poetry update
    poetry install
}

if ($Target -eq 'setup-key-vault-dev') {

    az login
    az keyvault set-policy --name "az_kv_key_vault_name" --resource-group "OCIO-DAV-DEV" --spn "140ec12a-3b3d-4138-8294-57d6c0e82dd6" --secret-permissions get
}

 
function Install-Requirements {
    param (
        [string]$pipPath,
        [string]$requirementsPath
    )

    Write-Host "Installing requirements from requirements.txt..."
    & $pipPath install -r $requirementsPath
    if ($?) {
        Write-Host "Requirements installed successfully."
    } else {
        Write-Host "Failed to install requirements."
    }
}

function New-VirtualEnvironment {
    param (
        [string]$venvPath,
        [string]$pipPath,
        [string]$requirementsPath
    )

    Write-Host "Creating virtual environment..."
    & python -m venv $venvPath
    if ($?) {
        Write-Host "Virtual environment created successfully."
        Install-Requirements -pipPath $pipPath -requirementsPath $requirementsPath
    } else {
        Write-Host "Failed to create virtual environment."
    }
}

function Find-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python") {
            Write-Host "Python is installed. Version: $pythonVersion"
            return $true
        } else {
            Write-Host "Python is not installed. Please install Python."
            return $false
        }
    } catch {
        Write-Host "Python is not installed. Please install Python from https://www.python.org/downloads/"
        return $false
    }
}

# Check if Python is installed
if (-not (Find-PythonInstallation)) {
    return
}

# Get the current script's directory
$scriptDirectory = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Define the path of the .venv folder and the python.exe within it
$venvPath = Join-Path -Path $scriptDirectory -ChildPath ".venv"
$pythonExePath = Join-Path -Path $venvPath -ChildPath "Scripts\python.exe"
$pipPath = Join-Path -Path $venvPath -ChildPath "Scripts\pip.exe"
$requirementsPath = Join-Path -Path $scriptDirectory -ChildPath "requirements.txt"

# Check if the .venv folder exists and Scripts/python.exe exists within the .venv folder
if (Test-Path -Path $pythonExePath) {
    Write-Host ".venv folder and Scripts/python.exe exist."

    # Check if requirements.txt exists
    if (Test-Path -Path $requirementsPath) {
        Install-Requirements -pipPath $pipPath -requirementsPath $requirementsPath
    } else {
        Write-Host "requirements.txt not found."
    }
} else {
    New-VirtualEnvironment -venvPath $venvPath -pipPath $pipPath -requirementsPath $requirementsPath
}

# clear the screen
Clear-Host

& python .\__init__.py

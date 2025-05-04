# =========================
# deploy-main.ps1
# =========================

param (
    [string]$subscriptionId = "8ce77fc4-6e27-415d-bcce-2c7a8f724348",
    [string]$resourceGroup = "rg-pdf-app",
    [string]$location = "westeurope"
)

$ErrorActionPreference = "Stop"

Write-Host "Setting subscription to $subscriptionId..."
az account set --subscription $subscriptionId

# Create resource group if it doesn't exist
Write-Host "Checking if resource group '$resourceGroup' exists..."
$rgExists = az group exists --name $resourceGroup | ConvertFrom-Json
if (-not $rgExists) {
    Write-Host "Creating resource group: $resourceGroup in $location..."
    az group create --name $resourceGroup --location $location | Out-Null
} else {
    Write-Host "Resource group already exists."
}

# Deploy Bicep template
Write-Host "Starting Bicep deployment..."
az deployment group create `
  --resource-group $resourceGroup `
  --template-file ./main.bicep `
  --parameters location=$location `
  --confirm-with-what-if `
  --only-show-errors

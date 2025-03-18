param (
    [string]$subscriptionId = "8ce77fc4-6e27-415d-bcce-2c7a8f724348",
    [string]$resourceGroup = "rg-pdf-audio",
    [string]$location = "westeurope"
)

# Login and select subscription
az account set --subscription $subscriptionId

# Create resource group if not exists
az group create --name $resourceGroup --location $location

# Deploy Bicep file
az deployment group create `
    --resource-group $resourceGroup `
    --template-file ./main.bicep `
    --parameters location=$location

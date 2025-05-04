@description('The Azure region to deploy resources')
param location string = resourceGroup().location

@description('The name of the Web App')
param appServiceName string = 'pdf-app-service'

@description('The name of the existing App Service Plan')
param appServicePlanName string = 'plan-pdf-audio'

@description('The resource group where the App Service Plan exists')
param aspResourceGroupName string = 'appserviceplan-dev'

@description('The Docker image to deploy')
param dockerImage string = 'ghcr.io/yourname/pdf-audio-app:latest'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' existing = {
  name: appServicePlanName
  scope: resourceGroup(aspResourceGroupName)
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://ghcr.io'
        }
      ]
    }
    httpsOnly: true
  }
  kind: 'app,linux,container'
}

param location string = 'westeurope'
param appServicePlanName string = 'plan-pdf-audio'
param appName string = 'app-pdf-audio'
param dockerImage string = 'ghcr.io/library/pdf-audio-converter:latest' // Replace with your image if needed

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: false
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
    }
    httpsOnly: true
  }
}

module.exports = {
    devServer: {
      host: '0.0.0.0',        // allow external access from Codespaces
      port: 8080,
      https: false,           // let GitHub Codespaces handle HTTPS
      client: {
        webSocketURL: {
          protocol: 'wss',    // secure websocket
          hostname: 'studious-tribble-wprp65v6749h9p54-8080.app.github.dev', // your Codespace URL
          port: 443,
          pathname: '/ws',
        }
      }
    }
  }
  
const os = require('os');
const ip = require('ip');

function getLocalIps() {
    const localIps = [];

    const hostIp = ip.address();
    console.log(`My IP address is: ${hostIp}`);
    localIps.push(hostIp)
    
    return localIps
}

// Exemplo de uso
const ipsLocais = getLocalIps();
console.log('Endereços IP locais:', ipsLocais);

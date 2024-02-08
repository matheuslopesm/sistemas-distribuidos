const devicesIds = [];
const devices = [];

async function ping(ip) {
    try {
        const response = await fetch(`http://${ip}`, { method: 'HEAD' });
        if (response.ok) {
            return true; // IP está acessível
        } else {
            return false; // Falha ao acessar o IP
        }
    } catch (error) {
        return false; // Erro ao tentar acessar o IP
    }
}

async function checkDevicesAvailability() {
    for (let ip_machine = 1; ip_machine <= 10; ip_machine++) {
        const ip = `172.16.100.${ip_machine}`;
        const isReachable = await ping(ip);
        if (isReachable) {
            devicesIds.push(ip_machine);
            devices.push({ "ID": ip_machine, "IP": ip });
        }
    }

    console.log("Dispositivos acessíveis:", devices);
}

checkDevicesAvailability();

var ping = require('ping');

const devices = [];
const hosts = [];

for (let ip_machine = 3; ip_machine < 12; ip_machine++) {
    const ip = `172.16.100.${ip_machine}`;
    devices.push(ip);
}

async function checkHosts() {
    for (const device of devices) {
        try {
            const res = await ping.promise.probe(device);
            if (res.alive) {
                hosts.push(device);
            }
        } catch (error) {
            console.error('Error occurred while pinging:', error);
        }
    }
    console.log(hosts);
}

checkHosts();
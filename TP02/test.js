const ping = require('ping');

const devicesIds = [];
const devices = [];

for (let ip_machine = 1; ip_machine < 10; ip_machine++) {
    const ip = `172.16.100.${ip_machine}`;

    ping.promise.probe(ip)
        .then((res) => {
            if (res.alive) {
                devicesIds.push(ip_machine);
                devices.push({ "ID": ip_machine, "IP": ip });
            }
        })
        .catch((err) => {
            console.error('Error occurred while pinging:', err);
        });

    console.log(devices)
}

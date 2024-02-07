const { exec } = require('child_process');

let hostname = 'localhost';
exec("ip route | awk '/default/ {print $3}'", (error, stdout) => {
    if (error) {
        console.error('cannot get outer ip address for wrapper service', error);
    } else {
        hostname = stdout.replace(/\n/, '');
        console.log(hostname)
    }
});

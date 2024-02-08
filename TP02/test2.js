const Docker = require('dockerode');

// Função para obter os IPs dos contêineres
async function getContainerIPs() {
    const docker = new Docker({ socketPath: '/etc/docker/daemon.json' });

    try {
        // Obtendo todos os contêineres em execução
        const containers = await docker.listContainers({});
        console.log(containers)
        const containerIPs = [];

        // Iterando sobre cada contêiner
        for (const containerInfo of containers) {
            const container = docker.getContainer(containerInfo.Id);

            // Obtendo detalhes do contêiner
            const containerDetails = await container.inspect();

            // Verificando se o contêiner está em execução
            if (containerDetails.State.Running) {
                // Obtendo o endereço IP do contêiner
                const ip = containerDetails.NetworkSettings.Networks.bridge.IPAddress;
                const name = containerDetails.Name;

                containerIPs.push({ name, ip });
            }
        }

        return containerIPs;
    } catch (error) {
        console.error('Erro ao obter IPs dos contêineres:', error);
        return [];
    }
}

// Exemplo de uso da função
getContainerIPs().then((containerIPs) => {
    console.log('IPs dos contêineres:', containerIPs);
}).catch((error) => {
    console.error('Erro:', error);
});

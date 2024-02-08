const fs = require('fs')
var ping = require('ping');

let recursoEmUso = false;
let coordenador = null;
let arrProvisorio = [];
let arrIpsMaquinas = [];
let maquinasEscaneadas = [];
let filaDeEspera = [];

async function checkHosts() {
    for (let ipMaq = 3; ipMaq < 12; ipMaq++) {
        const ip = `172.16.100.${ipMaq}`;
        arrProvisorio.push(ip);
    }

    for (const device of arrProvisorio) {
        try {
            const res = await ping.promise.probe(device);
            if (res.alive) {
                maquinasEscaneadas.push(device);
            }
        } catch (error) {
            console.error('Erro ocorrido ao pingar:', error);
        }
    }

    return maquinasEscaneadas
}

async function criaMaquinas() {
    maquinas = await checkHosts();

    // maquinas = [
    //     "172.168.100.1",
    //     "172.168.100.2",
    //     "172.168.100.3",
    //     "172.168.100.4",
    //     "172.168.100.5",
    // ]

    const idsDisponiveis = Array.from({ length: maquinas.length }, (_, index) => index + 1);

    arrIpsMaquinas = maquinas.map((ip, index) => {
        const idEscolhido = idsDisponiveis[index];
        return { ID: idEscolhido, IP: ip };
    });

    arrIpsMaquinas.sort((a, b) => a.ID - b.ID);
    arrAux = arrIpsMaquinas

    return arrAux
}

function eleicaoDoAnel() {
    let maiorID = null;

    for (let i = 0; i < arrIpsMaquinas.length; i++) {
        if (maiorID === null || arrIpsMaquinas[i].ID > maiorID) {
            maiorID = arrIpsMaquinas[i].ID;
            coordenador = arrIpsMaquinas[i];
        }
    }

    if (coordenador && coordenador.ID && coordenador.IP) {
        console.log("\n");
        console.log(`******** Coordenador: Máquina ${coordenador.ID} - ${coordenador.IP}! ********`);
        console.log("\n");
    }
}

function exclusaoMutua() {
    const solicitantes = arrIpsMaquinas.filter(ip => ip !== coordenador && ip !== filaDeEspera[0]);
    const solicitante = solicitantes[Math.floor(Math.random() * solicitantes.length)];

    if (recursoEmUso) {
        povoaFilaDeSolicitantes(solicitante)
        return
    }

    if (filaDeEspera.length === 0 && solicitante) {
        processaRecurso(solicitante);
    } else if (filaDeEspera.length > 0 && !filaDeEspera.some(item => item.ID === solicitante.ID && item.IP === solicitante.IP) && solicitante) {
        processaRecurso(solicitante);
    } else if (recursoEmUso && solicitante) {
        if (solicitante) {  // Verifica se solicitante não é nulo
            povoaFilaDeSolicitantes(solicitante);
        }
    }
}

function processaRecurso(solicitante) {
    console.log(`******** Máquina {${solicitante.ID} - ${solicitante.IP}} consumiu o recurso ********`);
    removeDaFilaDeSolicitantes(solicitante)

    recursoEmUso = true;

    setTimeout(() => {
        fs.appendFile("recurso.txt", `Máquina ${solicitante.ID} - (${solicitante.IP}) consumiu em ${new Date().toLocaleString()}\n`, (err) => {
            if (err) throw err;
        });

        recursoEmUso = false;

        if (filaDeEspera[0]) {
            solicitante = filaDeEspera[0]
            processaRecurso(solicitante)
        } else {
            solicitante = null; // Reinicia solicitante apenas se não houver mais na fila
            exclusaoMutua();
        }
    }, 10000);
}

function povoaFilaDeSolicitantes(novoSolicitante) {
    const jaNaFila = filaDeEspera.some(item => item.ID === novoSolicitante.ID && item.IP === novoSolicitante.IP);

    if (!jaNaFila) {
        filaDeEspera.push(novoSolicitante);
        console.log("\n");
        console.log(`******** Máquina {${novoSolicitante.ID} - ${novoSolicitante.IP}} entrou na fila! ********`);
        console.log("Fila de espera atual: " + filaDeEspera.map(item => `${item.ID} - ${item.IP}`).join(", "));
        console.log("\n");
    }
}

function removeDaFilaDeSolicitantes(maquina) {
    const index = filaDeEspera.indexOf(maquina);
    if (index !== -1) {
        filaDeEspera.splice(index, 1);
    }
}

criaMaquinas()
eleicaoDoAnel()
exclusaoMutua()

setInterval(() => {
    exclusaoMutua();
}, 10000); // 10 segundos em milissegundos
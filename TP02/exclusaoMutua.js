const fs = require('fs')

let coordenador = null;
let solicitante = null;
let recursoEmUso = false;
let arrIpsMaquinas = [];
let filaDeEspera = [];
let maquinaAtual = null;

function criaMaquinas() {
    const maquinasEscaneadas = [
        "172.16.100.1",
        "172.16.100.2",
        "172.16.100.3",
        "172.16.100.4",
        "172.16.100.5",
    ];

    const idsDisponiveis = Array.from({ length: maquinasEscaneadas.length }, (_, index) => index + 1);

    arrIpsMaquinas = maquinasEscaneadas.map((ip, index) => {
        const idEscolhido = idsDisponiveis[index];
        return { ID: idEscolhido, IP: ip };
    });

    arrIpsMaquinas.sort((a, b) => a.ID - b.ID);
    arrAux = arrIpsMaquinas

    return arrAux
}

function arraysSaoIguais(array1, array2) {
    if (array1.length !== array2.length) {
        return false;
    }

    for (let i = 0; i < array1.length; i++) {
        if (array1[i].IP !== array2[i].IP) {
            return false;
        }
    }

    return true;
}

function filtraMaquinasAusentes() {
    newArr = criaMaquinas();

    const diferenca = arrIpsMaquinas.filter(maquina => !newArr.includes(maquina.IP));

    if (arraysSaoIguais(diferenca, arrIpsMaquinas)) {
        return;
    }

    console.log("\n");
    diferenca.forEach(maquinaRemover => {
        const indexRemover = arrIpsMaquinas.findIndex(maquina => maquina.IP === maquinaRemover.IP);
        arrIpsMaquinas.splice(indexRemover, 1);
        console.log(`******** Máquina {${maquinaRemover.ID} - ${maquinaRemover.IP}} caiu! ********`);
    });
    console.log("\n");

    for (let i = 0; i < diferenca.length; i++) {
        const ipDiferenca = diferenca[i].IP;
        if (filaDeEspera.includes(ipDiferenca)) {
            removeDaFilaDeSolicitantes(ipDiferenca);
        }
    }

    if (!arrIpsMaquinas.includes(coordenador)) {
        coordenador = null
    }
}

function escolheCoordenador() {
    coordenador = arrIpsMaquinas[Math.floor(Math.random() * arrIpsMaquinas.length)];

    if (filaDeEspera.includes(coordenador)) {
        removeDaFilaDeSolicitantes(coordenador);
    }

    console.log("\n");
    console.log(`******** Coordenador: Máquina {${coordenador.ID} - ${coordenador.IP}}! ********`);
    console.log("\n");

    criaSolicitante();
}

function escolheSolicitante() {
    const solicitantes = arrIpsMaquinas.filter(ip => ip !== coordenador && ip !== maquinaAtual);
    const solicitante = solicitantes[Math.floor(Math.random() * solicitantes.length)];
    maquinaAtual = null;
    return solicitante;
}

function criaSolicitante() {
    const coord = coordenador;

    if (!coord) {
        escolheCoordenador();
    }
    solicitante = escolheSolicitante();
    maquinaAtual = solicitante;

    if (recursoEmUso) {
        povoaFilaDeSolicitantes(solicitante)
        return
    }

    if (filaDeEspera.length === 0 && solicitante) {
        processaRecurso();
    } else if (filaDeEspera.length > 0 && !filaDeEspera.some(item => item.ID === solicitante.ID && item.IP === solicitante.IP) && solicitante) {
        processaRecurso();
    } else if (recursoEmUso && solicitante) {
        if (solicitante) {  // Verifica se solicitante não é nulo
            povoaFilaDeSolicitantes(solicitante);
        }
    }
}

function processaRecurso() {
    if (!solicitante) {
        console.log("Nenhum solicitante disponível.");
        criaSolicitante();
        return;
    }
    aux = solicitante
    console.log(`******** Máquina {${aux.ID} - ${aux.IP}} solicita acesso ao Coordenador ********`);
    console.log("Coordenador libera acesso.");

    recursoEmUso = true;

    console.log(`Consumindo recurso em 5s...`);
    fs.appendFile("exclusaoMutua.txt", `Máquina ${solicitante.ID} - (${solicitante.IP}) consumiu em ${new Date().toLocaleString()}\n`, (err) => {
        if (err) throw err;
    });

    setTimeout(() => {
        // Verifica se solicitante ainda é o mesmo antes de acessar propriedades
        if (solicitante && solicitante.ID && solicitante.IP) {
            console.log(`Solicitante ${aux.ID} (${aux.IP}) liberou o recurso.\n`);
            recursoEmUso = false;

            removeDaFilaDeSolicitantes(aux)

            if (filaDeEspera[0]) {
                solicitante = filaDeEspera[0]
                processaRecurso()
            } else {
                solicitante = null; // Reinicia solicitante apenas se não houver mais na fila
                criaSolicitante();
            }
        } else {
            console.log("Solicitante indefinido. Aguardando novo solicitante.");
            recursoEmUso = false;
            criaSolicitante();
        }
    }, 5000);
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

function limpaArquivo() {
    fs.writeFileSync('eleicaoAnel.txt', '', 'utf-8');
}

// Início do processo
limpaArquivo();
criaMaquinas();
escolheCoordenador()

setInterval(() => {
    criaSolicitante();
}, 5000); // 10 segundos em milissegundos

setInterval(() => {
    filtraMaquinasAusentes()
}, 10000)

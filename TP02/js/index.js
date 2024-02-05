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
    ];

    const idsDisponiveis = Array.from({ length: maquinasEscaneadas.length }, (_, index) => index + 1);

    arrIpsMaquinas = maquinasEscaneadas.map((ip, index) => {
        const idEscolhido = idsDisponiveis[index];
        return { ID: idEscolhido, IP: ip };
    });

    arrIpsMaquinas.sort((a, b) => a.ID - b.ID);

    escolheCoordenador()
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

// Tentativa de implementação da eleição do anal, vou deixar comentado por que nao vou saber implementar direitinho mas pode ajudar na logica AKDAKSDAS

function escolheCoordenadorAnel() {

    // // Basicamente a eleição do anel funciona assim:
    // 1. ao detectar que o coordenador criaMaquinas, uma nova eleição é convocada
    // 2. a escolha do coord é feita de forma incremental, ou seja, um processo X ira iniciar a eleição e escrever seu ID numa especie de pacote que ira ser passado para a maquina X=1 que também ira anotar seu ID e passar para a proxima até chegar ao final da lista de maquinas
    // 3. Se o ID da maquina X é o maior inteiro da lista de maquinas, ela se torna o coordenador
    // 4. se alguma outra maquina possuir ID maior que o ID de X, a maquina X desiste e passa a coordenação para a maquina de maior ID
    // 6. importante!! -> o processo incremental deve PULAR o coordenador que acabou de cair e mandar direto para a maquina sucessora dele, ou seja de alguma forma teriamos que ou criar um array de maquinas disponíveis e remover o coord que caiu de la ou remover o que caiu direto da arrIpsMaquinas[]
    // 5. Os outros processos sao informados do novo coordenador

    let maiorID = null;

    for (let i = 0; i < arrIpsMaquinas.length; i++) {
        maiorID = (maiorID === null || arrIpsMaquinas[i] > maiorID) ? arrIpsMaquinas[i] : maiorID;
    }


    // teremos um problema na parte de atribuição de IDs ja que o array de maquinas possui apenas os ips como String, teriamos duas soluções:

    // 1. Criar um Objeto MAQUINA que possua uma tupla (IPstring e IDint) podemos atribuir o ID de forma aleatoria ou sequencial (seria interessante se fosse random)

    // 2. Arrumar alguma forma de converter o IP de da maquina de string para int e usar os numeros do IP como ID, solução rápida porém o maior ID vai ser sempre da maquina maior IP e nao de forma randomica

    coordenador = arrIpsMaquinas[maiorID];

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

    setTimeout(() => {
        // Verifica se solicitante ainda é o mesmo antes de acessar propriedades
        if (solicitante && solicitante.ID && solicitante.IP) {
            fs.appendFile("./recurso_compartilhado.txt", `Máquina ${solicitante.ID} - (${solicitante.IP}) consumiu em ${new Date().toLocaleString()}\n`, (err) => {
                if (err) throw err;
            });

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

// Início do processo
criaMaquinas();

setInterval(() => {
    criaSolicitante();
}, 20000); // 20 segundos em milissegundos


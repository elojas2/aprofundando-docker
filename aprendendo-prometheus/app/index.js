var express = require('express')
const prom = require('prom-client');
const register = prom.register;

var app = express();

const contadorRequisicoes = new prom.Counter({
    name: 'aula_request_total',
    help: 'contador_request',
    labelNames: ['statusCode']
})

const usuariosLogados = new prom.Gauge({
    name: 'aula_usuarios_logados_total',
    help: 'numero de usuarios logados no momento'
})

// const summary = new prom.Summary({
//     name: 'aula_summary_request_time_seconds',
//     help: 'Tempo de resposta de API',
//     percentiles: [0.5, 0.9, 0.99]
// })


const tempoDeResposta = new prom.Histogram({
    name: 'aula_request_duration_seconds',
    help: 'Tempo de resposta de API',
    //buckets: [0.1, 0.2, 0.3, 0.4, 0.5]
})


var zeraUsuarioLogados = false;


function randn_bm(min, max, skew) {
    let u = 0, v = 0;
    while(u === 0) u = Math.random() //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random()
    let num = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v )
    
    num = num / 10.0 + 0.5 // Translate to 0 -> 1
    if (num > 1 || num < 0) 
      num = randn_bm(min, max, skew) // resample between 0 and 1 if out of range
    
    else{
      num = Math.pow(num, skew) // Skew
      num *= max - min // Stretch to fill range
      num += min // offset to min
    }
    return num
}


setInterval(()=> {
    var erro = 5;
    var statusCode = (Math.random() < erro/100) ? '500' : '200';
    contadorRequisicoes.labels(statusCode).inc();
    var usuario = (zeraUsuarioLogados) ? 0 : 500 + Math.round((50*Math.random()))
    usuariosLogados.set(usuario);
    
    var tempoObservado = randn_bm(0,3,4)
    tempoDeResposta.observe(tempoObservado);
},100)


app.get('/', function(req, res){
    res.send("Hello world");
});

app.get('/zera-usuarios', function(req, res){
    zeraUsuarioLogados = true;
    res.send("zerado");
});

app.get('/retorna-usuarios', function(req, res){
    zeraUsuarioLogados = false;
    res.send("retorna");
});


app.get('/metrics', async function(req, res){

    res.set("Content-Type", register.contentType);
    res.end(await register.metrics())
});

app.listen(30000);
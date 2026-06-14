import { getMeta, optimize } from "./api.js"
import { subscribe, state } from "./state.js"
import { buildDropdown, renderParams, renderInfo } from "./ui.js"
import { renderGraph } from "./graph.js"

const algoSelect = document.getElementById("algorithmSelect")
const funcSelect = document.getElementById("functionSelect")
const paramsDiv = document.getElementById("parameters")
const infoPanel = document.getElementById("infoPanel")

let meta = null

async function init(){
    meta = await getMeta()
    buildDropdown(algoSelect, meta.algorithms, "algorithm")
    buildDropdown(funcSelect, meta.functions, "function")
    algoSelect.value = meta.algorithms[0].name
    funcSelect.value = meta.functions[0].name
    state.algorithm = algoSelect.value
    state.function = funcSelect.value
    updateParams()
}

function updateParams(){
    const algo = meta.algorithms.find(a=>a.name===state.algorithm)
    renderParams(paramsDiv, algo.parameters)
}

subscribe(async (s) => {
    if(!s.algorithm || !s.function) return
    const result = await optimize({
        algorithm: s.algorithm,
        function: s.function,
        params: s.params
    })
    renderGraph(result)
    renderInfo(infoPanel, result.info)
})

init()
window.addEventListener("algorithmChanged", () => {
    updateParams()
})

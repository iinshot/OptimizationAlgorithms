import { setState, state } from "./state.js"

export function buildDropdown(select, items, key){
    select.innerHTML = ""

    items.forEach(it => {
        const opt = document.createElement("option")
        opt.value = it.name
        opt.textContent = it.label
        select.appendChild(opt)
    })

    select.onchange = () => {
        setState({ [key]: select.value })

        if(key === "algorithm"){
            window.dispatchEvent(new Event("algorithmChanged"))
        }
    }
}

export function renderParams(container, params){

    container.innerHTML = ""

    const values = {}

    params.forEach(p => {

        const row = document.createElement("div")
        row.className = "paramRow"

        const label = document.createElement("label")
        label.textContent = `${p.label} =`

        const input = document.createElement("input")
        input.type = "number"
        input.value = p.default

        if(p.min !== undefined) input.min = p.min
        if(p.max !== undefined) input.max = p.max
        if(p.step !== undefined) input.step = p.step

        values[p.name] = Number(p.default)

        input.oninput = () => {
            values[p.name] = Number(input.value)
            setState({ params:{...values} })
        }

        row.appendChild(label)
        row.appendChild(input)

        container.appendChild(row)
    })

    setState({ params: values })
}

export function renderInfo(panel, info){

    if(!info){
        panel.innerHTML = ""
        return
    }

    panel.innerHTML = `
        <b>Результат</b><br>
        Мин. значение: ${info.min_value.toFixed(7)}<br>
        Точка: (${info.min_point[0].toFixed(2)}, ${info.min_point[1].toFixed(2)})
        <span style="color: #2c3e50; background: #ecf0f1; padding: 4px 8px; border-radius: 4px; display: inline-block; margin-top: 8px;">
            ${info.stop_reason || "⚠Причина не указана"}
        </span>
    `
}

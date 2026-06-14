export const state = {
    algorithm: null,
    function: null,
    params: {},
    listeners: []
}

export function setState(patch){
    Object.assign(state, patch)
    state.listeners.forEach(l => l(state))
}

export function subscribe(fn){
    state.listeners.push(fn)
}
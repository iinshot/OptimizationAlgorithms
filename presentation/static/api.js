export async function getMeta(){
    const response = await fetch("/meta")
    return response.json()
}

export async function optimize(payload){
    const response = await fetch("/optimize",{
        method: "POST",
        headers: { "Content-Type":"application/json" },
        body:JSON.stringify(payload)
    })

    return response.json()
}

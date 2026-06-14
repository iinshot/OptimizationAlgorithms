export function renderGraph(data) {
    const traceSurface = {
        z: data.surface.z,
        x: data.surface.x,
        y: data.surface.y,
        type: "surface",
        opacity: 0.8  // чуть прозрачнее — точка не прячется за поверхность
    }

    const tracePath = {
        x: data.trajectory.map(p => p[0]),
        y: data.trajectory.map(p => p[1]),
        z: data.trajectory.map(p => p[2]),
        mode: "lines+markers",
        marker: { size: 6, color: "red", symbol: "circle" },
        line: { color: "red", width: 4 },
        type: "scatter3d"
    }

    const xMin = Math.min(...data.surface.x)
    const xMax = Math.max(...data.surface.x)
    const yMin = Math.min(...data.surface.y)
    const yMax = Math.max(...data.surface.y)

    const zFlat = data.surface.z.flat()
    const zMin = Math.min(...zFlat, ...data.trajectory.map(p => p[2]))
    const zMax = Math.max(...zFlat, ...data.trajectory.map(p => p[2]))

    const layout = {
        scene: {
            xaxis: { range: [xMin, xMax] },
            yaxis: { range: [yMin, yMax] },
            zaxis: { range: [zMin, zMax] }
        }
    }

    Plotly.react("graph", [traceSurface, tracePath], layout)
}
let pyodide = null;
let lastCsv = null;

function setStatus(msg) {
  document.getElementById("status").textContent = msg;
}

function setDebug(msg) {
  document.getElementById("debug").textContent = msg;
}

async function initPyodideAndLoad() {
  setStatus("Loading Pyodide...");
  pyodide = await loadPyodide();

  // Load packages you need. Keep it minimal.
  setStatus("Loading Python packages (numpy)...");
  await pyodide.loadPackage(["numpy"]);

  // Load solver.py as text and execute it.
  setStatus("Loading solver.py...");
  const solverText = await fetch("./solver.py").then(r => r.text());
  await pyodide.runPythonAsync(solverText);

  setStatus("Ready.");
}

function readInputs() {
  return {
    rho: Number(document.getElementById("rho").value),
    gamma: Number(document.getElementById("gamma").value),
    theta_deg: Number(document.getElementById("theta").value),
    R: Number(document.getElementById("R").value),
    g: Number(document.getElementById("g").value),
    n: Number(document.getElementById("n").value),
  };
}

function plotResult(x, y) {
  const trace = {
    x: x,
    y: y,
    mode: "lines+markers",
    name: "meniscus",
  };
  const layout = {
    title: "Meniscus profile (example model)",
    xaxis: { title: "r [m]" },
    yaxis: { title: "z [m]" },
    margin: { l: 60, r: 20, t: 50, b: 60 },
  };
  Plotly.newPlot("plot", [trace], layout, { responsive: true });
}

async function runSolver() {
  try {
    document.getElementById("runBtn").disabled = true;
    setStatus("Running solver...");
    setDebug("");

    const params = readInputs();

    // Call Python function: solve(params)
    // IMPORTANT: params becomes JsProxy in Python. Python must call params.to_py().
    const solve = pyodide.globals.get("solve");
    const resultProxy = await solve(params); // returns a Python dict -> JsProxy

    // Convert Python dict proxy to a plain JS object
    const result = resultProxy.toJs({ dict_converter: Object.fromEntries });

    const x = result.x;   // JS array
    const y = result.y;   // JS array
    lastCsv = result.csv; // string

    plotResult(x, y);

    document.getElementById("downloadBtn").disabled = false;
    setStatus("Done.");
  } catch (e) {
    setStatus("Error.");
    setDebug(String(e?.stack || e));
    console.error(e);
  } finally {
    document.getElementById("runBtn").disabled = false;
  }
}

function downloadCsv() {
  if (!lastCsv) return;
  const blob = new Blob([lastCsv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "meniscus.csv";
  a.click();

  URL.revokeObjectURL(url);
}

document.getElementById("runBtn").addEventListener("click", runSolver);
document.getElementById("downloadBtn").addEventListener("click", downloadCsv);

initPyodideAndLoad();

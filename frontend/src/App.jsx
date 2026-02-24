import React, { useState } from 'react'

const api = 'http://localhost:8000'

export default function App() {
  const [file, setFile] = useState(null)
  const [scale, setScale] = useState('1:100')
  const [project, setProject] = useState(null)

  const parse = async () => {
    const fd = new FormData()
    fd.append('file', file)
    const res = await fetch(`${api}/parse?scale_input=${encodeURIComponent(scale)}`, { method: 'POST', body: fd })
    setProject(await res.json())
  }

  const run = async () => {
    const res = await fetch(`${api}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project }),
    })
    const out = await res.json()
    setProject(out.project)
    alert(`Report: ${out.report_path}\nAnnotated: ${out.annotated_pdf_path}`)
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 20 }}>
      <h2>PDF Member Size Checker (v1)</h2>
      <input type='file' accept='application/pdf' onChange={(e) => setFile(e.target.files[0])} />
      <input value={scale} onChange={(e) => setScale(e.target.value)} style={{ marginLeft: 8 }} />
      <button disabled={!file} onClick={parse} style={{ marginLeft: 8 }}>Parse PDF</button>
      <button disabled={!project} onClick={run} style={{ marginLeft: 8 }}>Run Checks</button>
      {project && <pre>{JSON.stringify(project, null, 2)}</pre>}
    </div>
  )
}

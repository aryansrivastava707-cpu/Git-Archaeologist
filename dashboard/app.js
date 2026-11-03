const input = document.querySelector('#report-file');
const status = document.querySelector('#status');
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const table = (headers, rows) => rows.length
  ? `<table><thead><tr>${headers.map(h=>`<th>${escapeHtml(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(v=>`<td>${escapeHtml(v)}</td>`).join('')}</tr>`).join('')}</tbody></table>`
  : '<p>No data in this section.</p>';
function render(data) {
  if (!data || !Array.isArray(data.hotspots) || !Array.isArray(data.work_rhythm)) throw new Error('This file is not a Git Archaeologist report.');
  const cards = [['Repository', data.repository], ['Commits', data.commit_count], ['Estimated bus factor', data.bus_factor?.authors_needed ?? '—'], ['Changed lines', data.bus_factor?.changed_lines ?? '—']];
  document.querySelector('#summary').innerHTML = cards.map(([k,v])=>`<article class="card"><small>${escapeHtml(k)}</small><strong>${escapeHtml(v ?? '—')}</strong></article>`).join('');
  document.querySelector('#hotspots').innerHTML = table(['File','Commits','Changed lines'],data.hotspots.map(x=>[x.path,x.commits,x.changed_lines]));
  document.querySelector('#authors').innerHTML = table(['Author','Changed lines'],(data.bus_factor?.authors ?? []).map(x=>[x.name,x.changed_lines]));
  document.querySelector('#stale').innerHTML = table(['File','Days since change'],(data.stale_files ?? []).map(x=>[x.path,x.days_since_change]));
  const days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], blocks=['00–06','06–12','12–18','18–24'];
  const max=Math.max(1,...data.work_rhythm.flat());
  document.querySelector('#rhythm').innerHTML=`<div class="rhythm-row"><span></span>${blocks.map(b=>`<small>${b}</small>`).join('')}</div>`+data.work_rhythm.map((row,i)=>`<div class="rhythm-row"><strong>${days[i]}</strong>${row.map(n=>`<span class="cell" data-level="${Math.min(3,Math.ceil(n/max*3))}" title="${n} commits">${n}</span>`).join('')}</div>`).join('');
  status.textContent=`Loaded ${data.commit_count} commits from ${data.repository}.`;
}
input.addEventListener('change', async () => {
  const file=input.files?.[0]; if (!file) return;
  try { render(JSON.parse(await file.text())); }
  catch (error) { status.textContent=error.message || 'Could not read this report.'; }
});

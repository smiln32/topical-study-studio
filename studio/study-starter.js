/* Study starter: fill in the blanks, get a study specification that validates today.

   buildStudySpec(form) is pure and runs in Node as well as the browser, so a test can hold
   the layout it writes to the validator. The rest is the page's own behaviour. Blocks are
   laid out on the split recipe in stages/03_spec/references/layout-recipes.md, and every row
   count is computed from the engine's height estimate so the validator reports nothing. */

const STARTER_VERSION = 1;
const CONTENT = { top: 104, bottom: 1030, left: 28, full: 760, half: 373, right: 415, gap: 14 };
const HEAD_H = 32, BODY_TOP_PAD = 11, BORDER_W = 1.2, LINE_H = 22, CHECK_H = 24, PROMPT_H = 16;
const MAX_WORDS = 10, MAX_QUESTIONS = 4;
const COLOURS = ['sage', 'blue', 'lav', 'warm'];

function bodyHeight(h) { return h - HEAD_H - BODY_TOP_PAD - 2 * BORDER_W; }
function linesThatFit(h, hasPrompt) { return Math.max(1, Math.floor((bodyHeight(h) - (hasPrompt ? PROMPT_H : 0)) / LINE_H)); }
function checksThatFit(h) { return Math.max(0, Math.floor(bodyHeight(h) / CHECK_H)); }
function calloutRows(h, text, w) {
  const charsPerLine = Math.max(20, Math.floor((w - 26) / 5));
  const textLines = Math.ceil(String(text).length / charsPerLine);
  return Math.max(0, Math.min(4, Math.floor((bodyHeight(h) - textLines * 14) / LINE_H)));
}
function clean(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }
function list(s, max) { return String(s || '').split(/[,\n]/).map(clean).filter(Boolean).slice(0, max); }
function listLines(s, max) { return String(s || '').split('\n').map(clean).filter(Boolean).slice(0, max); }

/* The wording the starter writes when a field is left blank. Each one carries the passage
   reference, so the same field on two sessions never repeats a prompt. */
function sessionDefaults(reference, n) {
  const ref = clean(reference) || `the passage for session ${n}`;
  return {
    read: `Read ${ref} twice in the NASB 2020, once silently and once aloud. Then write out, in your own hand, the verse that speaks most clearly to you.`,
    observe: `What does ${ref} say? Note every action, picture and repeated word before you decide what it means.`,
    interpret: `What would ${ref} have meant to the people who first heard it? What does it show about who God is?`,
    apply: `What does ${ref} ask of me this week?`,
    prayer: `A prayer in response to ${ref}`,
  };
}

function sessionPage(s, n, theme) {
  const ref = clean(s.reference);
  const refOrSession = ref || `Session ${n}`;
  const name = clean(s.title) || refOrSession;
  const d = sessionDefaults(ref, n);
  const text = clean(s.read) || d.read;
  const words = list(s.words, MAX_WORDS);
  const blocks = [
    { x: CONTENT.left, y: 104, w: CONTENT.full, h: 150, title: ref ? `Read ${ref}` : `Session ${n} · Read the passage`, color: 'sage',
      content: { type: 'callout', text, rows: calloutRows(150, text, CONTENT.full) } },
    { x: CONTENT.left, y: 268, w: CONTENT.half, h: 300, title: `Session ${n} · Observe`, color: 'blue',
      content: { type: 'lines', prompt: clean(s.observe) || d.observe, rows: linesThatFit(300, true) } },
    words.length
      ? { x: CONTENT.right, y: 268, w: CONTENT.half, h: 300, title: `Session ${n} · Words to look up`, color: 'lav',
          content: { type: 'checklist', items: words, blank_rows: Math.max(0, checksThatFit(300) - words.length) } }
      : { x: CONTENT.right, y: 268, w: CONTENT.half, h: 300, title: `Session ${n} · Questions`, color: 'lav',
          content: { type: 'lines', prompt: `Questions ${refOrSession} raises for me`, rows: linesThatFit(300, true) } },
    { x: CONTENT.left, y: 582, w: CONTENT.full, h: 200, title: `Session ${n} · Interpret`, color: 'warm',
      content: { type: 'lines', prompt: clean(s.interpret) || d.interpret, rows: linesThatFit(200, true) } },
    { x: CONTENT.left, y: 796, w: CONTENT.full, h: 234, title: `Session ${n} · Apply`, color: 'sage',
      content: { type: 'split',
        left: { type: 'lines', prompt: clean(s.apply) || d.apply, rows: linesThatFit(234, true) },
        right: { type: 'lines', prompt: clean(s.prayer) || d.prayer, rows: linesThatFit(234, true) } } },
  ];
  return {
    label: `Session ${n}`,
    concept: `Session ${n}: ${name}`,
    title: `SESSION ${n}: ${name.toUpperCase()}`,
    subtitle: clean(s.intro) || `${refOrSession}. Read the whole passage before you begin.`,
    theme,
    blocks,
  };
}

function discussionPage(s, n, theme) {
  const questions = listLines(s.questions, MAX_QUESTIONS);
  if (!questions.length) return null;
  const ref = clean(s.reference) || `Session ${n}`;
  const m = questions.length;
  const h = Math.floor((CONTENT.bottom - CONTENT.top - CONTENT.gap * (m - 1)) / m);
  const blocks = questions.map((q, k) => {
    const y = CONTENT.top + k * (h + CONTENT.gap);
    const height = k === m - 1 ? CONTENT.bottom - y : h;
    return { x: CONTENT.left, y, w: CONTENT.full, h: height, title: `Session ${n} · Question ${k + 1}`, color: COLOURS[k % COLOURS.length],
      content: { type: 'lines', prompt: q, rows: linesThatFit(height, true) } };
  });
  return {
    label: `Session ${n} · Discuss`,
    concept: `Session ${n}: Discuss ${ref}`,
    title: `SESSION ${n}: DISCUSS`,
    subtitle: `${ref}. Talk these through together, and go back to the text whenever you disagree.`,
    theme,
    blocks,
  };
}

function buildStudySpec(form) {
  const title = clean(form.title) || 'Untitled study';
  const brand = clean(form.brand) || 'Simplify to Glorify';
  const theme = /^#[0-9a-f]{6}$/i.test(form.theme || '') ? form.theme : '#b2c6b1';
  const pages = [];
  (form.sessions || []).forEach((s, i) => {
    pages.push(sessionPage(s, i + 1, theme));
    const discuss = discussionPage(s, i + 1, theme);
    if (discuss) pages.push(discuss);
  });
  return {
    starter_version: STARTER_VERSION,
    set_title: title,
    footer_label: `${brand} | ${title}`,
    audience: clean(form.audience),
    outcome: clean(form.outcome),
    pages,
  };
}

if (typeof module !== 'undefined' && module.exports) module.exports = { buildStudySpec, sessionDefaults };

/* ---------------------------------------------------------------- the page */
if (typeof document !== 'undefined') (function () {
  const $ = (s, el) => (el || document).querySelector(s), $$ = (s, el) => [...(el || document).querySelectorAll(s)];
  const KEY = 'studyStarter';
  const AUTO = ['read', 'observe', 'interpret', 'apply', 'prayer'];
  let form, timer;

  function freshSession() { return { title: '', reference: '', words: '', intro: '', read: '', observe: '', interpret: '', apply: '', prayer: '', questions: '', auto: AUTO.slice() }; }
  function fresh() {
    return { title: '', brand: 'Simplify to Glorify', audience: '', outcome: '', theme: '#b2c6b1', sessions: [freshSession()] };
  }
  function load() {
    try { form = JSON.parse(localStorage.getItem(KEY)) || fresh(); } catch { form = fresh(); }
    if (!Array.isArray(form.sessions) || !form.sessions.length) form.sessions = [freshSession()];
    form.sessions.forEach(s => { if (!Array.isArray(s.auto)) s.auto = AUTO.filter(k => !clean(s[k])); });
  }
  function save() {
    clearTimeout(timer);
    $('#saved').textContent = 'Saving…';
    timer = setTimeout(() => { localStorage.setItem(KEY, JSON.stringify(form)); $('#saved').textContent = 'Saved locally'; }, 250);
  }
  function fillAuto(s, n) {
    const d = sessionDefaults(s.reference, n);
    s.auto.forEach(k => { s[k] = d[k]; });
  }
  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._timer); t._timer = setTimeout(() => t.classList.remove('show'), 2200);
  }
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'study'; }
  function spec() { return buildStudySpec(form); }

  function renderStudy() {
    $('#title').value = form.title; $('#brand').value = form.brand; $('#audience').value = form.audience;
    $('#outcome').value = form.outcome; $('#theme').value = form.theme;
  }
  function renderSessions() {
    const ol = $('#sessions');
    ol.innerHTML = '';
    form.sessions.forEach((s, i) => {
      const n = i + 1;
      fillAuto(s, n);
      const li = $('#sessionRow').content.firstElementChild.cloneNode(true);
      $('.n', li).textContent = n;
      $$('[data-k]', li).forEach(el => {
        const k = el.dataset.k;
        el.value = s[k] || '';
        el.id = `s${n}-${k}`;
        el.oninput = () => {
          s[k] = el.value;
          if (AUTO.includes(k)) s.auto = s.auto.filter(a => a !== k);
          if (k === 'reference') { fillAuto(s, n); AUTO.forEach(a => { $(`[data-k="${a}"]`, li).value = s[a]; }); }
          save(); renderSpec();
        };
      });
      $$('[data-act]', li).forEach(b => b.onclick = () => {
        const act = b.dataset.act;
        if (act === 'remove') { if (form.sessions.length === 1) return toast('A study needs at least one session'); form.sessions.splice(i, 1); }
        if (act === 'up' && i > 0) form.sessions.splice(i - 1, 0, form.sessions.splice(i, 1)[0]);
        if (act === 'down' && i < form.sessions.length - 1) form.sessions.splice(i + 1, 0, form.sessions.splice(i, 1)[0]);
        renderSessions(); save(); renderSpec();
      });
      $('[data-act="up"]', li).disabled = i === 0;
      $('[data-act="down"]', li).disabled = i === form.sessions.length - 1;
      ol.appendChild(li);
    });
  }
  function renderSpec() { $('#specView').textContent = JSON.stringify(spec(), null, 2); }
  function showFindings(findings, valid) {
    const box = $('#findings');
    if (!findings.length) { box.innerHTML = '<p class="finding good">No findings. The study validates cleanly.</p>'; return; }
    box.innerHTML = (valid ? '<p class="finding">Warnings to read; nothing stops generation.</p>' : '')
      + findings.map(f => `<p class="finding ${f.startsWith('ERROR') ? 'bad' : ''}">${esc(f)}</p>`).join('');
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]); }
  const OFFLINE = 'The local generator is not running. Start it with python study_studio.py and open this page from there to check, preview and download the finished HTML. The JSON download works without it.';

  async function post(path) {
    const r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(spec()) });
    return r;
  }
  async function check() {
    try {
      const r = await (await post('/api/validate')).json();
      showFindings(r.findings || [], r.valid);
      return r;
    } catch { showFindings([OFFLINE], false); return null; }
  }
  async function rendered() {
    let r;
    try { r = await post('/api/render'); } catch { showFindings([OFFLINE], false); return null; }
    if (!r.ok) {
      let payload = {};
      try { payload = await r.json(); } catch { /* not JSON */ }
      showFindings(payload.findings || [payload.error || `The generator answered ${r.status}.`], false);
      return null;
    }
    return r.text();
  }
  function download(blob, name) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    toast(`${name} downloaded`);
  }

  load();
  renderStudy();
  renderSessions();
  renderSpec();
  ['title', 'brand', 'audience', 'outcome', 'theme'].forEach(k => {
    $('#' + k).oninput = e => { form[k] = e.target.value; save(); renderSpec(); if (k === 'theme') $('#theme').value = form.theme; };
  });
  $('#addSession').onclick = () => { form.sessions.push(freshSession()); renderSessions(); save(); renderSpec(); $(`#s${form.sessions.length}-reference`).focus(); };
  $('#reset').onclick = () => {
    if (!confirm('Clear every field and start over?')) return;
    form = fresh(); localStorage.removeItem(KEY); renderStudy(); renderSessions(); renderSpec(); $('#findings').innerHTML = ''; $('#previewCard').hidden = true; toast('Cleared');
  };
  $('#check').onclick = check;
  $('#preview').onclick = async () => {
    const html = await rendered();
    if (html === null) return;
    $('#frame').srcdoc = html; $('#previewCard').hidden = false; $('#previewCard').scrollIntoView({ behavior: 'smooth' });
    await check();
  };
  $('#html').onclick = async () => {
    const html = await rendered();
    if (html === null) return;
    download(new Blob([html], { type: 'text/html' }), slug(form.title || 'study') + '.html');
    await check();
  };
  $('#json').onclick = () => download(new Blob([JSON.stringify(spec(), null, 2)], { type: 'application/json' }), slug(form.title || 'study') + '.json');
  $('#study').onsubmit = e => { e.preventDefault(); check(); };
})();

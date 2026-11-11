/* Study starter: fill in the blanks, get a study specification that validates today.

   buildStudySpec(form) is pure and runs in Node as well as the browser, so a test can hold
   the layout it writes to the validator. The rest is the page's own behaviour. Blocks are
   laid out on the split recipe in stages/03_spec/references/layout-recipes.md, and every row
   count is computed from the engine's height estimate so the validator reports nothing. */

const STARTER_VERSION = 1;
const CONTENT = { top: 104, bottom: 1030, left: 28, full: 760, half: 373, right: 415, gap: 14 };
const HEAD_H = 32, BODY_TOP_PAD = 11, BORDER_W = 1.2, LINE_H = 22, CHECK_H = 24, PROMPT_H = 16;
const PASSAGE_REF_H = 20, PASSAGE_CHAR_W = 5.6, PASSAGE_LINE_H = 15.4, NOTICE_CHAR_W = 4.4, NOTICE_LINE_H = 10.7;
const REF_CHAR_W = 6.4, REF_LINE_H = 14, REF_LABEL_W = 64;
const MIN_ROW_H = 110;
const MAX_WORDS = 10, MAX_QUESTIONS = 4;
const COLOURS = ['sage', 'blue', 'lav', 'warm'];
const AUTO = ['read', 'observe', 'interpret', 'apply', 'prayer'];
const TEXT_KEYS = ['title', 'reference', 'passage', 'words', 'intro', 'read', 'observe', 'interpret', 'apply', 'prayer', 'questions'];

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

/* Pasted passage text, one verse per line, each starting with its number. A line with no number
   continues the verse before it; a first line with no number reaches the validator, which names it. */
function parseVerses(text) {
  const verses = [];
  String(text || '').split('\n').map(clean).filter(Boolean).forEach(line => {
    const m = line.match(/^(\d+)[\s.:)]+(.+)$/);
    if (m) verses.push({ number: Number(m[1]), text: m[2] });
    else if (verses.length) verses[verses.length - 1].text += ' ' + line;
    else verses.push({ number: 0, text: line });
  });
  return verses;
}

/* How tall a full-width passage block must be; the same estimate the engine makes. */
function passageBlockHeight(verses, notice, hasPrompt, reference) {
  const inner = CONTENT.full - 26;
  const perLine = (w, room = inner) => Math.max(1, Math.floor(room / w));
  const chars = verses.reduce((n, v) => n + v.text.length + String(v.number).length + 1, 0);
  const refLines = Math.max(1, Math.ceil(String(reference || '').length / perLine(REF_CHAR_W, inner - REF_LABEL_W)));
  let need = PASSAGE_REF_H + (refLines - 1) * REF_LINE_H + Math.ceil(chars / perLine(PASSAGE_CHAR_W)) * PASSAGE_LINE_H + (hasPrompt ? PROMPT_H : 0);
  if (notice) need += 4 + Math.ceil(notice.length / perLine(NOTICE_CHAR_W)) * NOTICE_LINE_H;
  return Math.ceil(need + HEAD_H + BODY_TOP_PAD + 2 * BORDER_W + 1);
}

/* The wording the starter writes when a field is left blank. Each one carries the passage
   reference, and the session number as well when another session has the same reference,
   so the same field on two sessions never repeats a prompt. */
function sessionDefaults(reference, n, shared) {
  const ref = clean(reference) ? clean(reference) + (shared ? ` (session ${n})` : '') : `the passage for session ${n}`;
  return {
    read: `Read ${ref} twice in the NASB 2020, once silently and once aloud. Then write out, in your own hand, the verse that speaks most clearly to you.`,
    observe: `What does ${ref} say? Note every action, picture and repeated word before you decide what it means.`,
    interpret: `What would ${ref} have meant to the people who first heard it? What does it show about who God is?`,
    apply: `What does ${ref} ask of me this week?`,
    prayer: `A prayer in response to ${ref}`,
  };
}

/* Which sessions share a reference with another session. */
/* The validator compares phrases with case and punctuation removed, so "1-3" and "1–3" match. */
function phrase(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim(); }
function sharedReferences(sessions) {
  const counts = {};
  sessions.forEach(s => { const r = phrase(s.reference); if (r) counts[r] = (counts[r] || 0) + 1; });
  return sessions.map(s => counts[phrase(s.reference)] > 1);
}

/* The defaults for session i of a list, and whether each auto field still holds its plain
   default (the page copies defaults into the fields, so "left blank" means blank or unedited). */
function defaultsFor(sessions, i) {
  const s = sessions[i], n = i + 1, shared = sharedReferences(sessions)[i];
  const plain = sessionDefaults(s.reference, n, false);
  const d = sessionDefaults(s.reference, n, shared);
  const value = {};
  AUTO.forEach(k => { const v = clean(s[k]); value[k] = (!v || v === plain[k] || v === d[k]) ? d[k] : v; });
  return { defaults: d, value, shared };
}

function sessionPage(sessions, i, theme, notice) {
  const s = sessions[i], n = i + 1;
  const { value, shared, defaults } = defaultsFor(sessions, i);
  const ref = clean(s.reference);
  const refShown = ref ? ref + (shared ? ` (session ${n})` : '') : '';
  const name = clean(s.title) || ref;
  const words = list(s.words, MAX_WORDS);
  const verses = parseVerses(s.passage);
  const quoting = verses.length > 0 && !!ref;
  const readEdited = value.read !== defaults.read;
  /* A quoted passage takes the height it needs and the rows below give it up, each down to its own
     minimum; the checklist keeps room for every word. A passage too long for that moves to a page of its own. */
  const minObserve = Math.max(MIN_ROW_H, words.length ? Math.ceil(words.length * CHECK_H + HEAD_H + BODY_TOP_PAD + 2 * BORDER_W + 1) : 0);
  const rows = [[300, minObserve], [200, MIN_ROW_H], [234, MIN_ROW_H]];
  const spare = rows.reduce((t, [h, m]) => t + h - m, 0);
  const needH = quoting ? Math.max(92, passageBlockHeight(verses, notice, readEdited, ref)) : 150;
  const ownPage = quoting && needH - 150 > spare;
  const readH = ownPage ? 150 : needH;
  const take = Math.max(0, readH - 150);
  const shrink = ([h, m]) => Math.round(h - (h - m) / spare * take);
  const observeH = shrink(rows[0]), interpretH = shrink(rows[1]);
  const observeY = 104 + readH + CONTENT.gap, interpretY = observeY + observeH + CONTENT.gap, applyY = interpretY + interpretH + CONTENT.gap;
  const applyH = Math.max(92, CONTENT.bottom - applyY);
  const passageContent = Object.assign({ type: 'passage', reference: ref, verses }, notice ? { notice } : {}, readEdited ? { prompt: value.read } : {});
  const readText = ownPage && !readEdited ? `Read ${refShown} on the page before this one, twice, once silently and once aloud. Then write out the verse that speaks most clearly to you.` : value.read;
  const readContent = quoting && !ownPage ? passageContent : { type: 'callout', text: readText, rows: calloutRows(150, readText, CONTENT.full) };
  const blocks = [
    { x: CONTENT.left, y: 104, w: CONTENT.full, h: readH, title: ownPage ? `Session ${n} · Before you begin` : refShown ? `Read ${refShown}` : `Session ${n} · Read the passage`, color: 'sage', content: readContent },
    { x: CONTENT.left, y: observeY, w: CONTENT.half, h: observeH, title: `Session ${n} · Observe`, color: 'blue',
      content: { type: 'lines', prompt: value.observe, rows: linesThatFit(observeH, true) } },
    words.length
      ? { x: CONTENT.right, y: observeY, w: CONTENT.half, h: observeH, title: `Session ${n} · Words to look up`, color: 'lav',
          content: { type: 'checklist', items: words, blank_rows: Math.max(0, checksThatFit(observeH) - words.length) } }
      : { x: CONTENT.right, y: observeY, w: CONTENT.half, h: observeH, title: `Session ${n} · Questions`, color: 'lav',
          content: { type: 'lines', prompt: `Questions ${refShown || `session ${n}`} raises for me`, rows: linesThatFit(observeH, true) } },
    { x: CONTENT.left, y: interpretY, w: CONTENT.full, h: interpretH, title: `Session ${n} · Interpret`, color: 'warm',
      content: { type: 'lines', prompt: value.interpret, rows: linesThatFit(interpretH, true) } },
    { x: CONTENT.left, y: applyY, w: CONTENT.full, h: applyH, title: `Session ${n} · Apply`, color: 'sage',
      content: { type: 'split',
        left: { type: 'lines', prompt: value.apply, rows: linesThatFit(applyH, true) },
        right: { type: 'lines', prompt: value.prayer, rows: linesThatFit(applyH, true) } } },
  ];
  const page = {
    label: `Session ${n}`,
    concept: `Session ${n} study: ${name || 'untitled'}`,   // "study" and "discussion" sit where no typed title can reach
    title: name ? `Session ${n}: ${name}` : `Session ${n}`,
    subtitle: clean(s.intro) || `${ref || `Session ${n}`}. Read the whole passage before you begin.`,
    theme,
    blocks,
  };
  if (!ownPage) return [page];
  /* Verses in order, as many to a page as fit; a verse is never split. */
  const fullH = CONTENT.bottom - CONTENT.top, chunks = [[]];
  verses.forEach(v => {
    const last = chunks[chunks.length - 1];
    if (last.length && passageBlockHeight(last.concat([v]), notice, false, ref) > fullH) chunks.push([v]);
    else last.push(v);
  });
  const passagePages = chunks.map((part, k) => {
    const more = chunks.length > 1 ? ` (part ${k + 1})` : '';
    return {
      label: `Session ${n} · Passage${chunks.length > 1 ? ' ' + (k + 1) : ''}`,
      concept: `Session ${n} passage${more}: ${refShown}`,
      title: name ? `Session ${n}: ${name}` : `Session ${n}`,
      subtitle: k ? `${refShown}, continued.` : `${refShown}. Too long to share a page, so it has its own.`,
      theme,
      blocks: [{ x: CONTENT.left, y: CONTENT.top, w: CONTENT.full, h: fullH, title: `Read ${refShown}${more}`, color: 'sage',
        content: Object.assign({}, passageContent, { verses: part, prompt: undefined }) }],
    };
  });
  return passagePages.concat([page]);
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
    concept: `Session ${n} discussion: ${ref}`,
    title: `Session ${n}: Discuss`,
    subtitle: `${ref}. Talk these through together, and go back to the text whenever you disagree.`,
    theme,
    blocks,
  };
}

function buildStudySpec(form) {
  const title = clean(form.title) || 'Untitled study';
  const brand = clean(form.brand) || 'Simplify to Glorify';
  const theme = /^#[0-9a-f]{6}$/i.test(form.theme || '') ? form.theme : '#b2c6b1';
  const sessions = Array.isArray(form.sessions) ? form.sessions.filter(s => s && typeof s === 'object') : [];
  const pages = [];
  sessions.forEach((s, i) => {
    pages.push(...sessionPage(sessions, i, theme, clean(form.notice)));
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

if (typeof module !== 'undefined' && module.exports) module.exports = { buildStudySpec, sessionDefaults, defaultsFor, parseVerses };

/* ---------------------------------------------------------------- the page */
if (typeof document !== 'undefined') (function () {
  const $ = (s, el) => (el || document).querySelector(s), $$ = (s, el) => [...(el || document).querySelectorAll(s)];
  const KEY = 'studyStarter';
  const NOT_SAVED = 'Not saved: the browser refused to store the draft. Download the JSON to keep your work.';
  let form, timer;

  function freshSession() {
    const s = { auto: AUTO.slice() };
    TEXT_KEYS.forEach(k => { s[k] = ''; });
    return s;
  }
  function fresh() {
    return { title: '', brand: 'Simplify to Glorify', audience: '', outcome: '', theme: '#b2c6b1', notice: '', sessions: [freshSession()] };
  }
  /* A saved draft is data from an earlier visit: take only the fields the form knows, as strings. */
  function adopt(saved) {
    if (!saved || typeof saved !== 'object' || Array.isArray(saved)) return null;
    const f = fresh();
    ['title', 'brand', 'audience', 'outcome', 'theme', 'notice'].forEach(k => { if (typeof saved[k] === 'string') f[k] = saved[k]; });
    const sessions = (Array.isArray(saved.sessions) ? saved.sessions : []).filter(s => s && typeof s === 'object' && !Array.isArray(s)).map(s => {
      const t = freshSession();
      TEXT_KEYS.forEach(k => { if (typeof s[k] === 'string') t[k] = s[k]; });
      t.auto = Array.isArray(s.auto) ? s.auto.filter(k => AUTO.includes(k)) : AUTO.filter(k => !clean(t[k]));
      return t;
    });
    if (sessions.length) f.sessions = sessions;
    return f;
  }
  function load() {
    let saved = null, raw = null;
    try { raw = localStorage.getItem(KEY); } catch { raw = null; }
    try { saved = raw ? JSON.parse(raw) : null; } catch { saved = null; }
    form = adopt(saved) || fresh();
    if (raw && !adopt(saved)) toast('The saved draft could not be read; starting fresh');
  }
  function save() {
    clearTimeout(timer);
    $('#saved').textContent = 'Saving…';
    timer = setTimeout(() => {
      try { localStorage.setItem(KEY, JSON.stringify(form)); $('#saved').textContent = 'Saved locally'; }
      catch { $('#saved').textContent = 'Not saved'; toast(NOT_SAVED); }
    }, 250);
  }
  /* Write every session's auto fields from its defaults and show them, without redrawing the form. */
  function applyAuto() {
    form.sessions.forEach((s, i) => {
      const { defaults } = defaultsFor(form.sessions, i);
      s.auto.forEach(k => {
        s[k] = defaults[k];
        const el = $(`#s${i + 1}-${k}`);
        if (el && el.value !== s[k]) el.value = s[k];
      });
    });
  }
  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._timer); t._timer = setTimeout(() => t.classList.remove('show'), 2600);
  }
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'study'; }
  function spec() { return buildStudySpec(form); }

  function renderStudy() {
    $('#title').value = form.title; $('#brand').value = form.brand; $('#audience').value = form.audience;
    $('#outcome').value = form.outcome; $('#theme').value = form.theme; $('#notice').value = form.notice;
  }
  function renderSessions() {
    const ol = $('#sessions');
    ol.innerHTML = '';
    form.sessions.forEach((s, i) => {
      const n = i + 1;
      const li = $('#sessionRow').content.firstElementChild.cloneNode(true);
      $('.n', li).textContent = n;
      $$('[data-k]', li).forEach(el => {
        const k = el.dataset.k;
        el.id = `s${n}-${k}`;
        el.oninput = () => {
          s[k] = el.value;
          if (AUTO.includes(k)) s.auto = s.auto.filter(a => a !== k);
          if (k === 'reference') applyAuto();
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
    applyAuto();
    form.sessions.forEach((s, i) => { TEXT_KEYS.forEach(k => { const el = $(`#s${i + 1}-${k}`); if (el) el.value = s[k] || ''; }); });
  }
  function renderSpec() { $('#specView').textContent = JSON.stringify(spec(), null, 2); }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]); }
  function showFindings(findings, valid) {
    const box = $('#findings');
    if (!findings.length) { box.innerHTML = '<p class="finding good">No findings. The study validates cleanly.</p>'; return; }
    box.innerHTML = (valid ? '<p class="finding">Warnings to read; nothing stops generation.</p>' : '')
      + findings.map(f => `<p class="finding ${f.startsWith('ERROR') ? 'bad' : ''}">${esc(f)}</p>`).join('');
  }
  const OFFLINE = 'The local generator is not running. Start it with python study_studio.py and open this page from there to check, preview and download the finished HTML. The JSON download works without it.';

  async function post(path) {
    return fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(spec()) });
  }
  async function payloadOf(r) {
    try { return await r.json(); } catch { return {}; }
  }
  async function check() {
    let r;
    try { r = await post('/api/validate'); } catch { showFindings([OFFLINE], false); return null; }
    const payload = await payloadOf(r);
    if (!r.ok || !Array.isArray(payload.findings)) {
      showFindings([`ERROR: The generator could not check the study (${payload.error || `it answered ${r.status}`}).`], false);
      return null;
    }
    showFindings(payload.findings, !!payload.valid);
    return payload;
  }
  async function rendered() {
    let r;
    try { r = await post('/api/render'); } catch { showFindings([OFFLINE], false); return null; }
    if (!r.ok) {
      const payload = await payloadOf(r);
      showFindings(payload.findings || [`ERROR: ${payload.error || `The generator answered ${r.status}.`}`], false);
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
  function clearAll() {
    form = fresh();
    renderStudy(); renderSessions(); renderSpec();
    $('#findings').innerHTML = ''; $('#previewCard').hidden = true;
    try { localStorage.removeItem(KEY); $('#saved').textContent = 'Saved locally'; toast('Cleared'); }
    catch { $('#saved').textContent = 'Not saved'; toast('Cleared here, but the browser refused to forget the old draft; it may come back on refresh'); }
  }

  load();
  renderStudy();
  renderSessions();
  renderSpec();
  ['title', 'brand', 'audience', 'outcome', 'theme', 'notice'].forEach(k => {
    $('#' + k).oninput = e => { form[k] = e.target.value; save(); renderSpec(); };
  });
  $('#addSession').onclick = () => { form.sessions.push(freshSession()); renderSessions(); save(); renderSpec(); $(`#s${form.sessions.length}-reference`).focus(); };
  $('#reset').onclick = () => { if (confirm('Clear every field and start over?')) clearAll(); };
  $('#check').onclick = check;
  $('#preview').onclick = async () => {
    const html = await rendered();
    if (html === null) return;
    $('#frame').srcdoc = html; $('#previewCard').hidden = false; $('#previewCard').scrollIntoView({ behavior: 'smooth' });
    await check();
  };
  $('#html').onclick = async () => {
    const result = await check();
    if (!result) return;
    if (result.findings.some(f => f.includes('will not print'))) {
      toast('Some text will not fit its box. Shorten it, or split the passage across sessions, before downloading.');
      return;
    }
    const html = await rendered();
    if (html === null) return;
    download(new Blob([html], { type: 'text/html' }), slug(form.title || 'study') + '.html');
  };
  $('#json').onclick = () => download(new Blob([JSON.stringify(spec(), null, 2)], { type: 'application/json' }), slug(form.title || 'study') + '.json');
  $('#study').onsubmit = e => { e.preventDefault(); check(); };
})();

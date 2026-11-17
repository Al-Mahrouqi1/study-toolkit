(()=>{'use strict';
const PRISTINE='<!DOCTYPE html>\n'+document.documentElement.outerHTML;
const ROOT=document.querySelector('main')||document.body;
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const E=(tag,attrs={},html='')=>{const e=document.createElement(tag);for(const k in attrs)e.setAttribute(k,attrs[k]);e.innerHTML=html;return e};
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const KEY='tk:'+(($('meta[name=tk-id]')||{}).content||location.pathname+'|'+document.title);
const P={menu:'<path d="M4 6h16M4 12h16M4 18h10"/>',search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 lang:'<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
 notes:'<path d="M15.5 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.5L15.5 3Z"/><path d="M15 3v6h6"/>',
 moon:'<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 dl:'<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/>',x:'<path d="M18 6 6 18M6 6l12 12"/>',
 vol:'<path d="M11 5 6 9H2v6h4l5 4V5Z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>',
 pin:'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 pen:'<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',trash:'<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/>',
 copy:'<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/>',
 star:'<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9Z"/>',up:'<path d="m18 15-6-6-6 6"/>',down:'<path d="m6 9 6 6 6-6"/>',
 check:'<path d="M20 6 9 17l-5-5"/>',eraser:'<path d="m7 21-4.3-4.3a1 1 0 0 1 0-1.4l10-10a1 1 0 0 1 1.4 0l5.6 5.6a1 1 0 0 1 0 1.4L11 21"/><path d="M22 21H7"/><path d="m5 11 9 9"/>',
 under:'<path d="M6 4v6a6 6 0 0 0 12 0V4"/><path d="M4 20h16"/>',undo:'<path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
 fm:'<path d="M2 19 7.5 5h1L14 19"/><path d="M4.3 14h7.4"/><path d="M16 12h6"/>',fp:'<path d="M2 19 7.5 5h1L14 19"/><path d="M4.3 14h7.4"/><path d="M16 12h6M19 9v6"/>',
 alert:'<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>',go:'<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
 ok:'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',bad:'<circle cx="12" cy="12" r="9"/><path d="m15 9-6 6M9 9l6 6"/>',
 eye:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',reset:'<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
 hl:'<path d="m9 11-6 6v3h9l3-3"/><path d="m22 12-4.6 4.6a2 2 0 0 1-2.8 0l-5.2-5.2a2 2 0 0 1 0-2.8L14 4"/>',info:'<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>'};
const I=(n,s=18)=>`<svg class="tk-i" viewBox="0 0 24 24" width="${s}" height="${s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[n]}</svg>`;
const COLORS=[['y','أصفر'],['g','أخضر'],['b','أزرق'],['p','وردي'],['u','تسطير']];
let S={v:2,saved:0,hl:[],words:[],done:{},quiz:{},font:null,theme:null,toc:null};
try{const a=JSON.parse(localStorage.getItem(KEY)||'null');const t=$('#tk-data');const b=t&&t.textContent.trim()?JSON.parse(t.textContent):null;
  const p=a&&b?(a.saved>=b.saved?a:b):(a||b);if(p)S=Object.assign(S,p);}catch(e){}
let sT;const flush=()=>{clearTimeout(sT);try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){toast('تعذّر الحفظ في المتصفح — استخدم زر التصدير')}};
const save=()=>{S.saved=Date.now();clearTimeout(sT);sT=setTimeout(flush,200)};addEventListener('pagehide',flush);addEventListener('visibilitychange',()=>{if(document.hidden)flush()});
function toast(m,opt={}){const t=$('#tk-toast');t.innerHTML=`${I(opt.icon||'info',18)}<span>${esc(m)}</span>`+(opt.undo?`<button>${I('undo',16)} تراجع</button>`:'');
  if(opt.undo)$('button',t).onclick=()=>{undo();t.classList.remove('on')};t.classList.add('on');clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('on'),opt.ms||(opt.undo?6000:2600))}

/* ---------- text offsets ---------- */
const nodes=()=>{const o=[],w=document.createTreeWalker(ROOT,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.parentElement.closest('.tk-x,.tk-ui,script,style,textarea,button')?2:1});let n;while(n=w.nextNode())o.push(n);return o};
const fullText=()=>nodes().map(n=>n.data).join('');
function offsets(r){let p=0,s=-1,e=-1;for(const n of nodes()){const L=n.length;if(r.intersectsNode(n)){const a=n===r.startContainer?r.startOffset:0,b=n===r.endContainer?r.endOffset:L;if(b>a){if(s<0)s=p+a;e=p+b}}p+=L}return s<0?null:[s,e]}
function wrap(s,e,make){const seg=[];let p=0;for(const n of nodes()){const L=n.length,a=Math.max(s,p),b=Math.min(e,p+L);if(b>a)seg.push([n,a-p,b-p]);p+=L;if(p>=e)break}
  const out=[];for(const[n,a,b]of seg){if(seg.length>1&&!n.data.slice(a,b).trim())continue;const m=a?n.splitText(a):n;if(b-a<m.length)m.splitText(b-a);const w=make();m.parentNode.insertBefore(w,m);w.appendChild(m);out.push(w)}return out}
function unwrap(el){const p=el.parentNode;if(!p)return;while(el.firstChild)p.insertBefore(el.firstChild,el);p.removeChild(el);p.normalize()}
const offsetEl=o=>{let p=0;for(const n of nodes()){if(p+n.length>o)return n.parentElement;p+=n.length}return ROOT};
const isW=c=>!!c&&/[\p{L}\p{N}\p{M}_'’-]/u.test(c);
function snap(s,e,T){while(s<e&&/\s/.test(T[s]))s++;while(e>s&&/\s/.test(T[e-1]))e--;while(s>0&&isW(T[s-1])&&isW(T[s]))s--;while(e<T.length&&isW(T[e-1])&&isW(T[e]))e++;return[s,e]}

/* ---------- source ---------- */
function source(el){if(!el)return{};if(el.nodeType!==1)el=el.parentElement;
  const chap=(($('meta[name=chapter]')||{}).content)||(($('h1')||{}).firstChild||{}).textContent||document.title;
  const sec=el.closest('section');const ttl=sec&&($('h2 .te',sec)||$('h2',sec));
  let where=(el.closest('[data-src]')||{}).dataset?.src||'';
  if(!where){const fx=el.closest('figure,.explain');const f=fx&&(fx.tagName==='FIGURE'?fx:fx.previousElementSibling);const fs=f&&f.querySelector&&f.querySelector('figcaption .src');
    if(fs)where=fs.textContent.trim();else{const sl=sec&&($('.slides span[dir=ltr]',sec)||$('.slides',sec));if(sl)where=sl.textContent.trim()}}
  return{chap:(chap||'').trim(),sec:sec&&sec.id,title:ttl?ttl.textContent.trim():'',where}}
const srcLine=s=>[s.chap,s.title,s.where].filter(Boolean).map(esc).join(' › ');

/* ---------- UI shell ---------- */
const B=(k,ic,t)=>`<button data-b="${k}" title="${t}" aria-label="${t}">${I(ic,19)}</button>`;
document.body.append(
  E('div',{id:'tk-progress',class:'tk-ui'}),
  E('div',{id:'tk-bar',class:'tk-ui',role:'toolbar'},B('toc','menu','الفهرس')+B('find','search','بحث  ( / )')+B('tr','lang','الترجمة')+B('notes','notes','التحديدات والملاحظات')+B('draw','draw','الرسم: قلم، تظليل، نص، ممحاة (D)')+B('board','board','السبورة (B)')+'<span class="sep"></span>'+B('fm','fm','تصغير الخط')+B('fp','fp','تكبير الخط')+B('theme','moon','الوضع الليلي')+B('exp','dl','تنزيل نسخة فيها تحديداتك وملاحظاتك')),
  E('aside',{id:'tk-toc',class:'tk-ui',dir:'rtl'},`<header><b>الفهرس</b><div class="tk-meter"><i></i></div><small class="pc"></small></header><div class="list" dir="ltr"></div>`),
  E('aside',{id:'tk-panel',class:'tk-ui',dir:'rtl'},`<header><nav><button data-tab=tr>${I('lang',16)} الترجمة</button><button data-tab=notes>${I('notes',16)} الملاحظات</button><button data-tab=find>${I('search',16)} البحث</button></nav><button class="x" title="إغلاق (Esc)">${I('x',18)}</button></header>
   <div class="tab" data-tab="tr"><div class="tk-inw">${I('lang',18)}<input class="tk-in" id="tk-trin" dir="auto" placeholder="اكتب كلمة أو جملة ثم Enter"></div><div id="tk-trout"></div><div class="tk-h"><span>${I('star',16)} كلماتي المحفوظة</span><button class="tk-ib" id="tk-wexp" title="تنزيل القائمة">${I('dl',17)}</button></div><div id="tk-words"></div></div>
   <div class="tab" data-tab="notes"><div class="tk-filters" id="tk-nf"></div><div id="tk-notes"></div><div class="tk-row tk-foot"><button class="tk-btn" id="tk-nexp">${I('dl',16)} تنزيل كنص</button><button class="tk-btn dang" id="tk-nclr">${I('trash',16)} مسح الكل</button></div></div>
   <div class="tab" data-tab="find"><div class="tk-inw">${I('search',18)}<input class="tk-in" id="tk-fin" dir="auto" placeholder="ابحث في الملخص… Search"></div><div class="tk-row" id="tk-fnav"></div><div id="tk-fres"></div></div>`),
  E('div',{id:'tk-pop',class:'tk-ui',dir:'rtl',role:'toolbar'}),E('div',{id:'tk-toast',class:'tk-ui',role:'status'}));
const pop=$('#tk-pop');

/* ---------- look / progress ---------- */
const applyLook=()=>{setTimeout(()=>window.__tkInk&&window.__tkInk(),60);document.documentElement.style.fontSize=S.font?S.font+'px':'';document.documentElement.dataset.theme=S.theme||'light';$('[data-b=theme]').innerHTML=I(S.theme==='dark'?'sun':'moon',19)};
const scrollBar=()=>{const d=document.documentElement,m=d.scrollHeight-d.clientHeight;$('#tk-progress').style.width=(m>0?d.scrollTop/m*100:0)+'%'};
addEventListener('scroll',scrollBar,{passive:true});

/* ---------- TOC ---------- */
const secs=$$('section[id]',ROOT).filter(s=>$('h2',s));
function buildToc(){const L=$('#tk-toc .list');L.innerHTML='';
  secs.forEach(s=>{const n=($('h2 .n',s)||{}).textContent,t=($('h2 .te',s)||$('h2',s)).textContent.trim();
    const it=E('div',{class:'it','data-id':s.id},`<button class="ck" title="أنهيت هذا القسم">${I('check',13)}</button><a href="#${s.id}">${n?esc(n)+'. ':''}${esc(t)}</a>`);
    const set=()=>it.classList.toggle('done',!!S.done[s.id]);set();$('.ck',it).onclick=()=>{if(S.done[s.id])delete S.done[s.id];else S.done[s.id]=true;set();meter();save()};L.append(it);
    $$('h3',s).forEach((h,i)=>{if(!h.id)h.id=s.id+'-'+(i+1);const tx=(h.firstChild&&h.firstChild.nodeType===3?h.firstChild.textContent:h.textContent).trim();L.append(E('a',{class:'sub',href:'#'+h.id},esc(tx)))})});meter();
  if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)$$('#tk-toc .it').forEach(i=>i.classList.toggle('active',i.dataset.id===e.target.id))}),{rootMargin:'-30% 0px -60% 0px'});secs.forEach(s=>io.observe(s))}}
function meter(){const d=secs.filter(s=>S.done[s.id]).length;$('#tk-toc .tk-meter i').style.width=(secs.length?d/secs.length*100:0)+'%';$('#tk-toc .pc').textContent=`أنهيت ${d} من ${secs.length} أقسام`}
const toggleToc=v=>{document.body.classList.toggle('tk-toc-open',v);$('[data-b=toc]').classList.toggle('on',document.body.classList.contains('tk-toc-open'))};

/* ---------- panel ---------- */
function openPanel(tab){document.body.classList.add('tk-panel-open');$$('#tk-panel nav button').forEach(b=>b.classList.toggle('on',b.dataset.tab===tab));$$('#tk-panel .tab').forEach(t=>t.classList.toggle('on',t.dataset.tab===tab));
  $$('#tk-bar [data-b=tr],#tk-bar [data-b=notes],#tk-bar [data-b=find]').forEach(b=>b.classList.toggle('on',b.dataset.b===tab));if(tab==='notes')renderNotes();if(tab==='tr')renderWords()}
const closePanel=()=>{document.body.classList.remove('tk-panel-open');$$('#tk-bar [data-b=tr],#tk-bar [data-b=notes],#tk-bar [data-b=find]').forEach(b=>b.classList.remove('on'))};
const panelOpen=()=>document.body.classList.contains('tk-panel-open');
$$('#tk-panel nav button').forEach(b=>b.onclick=()=>openPanel(b.dataset.tab));$('#tk-panel .x').onclick=closePanel;

/* ---------- speech / copy ---------- */
function say(t){if(!('speechSynthesis'in window))return toast('النطق غير مدعوم في هذا المتصفح',{icon:'alert'});speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(t);const ar=/[؀-ۿ]/.test(t);u.lang=ar?'ar-SA':'en-US';u.rate=.92;
  const vs=speechSynthesis.getVoices(),v=vs.find(v=>v.lang.startsWith(ar?'ar':'en-US'))||vs.find(v=>v.lang.startsWith(ar?'ar':'en'));if(v)u.voice=v;speechSynthesis.speak(u)}
function copy(t){(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>toast('تم النسخ',{icon:'check'}),()=>{const a=E('textarea');a.value=t;document.body.append(a);a.select();document.execCommand('copy');a.remove();toast('تم النسخ',{icon:'check'})})}

/* ---------- translation ---------- */
const tmo=(u,ms=6000)=>{const c=new AbortController(),t=setTimeout(()=>c.abort(),ms);return fetch(u,{signal:c.signal}).finally(()=>clearTimeout(t))};
async function gtx(q,tl){const r=await tmo('https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl='+tl+'&dt=t&q='+encodeURIComponent(q));if(!r.ok)throw 0;const j=await r.json();return j[0].map(x=>x[0]).join('')}
async function mym(q,tl,sl){const r=await tmo('https://api.mymemory.translated.net/get?q='+encodeURIComponent(q.slice(0,480))+'&langpair='+sl+'|'+tl);const j=await r.json();const t=j&&j.responseData&&j.responseData.translatedText;if(!t||/MYMEMORY WARNING|INVALID/i.test(t))throw 0;return t}
async function lgv(q,tl){const r=await tmo('https://lingva.ml/api/v1/auto/'+tl+'/'+encodeURIComponent(q.slice(0,1000)));if(!r.ok)throw 0;const j=await r.json();if(!j.translation)throw 0;return j.translation}
async function online(q,tl,sl){for(const f of[()=>gtx(q,tl),()=>mym(q,tl,sl),()=>lgv(q,tl)]){try{const t=await f();if(t)return t}catch(e){}}return ''}
async function dict(w){try{const r=await tmo('https://api.dictionaryapi.dev/api/v2/entries/en/'+encodeURIComponent(w.toLowerCase()));if(!r.ok)return null;return (await r.json())[0]}catch(e){return null}}
let GL={};try{const g=$('#tk-gloss');if(g)for(const[k,v]of Object.entries(JSON.parse(g.textContent)))GL[k.toLowerCase().trim()]=v}catch(e){}
const GLR={};for(const[k,v]of Object.entries(GL))GLR[String(v).trim()]=k;
function gloss(q){const k=q.toLowerCase().replace(/[.,;:!?()"“”]/g,'').trim();if(GL[k])return GL[k];for(const s of[k.replace(/ies$/,'y'),k.replace(/es$/,''),k.replace(/s$/,'')])if(GL[s])return GL[s];return GLR[q.trim()]||''}
function twin(el){if(!el)return '';if(el.nodeType!==1)el=el.parentElement;const p=el.closest('.e,.a');if(!p)return '';const box=p.parentElement,o=box&&$(p.classList.contains('e')?':scope > .a':':scope > .e',box);return o?o.textContent.trim():''}
let trTok=0;
async function translate(q,el){q=(q||'').replace(/\s+/g,' ').trim();if(!q)return;openPanel('tr');const tok=++trTok,ar=/[؀-ۿ]/.test(q),out=$('#tk-trout'),tl=ar?'en':'ar',src=el?source(el):null;
  const g=gloss(q),tw=twin(el);
  out.innerHTML=`<div class="tk-card"><div class="tk-q" dir="auto">${esc(q.length>400?q.slice(0,400)+'…':q)}</div>${src&&src.where?`<span class="tk-src">${I('pin',14)} ${srcLine(src)}</span>`:''}
   ${g?`<div class="tk-tag">${I('star',13)} من مسرد الفصل</div><div class="tk-ans" dir="${ar?'ltr':'rtl'}">${esc(g)}</div>`:''}
   <div class="tk-on">${g?'<div class="tk-tag">ترجمة آلية</div>':''}<div class="tk-ans${g?' sm':''}" dir="${ar?'ltr':'rtl'}"><span class="tk-load"></span></div></div><div class="tk-row"></div><div class="tk-dict" dir="ltr"></div>
   ${tw&&tw!==q?`<details class="tk-twin"><summary>${I('lang',14)} المقابل في الملخص</summary><p dir="auto">${esc(tw)}</p></details>`:''}</div>`;
  const t=await online(q,tl,ar?'ar':'en');if(tok!==trTok)return;const box=$('.tk-on',out),final=t||g,en=ar?(final||''):q,arT=ar?q:(final||'');
  if(!t){const gt='https://translate.google.com/?sl=auto&tl='+tl+'&op=translate&text='+encodeURIComponent(q.slice(0,4000));
    box.innerHTML=`<div class="tk-err">${I('alert',17)} الترجمة الآلية غير متاحة ${top!==self?'— الملف مفتوح داخل معاينة تمنع الاتصال، افتحه في المتصفح مباشرة':'— تحقّق من الاتصال بالإنترنت'}</div><a class="tk-btn" href="${gt}" target="_blank" rel="noopener">${I('go',15)} افتح في Google Translate</a>`}
  else $('.tk-ans',box).textContent=t;
  const row=$('.tk-row',out);row.innerHTML=`<button class="tk-btn">${I('vol',16)} نطق</button>${final?`<button class="tk-btn pri">${I('star',16)} احفظ</button><button class="tk-btn">${I('copy',16)} نسخ</button>`:''}`;
  const rb=$$('button',row);rb[0].onclick=()=>say(ar&&!final?q:en||q);
  if(final){rb[2].onclick=()=>copy(final);rb[1].onclick=()=>{if(!S.words.some(w=>w.en.toLowerCase()===en.toLowerCase()))S.words.unshift({en,ar:arT,src:src?src.where:'',t:Date.now()});save();renderWords();rb[1].innerHTML=I('check',16)+' محفوظة';rb[1].disabled=true}}
  if(/^[A-Za-z][A-Za-z'-]*$/.test(en)&&en.length<30){const d=await dict(en);if(tok!==trTok||!d)return;const ph=(d.phonetics||[]).find(p=>p.text);
    let h=ph?`<div class="tk-ph">${esc(ph.text)}</div>`:'';(d.meanings||[]).slice(0,3).forEach(m=>{const df=(m.definitions||[])[0];if(df)h+=`<div class="tk-def"><i>${esc(m.partOfSpeech)}</i> — ${esc(df.definition)}</div>`});
    $('.tk-dict',out).innerHTML=h?`<div class="tk-dh">Dictionary</div>`+h:''}}
$('#tk-trin').addEventListener('keydown',e=>{if(e.key==='Enter')translate(e.target.value)});
function renderWords(){const b=$('#tk-words');b.innerHTML=S.words.length?'':'<div class="tk-empty">احفظ الكلمات من الترجمة لتراجعها هنا.</div>';
  S.words.forEach((w,i)=>{const r=E('div',{class:'tk-word'},`<button class="tk-ib" title="نطق">${I('vol',16)}</button><span class="en" dir="ltr">${esc(w.en)}</span><span class="ar" dir="auto">${esc(w.ar)}</span><button class="tk-ib" title="حذف">${I('x',15)}</button>`);
    const bb=$$('button',r);bb[0].onclick=()=>say(w.en);bb[1].onclick=()=>{S.words.splice(i,1);save();renderWords()};b.append(r)})}
const download=(name,text,type='text/plain')=>{const a=E('a',{href:URL.createObjectURL(new Blob([text],{type:type+';charset=utf-8'})),download:name});document.body.append(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500)};
const baseName=()=>(decodeURIComponent(location.pathname.split('/').pop()||'summary').replace(/\.html?$/i,'')||'summary').replace(/_annotated$/,'');
$('#tk-wexp').onclick=()=>download(baseName()+'_words.txt',S.words.map(w=>`${w.en} — ${w.ar}${w.src?'  ('+w.src+')':''}`).join('\n'));

/* ---------- highlights ---------- */
const marks=id=>$$(`mark.tk-hl[data-id="${id}"]`);
const newId=()=>'h'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
function paint(h){const ms=wrap(h.s,h.e,()=>E('mark',{class:'tk-hl','data-c':h.c,'data-id':h.id}));ms.forEach((m,i)=>{m.classList.toggle('has-note',!!h.n);if(i===ms.length-1)m.classList.add('tk-last');m.title=h.n||''});return ms.length}
function restore(){const txt=fullText();S.hl.forEach(h=>{if(txt.slice(h.s,h.e)!==h.t){const i=txt.indexOf(h.t);if(i>=0){h.s=i;h.e=i+h.t.length}else{h.lost=1;return}}delete h.lost;paint(h)})}
function repaintAll(){$$('mark.tk-hl').forEach(unwrap);restore()}
const hist=[];const snapshot=()=>{hist.push(JSON.stringify(S.hl));if(hist.length>40)hist.shift()};
function undo(){if(!hist.length)return toast('لا يوجد ما يمكن التراجع عنه');S.hl=JSON.parse(hist.pop());repaintAll();save();if(panelOpen())renderNotes();toast('تم التراجع',{icon:'undo'})}
const overlaps=(s,e)=>S.hl.filter(h=>!h.lost&&h.s<e&&h.e>s);
function addHl(range,c){const o=offsets(range);if(!o)return null;const T=fullText();let[s,e]=snap(o[0],o[1],T);if(e<=s)return null;
  snapshot();const touch=S.hl.filter(h=>!h.lost&&h.s<=e&&h.e>=s);let n='';
  touch.forEach(h=>{s=Math.min(s,h.s);e=Math.max(e,h.e);if(h.n)n+=(n?'\n':'')+h.n;marks(h.id).forEach(unwrap)});
  S.hl=S.hl.filter(h=>!touch.includes(h));const h={id:touch[0]?touch[0].id:newId(),s,e,c,n,t:T.slice(s,e)};
  if(!paint(h)){hist.pop();return null}S.hl.push(h);save();if(panelOpen())renderNotes();return h}
const trim=(a,b,T)=>{while(a<b&&/\s/.test(T[a]))a++;while(b>a&&/\s/.test(T[b-1]))b--;return[a,b]};
function erase(range){const o=offsets(range);if(!o)return;const T=fullText(),[s,e]=snap(o[0],o[1],T),hit=overlaps(s,e);if(!hit.length)return;snapshot();
  hit.forEach(h=>{marks(h.id).forEach(unwrap);S.hl=S.hl.filter(x=>x!==h);let first=true;
    [[h.s,s],[e,h.e]].forEach(([a,b])=>{if(b<=a)return;[a,b]=trim(a,b,T);if(b<=a)return;const p={id:first?h.id:newId(),s:a,e:b,c:h.c,n:first?h.n:'',t:T.slice(a,b)};first=false;S.hl.push(p);paint(p)})});
  save();if(panelOpen())renderNotes();toast('أُزيل التحديد من الجزء المختار',{icon:'eraser',undo:true})}
function delHl(id,quiet){snapshot();marks(id).forEach(unwrap);S.hl=S.hl.filter(h=>h.id!==id);save();if(panelOpen())renderNotes();if(!quiet)toast('حُذف التحديد',{icon:'trash',undo:true})}
function recolor(id,c){const h=S.hl.find(x=>x.id===id);if(!h||h.c===c)return;snapshot();h.c=c;marks(id).forEach(m=>m.dataset.c=c);save();if(panelOpen())renderNotes()}
function jump(el){if(!el)return;el.scrollIntoView({behavior:'smooth',block:'center'});const g=el.matches('mark.tk-hl')?marks(el.dataset.id):[el];g.forEach(x=>{x.classList.remove('tk-flash');void x.offsetWidth;x.classList.add('tk-flash')})}
ROOT.addEventListener('mouseover',e=>{const m=e.target.closest('mark.tk-hl');if(m)marks(m.dataset.id).forEach(x=>x.classList.add('hov'))});
ROOT.addEventListener('mouseout',e=>{const m=e.target.closest('mark.tk-hl');if(m)marks(m.dataset.id).forEach(x=>x.classList.remove('hov'))});

/* ---------- notes panel ---------- */
let nFilter='all';
function renderNotes(focusId){const f=$('#tk-nf'),b=$('#tk-notes');const all=[...S.hl].sort((a,b)=>a.s-b.s);
  const cnt=k=>k==='all'?all.length:k==='n'?all.filter(h=>h.n).length:all.filter(h=>h.c===k).length;
  f.innerHTML=[['all','الكل'],['n','بملاحظة'],...COLORS].filter(([k])=>k==='all'||cnt(k)).map(([k,l])=>`<button data-f="${k}" class="${nFilter===k?'on':''}">${k.length===1&&k!=='n'?`<i class="sw ${k}"></i>`:''}${l} <small>${cnt(k)}</small></button>`).join('');
  $$('button',f).forEach(x=>x.onclick=()=>{nFilter=x.dataset.f;renderNotes()});
  const list=all.filter(h=>nFilter==='all'||(nFilter==='n'?h.n:h.c===nFilter));
  b.innerHTML=list.length?'':`<div class="tk-empty">${I('hl',28)}<p>حدّد أي نص في الصفحة واختر لونًا، أو اضغط <b>ملاحظة</b> لتكتب عليه.</p></div>`;
  list.forEach(h=>{const m=marks(h.id)[0],s=source(m||offsetEl(h.s));const it=E('div',{class:'tk-item','data-c':h.c},
    `<div class="hd"><span class="sw ${h.c}"></span>${h.lost?`<span class="tk-src warn">${I('alert',14)} لم يُعثر على النص في الصفحة</span>`:`<span class="tk-src">${I('pin',14)} ${[s.title,s.where].filter(Boolean).map(esc).join(' › ')}</span>`}
     <span class="acts"><button class="tk-ib" data-a="go" title="انتقال">${I('go',16)}</button><button class="tk-ib" data-a="tr" title="ترجمة">${I('lang',16)}</button><button class="tk-ib" data-a="del" title="حذف">${I('trash',16)}</button></span></div>
     <blockquote dir="auto">${esc(h.t.length>240?h.t.slice(0,240)+'…':h.t)}</blockquote><textarea dir="auto" rows="1" placeholder="أضف ملاحظة…"></textarea>`);
    const ta=$('textarea',it);ta.value=h.n||'';const fit=()=>{ta.style.height='auto';ta.style.height=ta.scrollHeight+2+'px'};
    ta.oninput=()=>{h.n=ta.value;marks(h.id).forEach(x=>{x.classList.toggle('has-note',!!h.n);x.title=h.n});fit();save()};
    it.querySelector('[data-a=go]').onclick=()=>jump(marks(h.id)[0]);it.querySelector('[data-a=tr]').onclick=()=>translate(h.t,m);it.querySelector('[data-a=del]').onclick=()=>delHl(h.id);
    $('blockquote',it).onclick=()=>jump(marks(h.id)[0]);b.append(it);setTimeout(fit,0);
    if(focusId===h.id)setTimeout(()=>{it.scrollIntoView({block:'nearest',behavior:'smooth'});it.classList.add('focus');ta.focus()},280)})}
$('#tk-nclr').onclick=()=>{if(!S.hl.length)return;snapshot();$$('mark.tk-hl').forEach(unwrap);S.hl=[];save();renderNotes();toast('مُسحت كل التحديدات',{icon:'trash',undo:true})};
$('#tk-nexp').onclick=()=>{const L=[...S.hl].sort((a,b)=>a.s-b.s).map(h=>{const s=source(marks(h.id)[0]||offsetEl(h.s));return `• ${h.t}\n  [${[s.title,s.where].filter(Boolean).join(' › ')}]${h.n?'\n  ملاحظة: '+h.n:''}`});download(baseName()+'_notes.txt',(document.title+'\n\n')+L.join('\n\n'))};

/* ---------- selection popup ---------- */
let selRange=null,popMark=null,popMode='';
const coarse=()=>matchMedia('(pointer:coarse)').matches;
function popHTML(mark){const h=mark&&S.hl.find(x=>x.id===mark.dataset.id);const over=!mark&&selRange&&(()=>{const o=offsets(selRange);return o&&overlaps(o[0],o[1]).length})();
  const sw=COLORS.map(([c,l],i)=>`<button class="sw ${c}${h&&h.c===c?' on':''}" data-a="c" data-c="${c}" title="${l}  (${i+1})" aria-label="${l}">${c==='u'?I('under',15):h&&h.c===c?I('check',14):''}</button>`).join('');
  const ib=(a,ic,t,k)=>`<button class="ib" data-a="${a}" title="${t}${k?'  ('+k+')':''}" aria-label="${t}">${I(ic,18)}<span>${t}</span></button>`;
  return `<div class="row sws">${sw}</div><div class="row">${ib('note','pen',h&&h.n?'تعديل الملاحظة':'ملاحظة','N')}${ib('tr','lang','ترجمة','T')}${ib('say','vol','نطق')}${ib('copy','copy','نسخ','C')}${ib('src','pin','المصدر')}${ib('board','addb','للسبورة')}${mark?ib('del','trash','إزالة','Del'):over?ib('erase','eraser','مسح التحديد','Del'):''}</div><div class="info" hidden></div>`}
function place(rect){const w=pop.offsetWidth,h=pop.offsetHeight;let top=coarse()?rect.bottom+12:rect.top-h-12;if(top<8)top=rect.bottom+12;if(top+h>innerHeight-8)top=Math.max(8,rect.top-h-12);
  top=Math.max(8,Math.min(top,innerHeight-h-8));let left=rect.left+rect.width/2-w/2;left=Math.max(8,Math.min(left,innerWidth-w-8));pop.style.top=top+'px';pop.style.left=left+'px'}
function showPop(rect,mode){popMode=mode;$$('mark.tk-hl.sel').forEach(x=>x.classList.remove('sel'));if(popMark)marks(popMark.dataset.id).forEach(x=>x.classList.add('sel'));
  pop.innerHTML=popHTML(mode==='mark'?popMark:null);pop.classList.add('on');place(rect)}
const hidePop=()=>{pop.classList.remove('on');popMode='';popMark=null;$$('mark.tk-hl.sel').forEach(x=>x.classList.remove('sel'))};
const okNode=n=>{const el=n&&(n.nodeType===1?n:n.parentElement);return el&&ROOT.contains(el)&&!el.closest('.tk-x,.tk-ui,textarea,input,button')};
function checkSel(){const s=getSelection();if(!s.rangeCount||s.isCollapsed){if(popMode==='sel')hidePop();return}
  const r=s.getRangeAt(0);if(!okNode(r.startContainer)||!okNode(r.endContainer)||!s.toString().trim())return;selRange=r.cloneRange();popMark=null;showPop(r.getBoundingClientRect(),'sel')}
let selT;document.addEventListener('mouseup',e=>{if(!pop.contains(e.target))setTimeout(checkSel,10)});
document.addEventListener('keyup',e=>{if(e.shiftKey&&!popMode)checkSel()});
document.addEventListener('selectionchange',()=>{clearTimeout(selT);selT=setTimeout(()=>{const s=getSelection();if(s.isCollapsed){if(popMode==='sel')hidePop()}else if(coarse())checkSel()},350)});
pop.addEventListener('mousedown',e=>e.preventDefault());
ROOT.addEventListener('click',e=>{const m=e.target.closest('mark.tk-hl');if(!m||!getSelection().isCollapsed)return;popMark=m;const r=marks(m.dataset.id).map(x=>x.getBoundingClientRect()).find(r=>r.bottom>0)||m.getBoundingClientRect();showPop(r,'mark')});
document.addEventListener('mousedown',e=>{if(popMode&&!pop.contains(e.target)&&!e.target.closest('mark.tk-hl'))hidePop()});
addEventListener('scroll',()=>{if(popMode==='mark')hidePop()},{passive:true});
function act(a,b){const h=popMark?S.hl.find(x=>x.id===popMark.dataset.id):null;let text=h?h.t:'';if(!h&&selRange){const o=offsets(selRange),T=fullText();if(o){const[x,y]=snap(o[0],o[1],T);text=T.slice(x,y)}else text=selRange.toString().trim()}const anchorEl=popMark||(selRange&&selRange.startContainer);
  const done=()=>{getSelection().removeAllRanges();hidePop()};
  if(a==='c'){if(h){recolor(h.id,b.dataset.c);showPop(popMark.getBoundingClientRect(),'mark')}else{addHl(selRange,b.dataset.c);done()}}
  else if(a==='note'){const t=h||addHl(selRange,'y');done();if(t){openPanel('notes');renderNotes(t.id)}}
  else if(a==='tr'){translate(text,anchorEl);done()}
  else if(a==='say')say(text);
  else if(a==='copy'){copy(text);done()}
  else if(a==='src'){const s=source(anchorEl),i=$('.info',pop);i.hidden=false;i.innerHTML=I('pin',15)+' '+(srcLine(s)||'لا يوجد مرجع لهذا الجزء');place((popMark||selRange).getBoundingClientRect())}
  else if(a==='board'){openBoard(text);done()}
  else if(a==='del'&&h){delHl(h.id);done()}
  else if(a==='erase'){erase(selRange);done()}}
pop.addEventListener('click',e=>{const b=e.target.closest('button');if(b)act(b.dataset.a,b)});

/* ---------- search ---------- */
let found=[],cur=-1,fT;
function clearFind(){$$('mark.tk-find').forEach(unwrap);found=[];cur=-1}
function doFind(q){clearFind();const res=$('#tk-fres'),nav=$('#tk-fnav');res.innerHTML='';nav.innerHTML='';q=q.trim();if(q.length<2)return;
  const txt=fullText(),low=txt.toLowerCase(),ql=q.toLowerCase(),idx=[];let i=low.indexOf(ql);while(i>=0&&idx.length<300){idx.push(i);i=low.indexOf(ql,i+ql.length)}
  idx.reverse().forEach(i=>{const ms=wrap(i,i+q.length,()=>E('mark',{class:'tk-find'}));if(ms[0])found.unshift({el:ms[0],i})});
  const nh=S.hl.filter(h=>h.n&&h.n.toLowerCase().includes(ql));
  nav.innerHTML=`<span class="tk-q" id="tk-fc">${found.length?found.length+' نتيجة':'لا توجد نتائج'}${nh.length?' · '+nh.length+' في ملاحظاتك':''}</span>`+(found.length?`<span class="grow"></span><button class="tk-ib" title="السابق (Shift+Enter)">${I('up',18)}</button><button class="tk-ib" title="التالي (Enter)">${I('down',18)}</button>`:'');
  const nb=$$('button',nav);if(nb[0]){nb[0].onclick=()=>go(cur-1);nb[1].onclick=()=>go(cur+1)}
  const rx=new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi');
  nh.forEach(h=>{const b=E('button',{class:'tk-res'},`<span class="tk-src">${I('pen',14)} في ملاحظتك</span><span dir="auto">${esc(h.n).replace(rx,m=>`<b>${m}</b>`)}</span>`);b.onclick=()=>jump(marks(h.id)[0]);res.append(b)});
  found.slice(0,120).forEach((f,k)=>{const s=source(f.el),a=Math.max(0,f.i-45),sn=esc(txt.slice(a,f.i))+'<b>'+esc(txt.slice(f.i,f.i+q.length))+'</b>'+esc(txt.slice(f.i+q.length,f.i+q.length+60));
    const b=E('button',{class:'tk-res'},`<span class="tk-src">${I('pin',14)} ${[s.title,s.where].filter(Boolean).map(esc).join(' › ')}</span><span dir="auto">${a?'…':''}${sn}…</span>`);b.onclick=()=>go(k);res.append(b)});
  if(found.length>120)res.append(E('div',{class:'tk-empty'},'تُعرض أول 120 نتيجة — استخدم الأسهم للباقي'))}
function go(k){if(!found.length)return;cur=(k+found.length)%found.length;found.forEach(f=>f.el.classList.remove('cur'));const el=found[cur].el;el.classList.add('cur');el.scrollIntoView({behavior:'smooth',block:'center'});
  $$('#tk-fres .tk-res').forEach(x=>x.classList.remove('on'));const c=$('#tk-fc');if(c)c.textContent=`${cur+1} من ${found.length}`}
$('#tk-fin').addEventListener('input',e=>{clearTimeout(fT);fT=setTimeout(()=>doFind(e.target.value),250)});
$('#tk-fin').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go(e.shiftKey?cur-1:cur+1)}});

/* ---------- quiz ---------- */
const QEN=(($('meta[name=tk-quiz-lang]')||{}).content||'')==='en',L2=(ar,en)=>QEN?en:ar;
function initQuiz(){$$('.quiz',ROOT).forEach((qz,qi)=>{const qs=$$('.q',qz);if(!qs.length)return;const K='m'+qi;
  const board=E('div',{class:'tk-x tk-score',dir:QEN?'ltr':'rtl'});qs[0].before(board);
  const mode=()=>S.quiz[K]||qz.dataset.mode||'instant',submitted=()=>!!S.quiz['sub'+qi];
  const st=id=>S.quiz[id]||(S.quiz[id]={});const correct=(q,v)=>String(v)===String(q.dataset.answer);
  function render(){let ok=0,bad=0,tot=qs.length,ans=0;
    qs.forEach(q=>{const id=q.dataset.qid,s=S.quiz[id]||{},t=q.dataset.type;const has=t==='essay'?!!s.shown:s.pick!==undefined;if(has)ans++;
      const rev=has&&(mode()==='instant'||submitted());q.classList.toggle('revealed',rev);q.classList.toggle('locked',rev);
      const items=t==='mcq'?$$('ol.opts>li',q):t==='tf'?$$('.tk-tf button',q):[];
      items.forEach(it=>{const v=t==='mcq'?it.dataset.k:it.dataset.v;it.classList.toggle('picked',String(s.pick)===v);it.classList.toggle('right',rev&&correct(q,v));it.classList.toggle('wrong',rev&&String(s.pick)===v&&!correct(q,v))});
      let vd=$('.tk-verdict',q);if(!vd){vd=E('div',{class:'tk-x tk-verdict'});q.append(vd)}vd.className='tk-x tk-verdict';vd.innerHTML='';
      if(t==='essay'){const sm=$('.tk-self',q);if(sm)sm.hidden=!rev;if(rev&&s.self){s.self==='ok'?ok++:bad++;vd.classList.add(s.self);vd.innerHTML=s.self==='ok'?I('ok',20)+L2(' قيّمت إجابتك صحيحة',' You marked this correct'):I('bad',20)+L2(' قيّمت إجابتك غير مكتملة',' You marked this incomplete')}}
      else if(rev){const c=correct(q,s.pick);c?ok++:bad++;vd.classList.add(c?'ok':'bad');vd.innerHTML=c?I('ok',20)+L2(' إجابة صحيحة · Correct',' Correct'):I('bad',20)+L2(' إجابة خاطئة · Incorrect',' Incorrect')}});
    qz.classList.toggle('ar-on',!!S.quiz['ar'+qi]);
    const show=mode()==='instant'||submitted();
    board.innerHTML=`<div class="s">${show?`<span class="ok">${I('ok',18)} ${ok}</span><span class="bad">${I('bad',18)} ${bad}</span><span class="m">${L2('من','of')} ${tot}</span>${submitted()||ans===tot?`<span class="pc">${Math.round(ok/tot*100)}%</span>`:''}`:`<span class="m">${L2('أجبت عن','Answered')} ${ans} ${L2('من','of')} ${tot}</span>`}</div>
      <div class="seg" role="group"><button data-q="instant" class="${mode()==='instant'?'on':''}">${L2('تصحيح فوري','Instant feedback')}</button><button data-q="exam" class="${mode()==='exam'?'on':''}">${L2('وضع الاختبار','Exam mode')}</button></div>
      ${mode()==='exam'&&!submitted()?`<button class="tk-btn pri" data-q="sub">${I('check',16)} ${L2('تسليم وتصحيح','Submit')}</button>`:''}<button class="tk-btn" data-q="ar" title="Arabic · العربية">${S.quiz['ar'+qi]?L2('إخفاء العربية','Hide Arabic · إخفاء العربية'):L2('عرض العربية','Show Arabic · إظهار العربية')}</button><button class="tk-ib" data-q="reset" title="${L2('إعادة الاختبار','Reset')}">${I('reset',18)}</button>`}
  board.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const a=b.dataset.q;
    if(a==='ar'){S.quiz['ar'+qi]=!S.quiz['ar'+qi]}
    if(a==='instant'||a==='exam'){if(mode()===a)return;S.quiz[K]=a;delete S.quiz['sub'+qi]}
    if(a==='sub'){const left=qs.filter(q=>{const s=S.quiz[q.dataset.qid]||{};return q.dataset.type==='essay'?!s.shown:s.pick===undefined}).length;if(left&&!confirm(L2(`بقي ${left} سؤال بلا إجابة. تسليم على أي حال؟`,`${left} question(s) unanswered. Submit anyway?`)))return;S.quiz['sub'+qi]=1;toast(L2('تم التصحيح','Marked'),{icon:'check'})}
    if(a==='reset'){if(!confirm(L2('مسح إجاباتك في هذا الاختبار؟','Clear your answers in this test?')))return;qs.forEach(q=>{delete S.quiz[q.dataset.qid];const ta=$('.tk-essay',q);if(ta)ta.value=''});delete S.quiz['sub'+qi]}
    save();render()});
  qs.forEach((q,i)=>{const id=qi+'-'+i,t=q.dataset.type;q.dataset.qid=id;const qt=$('.qt',q)||q.firstElementChild;
    if(q.dataset.src){const a=E('a',{class:'tk-x tk-srcl',href:q.dataset.ref?'#'+q.dataset.ref:'#',title:L2('مصدر السؤال','Source')},I('pin',15)+' '+esc(q.dataset.src));a.onclick=e=>{e.preventDefault();if(q.dataset.ref)jump($('#'+q.dataset.ref));else toast(q.dataset.src,{icon:'pin'})};qt.append(a)}
    const pick=v=>{if(q.classList.contains('locked'))return;st(id).pick=v;save();render()};
    if(t==='mcq')$$('ol.opts>li',q).forEach((li,k)=>{li.dataset.k=k;li.tabIndex=0;li.addEventListener('click',()=>{if(getSelection().isCollapsed)pick(String(k))});li.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(String(k))}})});
    if(t==='tf'){const r=E('div',{class:'tk-x tk-tf'},`<button data-v="true">${I('check',17)} ${L2('True · صح','True')}</button><button data-v="false">${I('x',17)} ${L2('False · خطأ','False')}</button>`);qt.after(r);$$('button',r).forEach(b=>b.onclick=()=>pick(b.dataset.v))}
    if(t==='essay'){const ta=E('textarea',{class:'tk-x tk-essay',dir:'auto',placeholder:L2('Write your answer… اكتب إجابتك','Write your answer…')});ta.value=(S.quiz[id]||{}).text||'';ta.oninput=()=>{st(id).text=ta.value;save()};
      const r=E('div',{class:'tk-x tk-row'},`<button class="tk-btn pri">${I('eye',16)} ${L2('أظهر الإجابة النموذجية','Show model answer')}</button><span class="tk-self" hidden><span class="tk-q">${L2('قيّم إجابتك:','Rate yourself:')}</span><button class="tk-btn" data-s="ok">${I('ok',16)} ${L2('أصبت','Got it')}</button><button class="tk-btn" data-s="bad">${I('bad',16)} ${L2('أخطأت','Missed it')}</button></span>`);
      qt.after(ta,r);$('button.pri',r).onclick=()=>{st(id).shown=1;save();render();if(mode()==='exam'&&!submitted())toast(L2('ستظهر الإجابة النموذجية بعد التسليم','The model answer appears after you submit'))};
      $$('.tk-self button',r).forEach(b=>b.onclick=()=>{st(id).self=b.dataset.s;save();render()})}});
  render()})}

/* ---------- ink layer: pen, marker, eraser, text ---------- */
Object.assign(P,{type:'<path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>',board:'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="m8 21 4-4 4 4"/><path d="m7 12 3-3 3 3 4-4"/>',
 redo:'<path d="m15 14 5-5-5-5"/><path d="M20 9H9a5 5 0 0 0 0 10h3"/>',draw:'<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="m2 2 7.6 7.6"/><circle cx="11" cy="11" r="2"/>',addb:'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M12 8v5M9.5 10.5h5"/>'});
S.ink=S.ink||[];$('[data-b=draw]').innerHTML=I('draw',19);$('[data-b=board]').innerHTML=I('board',19);
const INK={k:'var(--ink)',r:'#E03131',b:'#1971C2',g:'#2F9E44',o:'#F08C00',v:'#9C36B5'},WID=[2,4,8];
const ink=E('div',{id:'tk-ink',class:'tk-ui'},'<svg xmlns="http://www.w3.org/2000/svg"></svg><div class="tl"></div>');document.body.append(ink);
const svg=$('svg',ink),tlay=$('.tl',ink);let pen={on:false,tool:'pen',c:'k',w:1},cache=[],inkH=[],inkR=[];
const blocks=()=>{const o=[];const kids=el=>[...el.children].filter(c=>!c.classList.contains('tk-x'));kids(ROOT).forEach((ch,i)=>{if(ch.tagName==='SECTION'&&ch.id)kids(ch).forEach((c,j)=>o.push([ch.id+':'+j,c]));else o.push(['m:'+i,ch])});return o};
const pageRect=el=>{const r=el.getBoundingClientRect();return{l:r.left+scrollX,t:r.top+scrollY,w:Math.max(r.width,1),h:Math.max(r.height,1)}};
function anchorAt(x,y){let best=null,bd=1e9;for(const[k,el]of blocks()){const r=pageRect(el);const d=y<r.t?r.t-y:y>r.t+r.h?y-r.t-r.h:0;if(d<bd){bd=d;best=[k,r]}if(!d)break}return best}
const r4=v=>Math.round(v*1e4)/1e4;
function smooth(p){if(!p.length)return'';if(p.length<3)return`M${p[0][0]} ${p[0][1]}`+p.slice(1).map(q=>`L${q[0]} ${q[1]}`).join('')+(p.length===1?`l.1 .1`:'');
  let d=`M${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;for(let i=1;i<p.length-1;i++){const m=[(p[i][0]+p[i+1][0])/2,(p[i][1]+p[i+1][1])/2];d+=`Q${p[i][0].toFixed(1)} ${p[i][1].toFixed(1)} ${m[0].toFixed(1)} ${m[1].toFixed(1)}`}const l=p[p.length-1];return d+`L${l[0].toFixed(1)} ${l[1].toFixed(1)}`}
function strokeAttrs(it){const hl=it.k==='m';return`stroke="${INK[it.c]||INK.k}" stroke-width="${WID[it.w]*(hl?4:1)}" stroke-opacity="${hl?.35:1}" fill="none" stroke-linecap="round" stroke-linejoin="round"${hl?' class="mk"':''}`}
let rT=0;const renderInk=()=>{cancelAnimationFrame(rT);rT=requestAnimationFrame(drawAll)};
function drawAll(){const H=Math.ceil(pageRect(ROOT).t+pageRect(ROOT).h+300),W=document.documentElement.scrollWidth;ink.style.height=H+'px';ink.style.width=W+'px';svg.setAttribute('width',W);svg.setAttribute('height',H);
  const map=Object.fromEntries(blocks().map(([k,el])=>[k,pageRect(el)]));cache=[];let h='';tlay.querySelectorAll('.tb').forEach(t=>{if(t!==document.activeElement)t.remove()});
  S.ink.forEach(it=>{const r=map[it.a];if(!r)return;if(it.k==='t'){if(tlay.querySelector(`.tb[data-id="${it.id}"]`))return;const x=r.l+it.x*r.w,y=r.t+it.y*r.h;tlay.append(textBox(it,x,y));return}
    const pts=it.p.map(([fx,fy])=>[r.l+fx*r.w,r.t+fy*r.h]);cache.push([it,pts]);h+=`<path data-id="${it.id}" d="${smooth(pts)}" ${strokeAttrs(it)}/>`});svg.innerHTML=h+'<path class="live"/>'}
function textBox(it,x,y){const t=E('div',{class:'tb','data-id':it.id,dir:'auto',spellcheck:'false'});t.textContent=it.t||'';t.style.cssText=`left:${x}px;top:${y}px;color:${INK[it.c]||INK.k};font-size:${[14,18,24][it.w]}px`;
  t.contentEditable=pen.on&&pen.tool==='text'?'true':'false';
  t.addEventListener('input',()=>{it.t=t.innerText;save()});t.addEventListener('blur',()=>{if(!t.innerText.trim()){inkSnap();S.ink=S.ink.filter(x=>x!==it);t.remove();save()}});
  t.addEventListener('pointerdown',e=>{if(!(pen.on&&pen.tool==='text'))return;const rc=t.getBoundingClientRect();if(e.clientX-rc.left>14&&e.clientY-rc.top>14)return;e.preventDefault();e.stopPropagation();
    const sx=e.clientX,sy=e.clientY,ox=parseFloat(t.style.left),oy=parseFloat(t.style.top);t.setPointerCapture(e.pointerId);
    const mv=ev=>{t.style.left=ox+ev.clientX-sx+'px';t.style.top=oy+ev.clientY-sy+'px'};const up=()=>{t.removeEventListener('pointermove',mv);t.removeEventListener('pointerup',up);inkSnap();const x=parseFloat(t.style.left),y=parseFloat(t.style.top),a=anchorAt(x,y);if(a){it.a=a[0];it.x=r4((x-a[1].l)/a[1].w);it.y=r4((y-a[1].t)/a[1].h);save()}};
    t.addEventListener('pointermove',mv);t.addEventListener('pointerup',up)});return t}
const inkSnap=()=>{inkH.push(JSON.stringify(S.ink));if(inkH.length>50)inkH.shift();inkR=[]};
function inkUndo(){if(!inkH.length)return;inkR.push(JSON.stringify(S.ink));S.ink=JSON.parse(inkH.pop());tlay.innerHTML='';renderInk();save()}
function inkRedo(){if(!inkR.length)return;inkH.push(JSON.stringify(S.ink));S.ink=JSON.parse(inkR.pop());tlay.innerHTML='';renderInk();save()}
let stk=null,erased=false;
function eraseAt(x,y){const R=12;let hit=false;cache=cache.filter(([it,pts])=>{const r=R+WID[it.w]*(it.k==='m'?2:.5);if(pts.some(p=>Math.abs(p[0]-x)<r&&Math.abs(p[1]-y)<r&&Math.hypot(p[0]-x,p[1]-y)<r)){if(!hit&&!erased)inkSnap();hit=true;erased=true;S.ink=S.ink.filter(s=>s!==it);const el=svg.querySelector(`[data-id="${it.id}"]`);if(el)el.remove();return false}return true});
  tlay.querySelectorAll('.tb').forEach(t=>{const rc=t.getBoundingClientRect();if(x-scrollX>=rc.left-4&&x-scrollX<=rc.right+4&&y-scrollY>=rc.top-4&&y-scrollY<=rc.bottom+4){if(!erased)inkSnap();erased=true;S.ink=S.ink.filter(s=>s.id!==t.dataset.id);t.remove()}});if(hit)save()}
ink.addEventListener('pointerdown',e=>{if(!pen.on||e.button>0)return;if(e.target.closest('.tb'))return;const x=e.pageX,y=e.pageY;
  if(pen.tool==='text'){e.preventDefault();const a=anchorAt(x,y);if(!a)return;inkSnap();const it={id:newId(),k:'t',a:a[0],x:r4((x-a[1].l)/a[1].w),y:r4((y-a[1].t-10)/a[1].h),c:pen.c,w:pen.w,t:''};S.ink.push(it);const t=textBox(it,x,y-10);t.contentEditable='true';tlay.append(t);t.focus();setTimeout(()=>{if(document.activeElement!==t)t.focus()},0);return}
  e.preventDefault();ink.setPointerCapture(e.pointerId);if(pen.tool==='eraser'){erased=false;eraseAt(x,y);return}
  stk={pts:[[x,y]],k:pen.tool==='marker'?'m':'p',c:pen.c,w:pen.w};const lv=svg.querySelector('.live');lv.setAttribute('d','');for(const[k,v]of Object.entries({stroke:INK[pen.c],'stroke-width':WID[pen.w]*(stk.k==='m'?4:1),'stroke-opacity':stk.k==='m'?.35:1,fill:'none','stroke-linecap':'round','stroke-linejoin':'round'}))lv.setAttribute(k,v)});
ink.addEventListener('pointermove',e=>{if(!pen.on)return;if(pen.tool==='eraser'&&e.buttons){eraseAt(e.pageX,e.pageY);return}if(!stk)return;
  const evs=e.getCoalescedEvents?e.getCoalescedEvents():[e];for(const v of evs){const l=stk.pts[stk.pts.length-1],x=v.pageX,y=v.pageY;if(Math.hypot(x-l[0],y-l[1])>1.5)stk.pts.push([x,y])}
  svg.querySelector('.live').setAttribute('d',smooth(stk.pts))});
const endStroke=()=>{if(!stk)return;const c=stk;stk=null;svg.querySelector('.live').setAttribute('d','');const a=anchorAt(c.pts[0][0],c.pts[0][1]);if(!a)return;inkSnap();
  S.ink.push({id:newId(),k:c.k,a:a[0],c:c.c,w:c.w,p:c.pts.map(([x,y])=>[r4((x-a[1].l)/a[1].w),r4((y-a[1].t)/a[1].h)])});save();renderInk()};
ink.addEventListener('pointerup',endStroke);ink.addEventListener('pointercancel',endStroke);
const dbar=E('div',{id:'tk-draw',class:'tk-ui',role:'toolbar'});document.body.append(dbar);
function drawBar(){const tb=(t,ic,l,k)=>`<button data-t="${t}" class="${pen.tool===t?'on':''}" title="${l} (${k})">${I(ic,19)}</button>`;
  dbar.innerHTML=tb('pen','pen','قلم','P')+tb('marker','hl','قلم تظليل','M')+tb('text','type','مربع نص','X')+tb('eraser','eraser','ممحاة','E')+'<span class="sep"></span>'+
  Object.entries(INK).map(([k,v])=>`<button data-c="${k}" class="cl${pen.c===k?' on':''}" title="لون"><i style="background:${v}"></i></button>`).join('')+'<span class="sep"></span>'+
  WID.map((w,i)=>`<button data-w="${i}" class="wd${pen.w===i?' on':''}" title="السُّمك"><i style="width:${w+3}px;height:${w+3}px"></i></button>`).join('')+'<span class="sep"></span>'+
  `<button data-a="undo" title="تراجع (Ctrl+Z)">${I('undo',19)}</button><button data-a="redo" title="إعادة (Ctrl+Y)">${I('redo',19)}</button><button data-a="clear" title="مسح كل الرسم">${I('trash',19)}</button><button data-a="off" class="done" title="إنهاء الرسم (Esc)">${I('check',19)}</button>`}
dbar.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const d=b.dataset;
  if(d.t)setTool(d.t);else if(d.c){pen.c=d.c;if(pen.tool==='eraser')setTool('pen');styleFocused()}else if(d.w){pen.w=+d.w;styleFocused()}
  else if(d.a==='undo')inkUndo();else if(d.a==='redo')inkRedo();else if(d.a==='clear'){if(S.ink.length){inkSnap();S.ink=[];tlay.innerHTML='';renderInk();save();toast('مُسح كل الرسم',{icon:'trash'})}}else if(d.a==='off')drawMode(false);drawBar()});
function styleFocused(){const t=document.activeElement;if(t&&t.classList&&t.classList.contains('tb')){const it=S.ink.find(x=>x.id===t.dataset.id);if(it){it.c=pen.c;it.w=pen.w;t.style.color=INK[pen.c];t.style.fontSize=[14,18,24][pen.w]+'px';save()}}}
const dropEmpty=()=>{const n=S.ink.length;S.ink=S.ink.filter(x=>x.k!=='t'||(x.t||'').trim()||(document.activeElement&&document.activeElement.dataset&&document.activeElement.dataset.id===x.id));if(S.ink.length!==n){tlay.innerHTML='';renderInk();save()}};
function setTool(t){dropEmpty();pen.tool=t;ink.dataset.tool=t;tlay.querySelectorAll('.tb').forEach(x=>x.contentEditable=t==='text'?'true':'false');drawBar()}
function drawMode(v){if(!v){document.activeElement&&document.activeElement.blur&&document.activeElement.blur();dropEmpty()}pen.on=v;document.body.classList.toggle('tk-drawing',v);$('[data-b=draw]').classList.toggle('on',v);if(v){hidePop();getSelection().removeAllRanges();setTool(pen.tool);toast('وضع الرسم: ارسم على الصفحة، Esc للخروج',{icon:'draw',ms:2200})}else{tlay.querySelectorAll('.tb').forEach(x=>{x.contentEditable='false';x.blur()})}}
if('ResizeObserver'in window)new ResizeObserver(renderInk).observe(ROOT);addEventListener('load',renderInk);

/* ---------- whiteboard (real Excalidraw, loaded on first open) ---------- */
const EXV='0.17.6';let board=null,bAPI=null,bT;
const js=src=>new Promise((res,rej)=>{const s=document.createElement('script');s.src=src;s.onload=res;s.onerror=()=>{s.remove();rej()};document.head.append(s)});
async function loadEx(){if(window.ExcalidrawLib)return;for(const b of['https://unpkg.com/','https://cdn.jsdelivr.net/npm/']){try{window.EXCALIDRAW_ASSET_PATH=b+`@excalidraw/excalidraw@${EXV}/dist/`;
  if(!window.React)await js(b+'react@18.3.1/umd/react.production.min.js');if(!window.ReactDOM)await js(b+'react-dom@18.3.1/umd/react-dom.production.min.js');await js(b+`@excalidraw/excalidraw@${EXV}/dist/excalidraw.production.min.js`);if(window.ExcalidrawLib)return}catch(e){}}throw 0}
async function openBoard(addText){if(!board){board=E('div',{id:'tk-board',class:'tk-ui'},`<header><b>${I('board',18)} السبورة</b><span class="st"></span><button class="tk-ib" data-a="close" title="إغلاق (رجوع للملخص)">${I('x',20)}</button></header><div class="cv"><div class="tk-empty"><span class="tk-load"></span><p>جارٍ تحميل السبورة…</p></div></div>`);
    document.body.append(board);$('[data-a=close]',board).onclick=closeBoard}
  board.classList.add('on');document.body.classList.add('tk-board-open');
  if(!bAPI){try{await loadEx()}catch(e){$('.cv',board).innerHTML=`<div class="tk-empty">${I('alert',28)}<p>تعذّر تحميل السبورة. تحتاج اتصالًا بالإنترنت أول مرة، وافتح الملف في المتصفح مباشرة.<br>يمكنك استخدام أدوات الرسم على الصفحة بدون إنترنت.</p></div>`;return}
    const cv=$('.cv',board);cv.innerHTML='';const B=S.board||{};
    await new Promise(res=>{ReactDOM.createRoot(cv).render(React.createElement(ExcalidrawLib.Excalidraw,{excalidrawAPI:a=>{bAPI=a;setTimeout(res,50)},
      initialData:{elements:B.elements||[],files:B.files||undefined,appState:{theme:S.theme==='dark'?'dark':'light',viewBackgroundColor:B.bg||(S.theme==='dark'?'#121212':'#ffffff')},scrollToContent:true},
      onChange:(els,app,files)=>{clearTimeout(bT);bT=setTimeout(()=>{const live=els.filter(x=>!x.isDeleted),ids=new Set(live.filter(x=>x.fileId).map(x=>x.fileId)),fl={};for(const k in files)if(ids.has(k))fl[k]=files[k];
        const nb={elements:live,files:fl,bg:app.viewBackgroundColor};if(JSON.stringify(nb.elements)!==JSON.stringify((S.board||{}).elements)||nb.bg!==(S.board||{}).bg){S.board=nb;save();$('.st',board).textContent='حُفظ تلقائيًا'}},500)}}))})}
  if(addText&&bAPI){const els=bAPI.getSceneElements(),y=els.reduce((m,e)=>Math.max(m,e.y+(e.height||0)),0)+40;
    const nw=ExcalidrawLib.convertToExcalidrawElements([{type:'text',x:0,y,text:addText.length>300?addText.slice(0,300)+'…':addText,fontSize:20}]);bAPI.updateScene({elements:[...els,...nw]});bAPI.scrollToContent(nw,{fitToContent:false})}}
function closeBoard(){if(board){board.classList.remove('on');document.body.classList.remove('tk-board-open')}}
const boardOpen=()=>!!board&&board.classList.contains('on');

/* ---------- export ---------- */
function exportHTML(){S.saved=Date.now();flush();
  const data=JSON.stringify(S).replace(/</g,'\\u003c'),tag='<script type="application/json" id="tk-'+'data">'+data+'<\/script>',re=/<script type="application\/json" id="tk-data">[\s\S]*?<\/script>/;
  const html=re.test(PRISTINE)?PRISTINE.replace(re,()=>tag):PRISTINE.replace('</head>',()=>tag+'</head>');download(baseName()+'_annotated.html',html,'text/html');toast('نُزّلت نسخة فيها تحديداتك وملاحظاتك وإجاباتك',{icon:'dl'})}

/* ---------- toolbar & keys ---------- */
$('#tk-bar').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const k=b.dataset.b;
  if(k==='toc'){toggleToc();S.toc=document.body.classList.contains('tk-toc-open');save()}
  else if(k==='tr'||k==='notes'||k==='find'){if(panelOpen()&&$(`#tk-panel .tab[data-tab=${k}]`).classList.contains('on'))closePanel();else{openPanel(k);if(k==='find')setTimeout(()=>$('#tk-fin').focus(),260)}}
  else if(k==='fm'||k==='fp'){const c=S.font||parseFloat(getComputedStyle(document.documentElement).fontSize);S.font=Math.max(14,Math.min(30,c+(k==='fp'?2:-2)));applyLook();save();toast('حجم الخط '+S.font,{icon:k,ms:1200})}
  else if(k==='theme'){S.theme=S.theme==='dark'?'light':'dark';applyLook();save()}
  else if(k==='exp')exportHTML()
  else if(k==='draw')drawMode(!pen.on)
  else if(k==='board')openBoard()});
document.addEventListener('keydown',e=>{if(boardOpen()){if(e.key==='Escape'&&!document.activeElement.closest('#tk-board .cv'))closeBoard();return}
  const inField=e.target.closest&&e.target.closest('input,textarea,[contenteditable=true]');
  if(e.key==='Escape'){if(inField&&inField.classList.contains('tb')){inField.blur();return}if(popMode){hidePop();getSelection().removeAllRanges()}else if(pen.on)drawMode(false);else if(panelOpen())closePanel();return}
  if(inField)return;
  if(pen.on&&!e.altKey){const k=e.key.toLowerCase();if((e.ctrlKey||e.metaKey)&&(k==='y'||(k==='z'&&e.shiftKey))){e.preventDefault();inkRedo();return}if((e.ctrlKey||e.metaKey)&&k==='z'){e.preventDefault();inkUndo();return}
    if(!e.ctrlKey&&!e.metaKey){const m={p:'pen',m:'marker',x:'text',e:'eraser'}[k];if(m){setTool(m);return}if(k==='d'){drawMode(false);return}}}
  if(!popMode&&!e.ctrlKey&&!e.metaKey&&!e.altKey){const k=e.key.toLowerCase();if(k==='d'){drawMode(!pen.on);return}if(k==='b'){openBoard();return}}
  if((e.ctrlKey||e.metaKey)&&!e.shiftKey&&e.key.toLowerCase()==='z'&&hist.length){e.preventDefault();undo();return}
  if(popMode&&!e.ctrlKey&&!e.metaKey&&!e.altKey){const k=e.key.toLowerCase();let a=null,b=null;
    if(/^[1-5]$/.test(k)){a='c';b={dataset:{c:COLORS[+k-1][0]}}}else if(k==='n')a='note';else if(k==='t')a='tr';else if(k==='c')a='copy';
    else if(k==='delete'||k==='backspace')a=popMode==='mark'?'del':(pop.querySelector('[data-a=erase]')?'erase':null);
    if(a){e.preventDefault();act(a,b);return}}
  if(e.key==='/'){e.preventDefault();openPanel('find');$('#tk-fin').focus()}});

/* ---------- start ---------- */
window.__tkInk=renderInk;
if(!$('.tk-sig'))document.body.append(E('footer',{class:'tk-sig tk-x'},'Eyad Al-Mahrouqi · @q7r_9'));
applyLook();initQuiz();restore();buildToc();scrollBar();
if(S.toc===true||(S.toc===null&&innerWidth>=1250))toggleToc(true);
if(!S.saved)setTimeout(()=>toast('حدّد أي نص لترجمته أو تلوينه أو إضافة ملاحظة عليه',{icon:'hl',ms:5000}),800);
if('speechSynthesis'in window)speechSynthesis.getVoices();
})();

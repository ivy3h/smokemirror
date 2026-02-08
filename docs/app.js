// ===== Sample Data =====
// Pre-generated story data matching SmokeMirror output format

const SAMPLE = {
  crime: {
    crime_type: "murder",
    setting: "Tech Startup - NovaTech Solutions",
    victim: { name: "Dr. Eleanor Voss", occupation: "Chief Science Officer", relationship: "Exposed the criminal's past corruption" },
    criminal: { name: "Marcus Hale", occupation: "Senior VP of Operations", motive: "Revenge and cover-up of embezzlement", means: "Access to victim's schedule and building security", opportunity: "Late-night board meeting" },
    conspirators: [
      { name: "Clara Nguyen", occupation: "Head of Security", leverage: "Marcus knows about her falsified credentials", alibi: "Claims she was monitoring east wing cameras" },
      { name: "Henry Whitaker", occupation: "CFO", leverage: "Complicit in the embezzlement scheme", alibi: "Says he was at a client dinner downtown" },
    ],
    evidence: [
      { id: "E1", type: "digital", description: "Security camera footage gap (22 minutes)", location: "Server room", steps: 3, real_meaning: "Footage deliberately deleted by Clara" },
      { id: "E2", type: "documentary", description: "Forged financial audit report", location: "Eleanor's desk", steps: 2, real_meaning: "Shows Marcus's embezzlement trail" },
      { id: "E3", type: "physical", description: "Broken brandy glass with trace DNA", location: "Crime scene study", steps: 2, real_meaning: "Glass was planted post-mortem" },
      { id: "E4", type: "testimonial", description: "Night janitor's account of strange noises", location: "Building lobby", steps: 1, real_meaning: "Janitor heard the actual crime occurring" },
      { id: "E5", type: "digital", description: "Victim's encrypted laptop files", location: "Eleanor's office", steps: 3, real_meaning: "Contains proof of Marcus's corruption" },
    ],
    timeline: [
      { time: "7:30 PM", event: "Board meeting ends, most staff leave", actor: "All" },
      { time: "8:15 PM", event: "Eleanor stays late to review audit files", actor: "Eleanor" },
      { time: "9:00 PM", event: "Marcus enters building using Clara's override", actor: "Marcus" },
      { time: "9:22 PM", event: "Clara disables cameras on floors 3-5", actor: "Clara" },
      { time: "9:45 PM", event: "Crime occurs in Eleanor's office", actor: "Marcus" },
      { time: "10:10 PM", event: "Scene staged to look like robbery", actor: "Marcus & Clara" },
      { time: "10:30 PM", event: "Henry provides cover at downtown restaurant", actor: "Henry" },
    ],
  },

  fabricated: {
    fake_suspect: { name: "Ryan Torres", occupation: "Fired software engineer", fake_motive: "Revenge for wrongful termination" },
    cover_story: "A disgruntled former employee broke in to steal proprietary code and confronted Eleanor when she caught him. The struggle turned fatal.",
    planted_evidence: [
      { id: "PE1", description: "Ryan's employee badge found near the scene" },
      { id: "PE2", description: "Threatening emails from Ryan's old account" },
    ],
    alibis: {
      "Clara Nguyen": "Was monitoring security feeds in the east wing control room",
      "Henry Whitaker": "Attended a client dinner at Marcello's from 8 PM to 11 PM",
    },
  },

  detective: {
    name: "Detective Jonathan Cole",
    background: "15-year veteran with the Cyber Crimes division, recently transferred to Homicide",
    personal_stakes: "Eleanor was his former informant who helped him crack his biggest case. He owes her.",
    dire_consequence: "If unsolved in 72 hours, the DA will charge Ryan Torres, an innocent man, and Cole's reputation as a detective who follows the evidence is destroyed.",
    deadline_reason: "Key digital evidence on the company servers will be overwritten by an automatic backup cycle in 72 hours.",
  },

  plot_points: [
    { id: 1, action: "Examines crime scene and interviews first responders", description: "Detective Cole arrives at NovaTech and documents the scene. The staged robbery looks convincing, but something about the broken glass pattern bothers him.", learns: "Victim found in her office, signs of forced entry, broken brandy glass nearby", suspense: 4, collision: false, reveal: "Reader knows the break-in was staged by Marcus and Clara" },
    { id: 2, action: "Reviews building security footage", description: "Cole requests all camera feeds from the night. He discovers a 22-minute gap in the coverage on floors 3-5.", learns: "Security footage gap from 9:20 PM to 9:42 PM is suspicious (E1 partial, 1/3 steps)", suspense: 5, collision: false, reveal: "Reader knows Clara deliberately deleted the footage" },
    { id: 3, action: "Interviews Clara Nguyen about the camera gap", description: "Cole questions Clara about the missing footage. She explains it as a 'routine server restart' and provides system logs to back her claim. Cole accepts her explanation for now.", learns: "Clara's alibi checks out on paper; she says the gap was a server restart", suspense: 6, collision: true, reveal: "Reader watches Clara lie directly to Cole's face, covering for Marcus" },
    { id: 4, action: "Investigates Ryan Torres as primary suspect", description: "Following the planted evidence, Cole tracks down Ryan. He finds the threatening emails and badge. Ryan claims he was framed, but has no alibi.", learns: "Ryan Torres had motive (fired), means (still had badge), opportunity (no alibi)", suspense: 5, collision: false, reveal: null },
    { id: 5, action: "Examines Eleanor's desk for financial documents", description: "Cole finds the forged audit report on Eleanor's desk. The numbers seem off, but he needs a forensic accountant to verify.", learns: "Partial progress on financial audit (E2, 1/2 steps) - something seems unusual", suspense: 6, collision: false, reveal: "Reader knows this document hides proof of Marcus's embezzlement" },
    { id: 6, action: "Attempts to access the victim's encrypted laptop", description: "Cole tries to break into Eleanor's laptop but encounters military-grade encryption. The IT department says it could take days to crack.", learns: "Laptop is encrypted; IT needs 48+ hours. Precious time ticking away.", suspense: 7, collision: false, reveal: "Reader knows the laptop contains definitive proof that could solve everything" },
    { id: 7, action: "Interviews the night janitor about what he heard", description: "The janitor describes hearing raised voices and a crash around 9:40 PM, but he was on the ground floor and can't identify voices. He also mentions seeing a 'tall figure' leaving via the back stairwell.", learns: "Witness heard the crime at 9:40 PM; saw unidentified figure leaving (E4 complete)", suspense: 7, collision: false, reveal: "Reader knows the 'tall figure' was Marcus, and the timeline matches perfectly" },
    { id: 8, action: "Cross-references security badge access logs with the camera gap", description: "Cole discovers Clara's security override was used during the camera blackout. He confronts her again, but Henry Whitaker steps in, explaining that Clara was running a 'confidential security audit' authorized by him.", learns: "Clara used override during gap, but Henry vouches for her with paperwork", suspense: 8, collision: true, reveal: "Reader watches Henry deploy his pre-arranged cover story to protect the conspiracy" },
    { id: 9, action: "Checks Henry Whitaker's dinner alibi at Marcello's", description: "Cole verifies Henry's alibi at the restaurant. The maitre d' confirms Henry arrived at 8:30 PM and left at 10:45 PM. But Cole notices the receipt was paid in cash - no credit card trail.", learns: "Henry's alibi appears solid but the cash payment is unusual (alibi: challenged)", suspense: 7, collision: false, reveal: "Reader knows Henry actually arrived late at 10:15 PM after helping stage the scene" },
    { id: 10, action: "Returns to crime scene to re-examine the brandy glass", description: "Something has been nagging Cole about the glass. He examines it more carefully and finds the DNA trace. But the lab results will take 24 hours.", learns: "DNA trace found on glass; lab results pending (E3, 1/2 steps)", suspense: 8, collision: false, reveal: "Reader knows the glass was planted and the DNA will lead to a dead end" },
    { id: 11, action: "Obtains partial decryption of victim's laptop files", description: "IT manages a partial decrypt. Cole finds fragments of financial documents referencing 'Project Phantom' and large transfers to offshore accounts. But the key files are still locked.", learns: "Victim was investigating 'Project Phantom' - possible financial fraud (E5, 1/3 steps)", suspense: 8, collision: true, reveal: "Reader watches as Cole gets tantalizingly close to the embezzlement proof, but Marcus secretly contacts IT to slow the decryption" },
    { id: 12, action: "Interviews Marcus Hale about Project Phantom", description: "Cole asks Marcus about the financial irregularities. Marcus smoothly explains it as a 'classified R&D initiative' and provides doctored documentation. He subtly redirects Cole back to Ryan Torres.", learns: "Marcus claims Project Phantom is legitimate R&D; provides supporting docs", suspense: 9, collision: true, reveal: "Reader watches Marcus lie with practiced ease, knowing every document is forged" },
    { id: 13, action: "Forensic analysis of financial audit returns results", description: "The forensic accountant finds the audit report was altered, but can't determine by whom. The trail leads to a shared company printer. Time is running out.", learns: "Audit was forged but origin untraceable. Full evidence obtained (E2, 2/2 steps complete)", suspense: 8, collision: false, reveal: "Reader knows Marcus forged it, but the evidence points nowhere without the laptop files" },
    { id: 14, action: "DNA results from the brandy glass arrive", description: "The DNA matches... Ryan Torres. Cole feels the case closing around an innocent man, but something still doesn't sit right. The glass shards don't match the wound pattern.", learns: "DNA matches Ryan Torres, but glass pattern inconsistency (E3, 2/2 complete)", suspense: 9, collision: false, reveal: "Reader knows the DNA was planted from Ryan's old coffee mug stolen from the break room" },
    { id: 15, action: "Makes final push to crack the laptop encryption", description: "With hours left before the server backup overwrites key data, Cole works through the night. He gets 60% of the files but the crucial financial records remain encrypted.", learns: "Partial laptop access shows Eleanor was building a case against someone senior (E5, 2/3 steps)", suspense: 9, collision: false, reveal: "Reader agonizes as the truth is literally one password away" },
    { id: 16, action: "Confronts the DA with doubts about Ryan Torres", description: "Cole presents his reservations to the DA, but the circumstantial evidence is overwhelming. The DA gives him until midnight to find an alternative suspect or charges are filed.", learns: "DA will charge Ryan Torres at midnight. 6 hours remain.", suspense: 10, collision: false, reveal: "Reader watches the countdown reach its crisis point" },
    { id: 17, action: "Reviews all evidence one final time, notices the timeline gap", description: "In a desperate final review, Cole spots it: the janitor's 9:40 PM timestamp, the camera blackout at 9:22 PM, and Clara's override. The window is too tight for an outside intruder. But he can't prove who was inside.", learns: "Timeline strongly suggests an inside job, but lacks definitive proof", suspense: 10, collision: false, reveal: "Reader watches Cole reach the edge of the truth but unable to cross the final gap" },
    { id: 18, action: "Final determination - Cole files his report", description: "The clock strikes midnight. Cole files his report noting 'unresolved inconsistencies' but lacking enough evidence to name an alternative suspect. Ryan Torres is charged. Cole stares at Eleanor's photo on his desk, haunted by the feeling that the real killer is still out there.", learns: "Case closed with Ryan Torres charged. The conspiracy holds.", suspense: 10, collision: false, reveal: "Reader watches Marcus Hale smile as he reads the news, knowing his secret is safe. The reader alone carries the weight of the truth." },
  ],

  evaluation: {
    logic_analyst: { score: 7.8, prediction_correct: false, issues: 2 },
    intuitive_reader: { score: 8.2, prediction_correct: false, issues: 1 },
    genre_expert: { score: 7.5, prediction_correct: false, issues: 3, pacing: "Strong build, slight plateau at points 4-5" },
  },

  refinement: {
    issues_found: 3,
    issues_fixed: 2,
    details: [
      "Plot point 4-5: pacing improved - added time pressure to Ryan Torres interview",
      "Plot point 9: strengthened the cash payment suspicion thread",
    ],
  },

  final_story: null, // Will be loaded from the story text
};

// We'll use the existing output story text
const STORY_TEXT = `# Shadows of Deception

*A Mystery Novel by SmokeMirror AI*

---

## Prologue: The Perfect Lie

Detective Jonathan Cole received the call at 11:47 PM. Dr. Eleanor Voss, Chief Science Officer at NovaTech Solutions, was dead. Found in her corner office on the fifth floor, surrounded by shattered glass and scattered financial documents.

Cole had known Eleanor. She'd been his informant three years ago, feeding him the digital breadcrumbs that led to the biggest cybercrime bust of his career. He owed her. Now, standing over her body as forensics dusted for prints, he swore he would find whoever did this.

What Cole didn't know - what he couldn't know - was that the killer was already standing beside him. Marcus Hale, Senior VP of Operations, had arrived minutes after the first responders. He wore the mask of a concerned colleague perfectly. Behind his sympathetic eyes, he was already calculating his next move.

---

## Chapter 1: The Crime Scene

The office told a story of violence. A broken window, an overturned desk, a shattered brandy glass with trace amounts of blood. To any detective, it screamed robbery gone wrong.

Cole crouched beside the glass shards, photographing each piece. Something about the break pattern seemed off - too clean, too deliberate - but he filed the thought away for later.

"The security footage," he said to the uniformed officer by the door. "I want everything from tonight."

What arrived was a 22-minute gap. Floors three through five, dark from 9:22 PM to 9:44 PM. The head of security, Clara Nguyen, attributed it to a server restart. She had logs to prove it.

Cole accepted the explanation. He had no reason not to.

*The reader, however, knows that Clara deleted that footage herself, her hands trembling as she watched Marcus's shadow move through the hallway toward Eleanor's office.*

---

## Chapter 2: The Suspect

Ryan Torres made an easy target. Fired six months ago after a dispute over intellectual property, his employee badge was found twenty feet from the body. Threatening emails from his old company account littered Eleanor's inbox.

Cole interviewed him in a cramped precinct room. Torres was sweating, scared, and adamant: "I didn't do this. I was home. Alone. I know how that sounds."

It sounded like guilt. Cole had seen this a hundred times - the desperate denial, the lack of alibi, the damning evidence. But something in Torres's eyes reminded him of another case, years ago, where the obvious suspect had been the wrong one.

He kept digging.

---

## Chapter 3: Cracks in the Mirror

The investigation deepened. Cole found Eleanor had been investigating something called "Project Phantom" - large financial transfers to offshore accounts, hidden in NovaTech's R&D budget. The forged audit report on her desk had been altered, but by whom?

When Cole asked Marcus about Project Phantom, the VP didn't miss a beat. "Classified R&D. I can get you the authorization documents." The paperwork arrived within the hour, complete and convincing.

*The reader knows every page is forged. Marcus spent three nights fabricating them, using Eleanor's own forensic techniques against the investigation she started.*

Meanwhile, the clock was ticking. Eleanor's laptop held encrypted files that might blow the case open, but IT needed 48 hours they didn't have. The company servers would overwrite backup logs in 72 hours. The DA was circling, ready to charge Torres.

Cole could feel the truth slipping through his fingers like smoke.

---

## Chapter 4: The Conspiracy Holds

Every path Cole followed led to a dead end - or worse, back to Ryan Torres. Clara's alibi checked out on paper. Henry Whitaker's dinner receipt placed him at Marcello's. The janitor heard voices but couldn't identify them. The DNA on the brandy glass matched Torres.

But the timeline nagged at him. The 22-minute camera gap. Clara's security override. The janitor's 9:40 PM timestamp. The window was too tight for an outside intruder to break in, commit murder, stage a robbery, and escape.

It pointed to an inside job. Cole knew it in his gut. But knowing and proving were separated by an ocean of circumstantial evidence, and he was running out of time to cross it.

---

## Chapter 5: Midnight

The DA's deadline arrived like a verdict. Cole sat in his office, Eleanor's case file spread across his desk, her photo pinned to the board beside a web of connections he couldn't quite complete.

He filed his report at 11:58 PM. "Unresolved inconsistencies warrant further investigation." But without a viable alternative suspect, the wheels of justice ground forward. Ryan Torres was charged with murder in the first degree.

Marcus Hale read about it the next morning over coffee, the ghost of a smile playing at his lips. Clara Nguyen called in sick, unable to face the office. Henry Whitaker transferred funds one last time, closing the offshore accounts forever.

And Jonathan Cole sat in his car outside NovaTech, staring up at the dark fifth-floor window, haunted by the certainty that the truth was still in there somewhere. Locked behind encryption he couldn't break. Hidden in footage that no longer existed. Protected by people who smiled to his face and lied with every breath.

The conspiracy held. The mirror remained unbroken.

*But the reader carries the weight of what really happened - and the knowledge that sometimes, the smoke clears too late.*

---

**THE END**

---

*Generated by SmokeMirror - AI Mystery Story Generator*
*Model: Qwen2.5-7B-Instruct | Suspense Score: 8.2/10 | 18 Plot Points*`;


// ===== App Logic =====

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

let generating = false;

// Generate button
$('#btn-generate').addEventListener('click', startGeneration);
$('#btn-restart')?.addEventListener('click', () => {
  $('#pipeline').classList.add('hidden');
  $('#story-output').classList.add('hidden');
  $('#hero').classList.remove('hidden');
  // Reset steps
  $$('.step').forEach(s => { s.classList.remove('active','done'); s.querySelector('.step-content').innerHTML = ''; });
  generating = false;
});

async function startGeneration() {
  if (generating) return;
  generating = true;
  $('#btn-generate').disabled = true;
  $('#btn-generate').textContent = 'Generating...';

  // Show pipeline, hide hero
  $('#hero').classList.add('hidden');
  $('#pipeline').classList.remove('hidden');

  // Run each phase
  await runPhase1();
  await runPhase2();
  await runPhase3();
  await runPhase4();
  await runPhase5();
  await runPhase6();

  // Show final story
  $('#pipeline').classList.add('hidden');
  showFinalStory();

  generating = false;
  $('#btn-generate').disabled = false;
  $('#btn-generate').textContent = 'Generate Mystery';
}

function updateProgress(pct, label) {
  $('#countdown-fill').style.width = pct + '%';
  $('#countdown-label').textContent = label;
}

function activateStep(n) {
  // Mark previous as done
  for (let i = 1; i < n; i++) {
    $(`#step-${i}`).classList.remove('active');
    $(`#step-${i}`).classList.add('done');
  }
  $(`#step-${n}`).classList.add('active');
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ===== Phase 1: Crime Backstory =====
async function runPhase1() {
  activateStep(1);
  updateProgress(5, 'Phase 1/6: Generating crime backstory...');
  await sleep(800);

  const c = SAMPLE.crime;
  let html = `
    <div class="info-card">
      <h4>Crime: ${c.crime_type.toUpperCase()}</h4>
      <div class="info-row"><span class="label">Setting:</span> <span class="value">${c.setting}</span></div>
      <div class="info-row"><span class="label">Victim:</span> <span class="value">${c.victim.name} (${c.victim.occupation})</span></div>
      <div class="info-row"><span class="label">Criminal:</span> <span class="value">${c.criminal.name} (${c.criminal.occupation})</span></div>
      <div class="info-row"><span class="label">Motive:</span> <span class="value">${c.criminal.motive}</span></div>
    </div>
    <div class="info-card">
      <h4>Conspirators</h4>
      ${c.conspirators.map(co => `
        <div class="info-row">
          <span class="tag danger">${co.name}</span>
          <span class="value">${co.occupation} &mdash; ${co.leverage}</span>
        </div>
      `).join('')}
    </div>
    <div class="info-card">
      <h4>Evidence (${c.evidence.length} items)</h4>
      ${c.evidence.map(e => `
        <div class="info-row">
          <span class="tag">${e.id}</span>
          <span class="tag gold">${e.type}</span>
          <span class="value">${e.description} <small>(${e.steps} steps)</small></span>
        </div>
      `).join('')}
    </div>`;

  $('#content-1').innerHTML = html;
  updateProgress(15, 'Crime backstory generated');
  await sleep(600);
}

// ===== Phase 2: Fabricated Narrative =====
async function runPhase2() {
  activateStep(2);
  updateProgress(20, 'Phase 2/6: Building fabricated narrative...');
  await sleep(800);

  const f = SAMPLE.fabricated;
  let html = `
    <div class="info-card">
      <h4>Fake Suspect: ${f.fake_suspect.name}</h4>
      <div class="info-row"><span class="label">Occupation:</span> <span class="value">${f.fake_suspect.occupation}</span></div>
      <div class="info-row"><span class="label">Fake Motive:</span> <span class="value">${f.fake_suspect.fake_motive}</span></div>
    </div>
    <div class="info-card">
      <h4>Cover Story</h4>
      <p>${f.cover_story}</p>
    </div>
    <div class="info-card">
      <h4>Conspirator Alibis</h4>
      ${Object.entries(f.alibis).map(([name, alibi]) => `
        <div class="info-row">
          <span class="tag danger">${name}</span>
          <span class="value">"${alibi}"</span>
        </div>
      `).join('')}
    </div>`;

  $('#content-2').innerHTML = html;
  updateProgress(30, 'Fabricated narrative built');
  await sleep(600);
}

// ===== Phase 3: Detective Investigation =====
async function runPhase3() {
  activateStep(3);
  updateProgress(35, 'Phase 3/6: Running suspense meta-controller...');

  const d = SAMPLE.detective;
  let headerHtml = `
    <div class="info-card">
      <h4>${d.name}</h4>
      <div class="info-row"><span class="label">Stakes:</span> <span class="value">${d.personal_stakes}</span></div>
      <div class="info-row"><span class="label">If failure:</span> <span class="value" style="color:var(--accent2)">${d.dire_consequence}</span></div>
      <div class="info-row"><span class="label">Deadline:</span> <span class="value">${d.deadline_reason}</span></div>
    </div>
    <div id="plot-points-container"></div>`;
  $('#content-3').innerHTML = headerHtml;

  await sleep(500);

  const container = $('#plot-points-container');
  const total = SAMPLE.plot_points.length;

  for (let i = 0; i < total; i++) {
    const pp = SAMPLE.plot_points[i];
    const pct = 35 + Math.round((i / total) * 35);
    const timeLeft = 21 - (i + 1);
    updateProgress(pct, `Plot point ${pp.id}/${total} | Time: ${timeLeft}/${21} | Suspense: ${pp.suspense}/10`);

    const cls = pp.collision ? 'collision' : (pp.reveal ? 'progress' : '');
    const suspenseColor = pp.suspense <= 5 ? 'var(--blue)' : pp.suspense <= 7 ? 'var(--gold)' : 'var(--accent2)';
    const suspensePct = pp.suspense * 10;

    let ppHtml = `<div class="plot-point ${cls}">
      <div class="pp-header">
        <span class="pp-id">PP-${pp.id} ${pp.collision ? '<span class="tag danger">COLLISION</span>' : ''}</span>
        <span class="pp-suspense">Suspense: ${pp.suspense}/10</span>
      </div>
      <div class="pp-body">${pp.description}</div>
      <div class="suspense-bar">
        <span>Suspense</span>
        <div class="suspense-track"><div class="suspense-value" style="width:${suspensePct}%;background:${suspenseColor}"></div></div>
      </div>
      ${pp.reveal ? `<div class="pp-reveal">${pp.reveal}</div>` : ''}
    </div>`;

    container.insertAdjacentHTML('beforeend', ppHtml);
    // Scroll the new plot point into view
    container.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    await sleep(350);
  }

  updateProgress(70, 'Investigation complete - 18 plot points generated');
  await sleep(400);
}

// ===== Phase 4: Reader Evaluation =====
async function runPhase4() {
  activateStep(4);
  updateProgress(75, 'Phase 4/6: Running reader simulation...');
  await sleep(800);

  const ev = SAMPLE.evaluation;
  let html = '';
  const readers = [
    { key: 'logic_analyst', label: 'Logic Analyst', icon: 'logical consistency & deduction' },
    { key: 'intuitive_reader', label: 'Intuitive Reader', icon: 'character behavior & immersion' },
    { key: 'genre_expert', label: 'Genre Expert', icon: 'pacing & narrative structure' },
  ];

  for (const r of readers) {
    const d = ev[r.key];
    const scoreColor = d.score >= 8 ? 'var(--green)' : d.score >= 6 ? 'var(--gold)' : 'var(--accent2)';
    html += `
      <div class="eval-card">
        <h4>${r.label}</h4>
        <small style="color:var(--text-dim)">${r.icon}</small>
        <div class="score-row"><span>Overall Score</span> <span class="score-val" style="color:${scoreColor}">${d.score}/10</span></div>
        <div class="score-row"><span>Identified Real Criminal?</span> <span class="score-val" style="color:var(--green)">No (good!)</span></div>
        <div class="score-row"><span>Issues Flagged</span> <span class="score-val">${d.issues}</span></div>
        ${d.pacing ? `<div class="score-row"><span>Pacing</span> <span style="color:var(--text-dim);font-size:.82rem">${d.pacing}</span></div>` : ''}
      </div>`;
  }

  $('#content-4').innerHTML = html;
  updateProgress(85, 'Reader evaluation complete');
  await sleep(600);
}

// ===== Phase 5: Refinement =====
async function runPhase5() {
  activateStep(5);
  updateProgress(88, 'Phase 5/6: Refining story...');
  await sleep(700);

  const ref = SAMPLE.refinement;
  let html = `
    <div class="info-card">
      <h4>Refinement Results</h4>
      <div class="info-row"><span class="label">Issues found:</span> <span class="value">${ref.issues_found}</span></div>
      <div class="info-row"><span class="label">Issues fixed:</span> <span class="value">${ref.issues_fixed}</span></div>
    </div>
    <div class="info-card">
      <h4>Changes Applied</h4>
      ${ref.details.map(d => `<div class="info-row"><span class="tag green">Fixed</span> <span class="value">${d}</span></div>`).join('')}
    </div>`;

  $('#content-5').innerHTML = html;
  updateProgress(92, 'Refinement complete');
  await sleep(500);
}

// ===== Phase 6: Story Assembly =====
async function runPhase6() {
  activateStep(6);
  updateProgress(95, 'Phase 6/6: Assembling final narrative...');
  await sleep(1200);
  $('#content-6').innerHTML = `<div class="info-card"><h4>Story assembled successfully</h4><p>18 plot points woven into a dual-layer narrative with dramatic irony.</p></div>`;
  updateProgress(100, 'Generation complete!');
  await sleep(800);
  // Mark step 6 as done
  $('#step-6').classList.remove('active');
  $('#step-6').classList.add('done');
}

// ===== Final Story Display =====
function showFinalStory() {
  $('#story-output').classList.remove('hidden');
  $('#story-meta').innerHTML = `
    <span class="tag">Qwen2.5-7B-Instruct</span>
    <span class="tag gold">18 Plot Points</span>
    <span class="tag green">Suspense: 8.2/10</span>
    <span class="tag">72h Countdown</span>
  `;

  // Convert markdown-like text to HTML
  let storyHtml = STORY_TEXT
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^---$/gm, '<hr>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');
  storyHtml = '<p>' + storyHtml + '</p>';

  $('#story-body').innerHTML = storyHtml;
  $('#story-output').scrollIntoView({ behavior: 'smooth' });
}

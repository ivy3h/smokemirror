// ===== Multiple Stories =====
// Each click randomly picks one story to animate through the pipeline

const ALL_STORIES = [

// ===== Story 1: Shadows of Deception (Tech Startup) =====
{
  crime: {
    crime_type: "murder",
    setting: "Tech Startup - NovaTech Solutions",
    victim: { name: "Dr. Eleanor Voss", occupation: "Chief Science Officer" },
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
  },
  fabricated: {
    fake_suspect: { name: "Ryan Torres", occupation: "Fired software engineer", fake_motive: "Revenge for wrongful termination" },
    cover_story: "A disgruntled former employee broke in to steal proprietary code and confronted Eleanor when she caught him. The struggle turned fatal.",
    alibis: { "Clara Nguyen": "Was monitoring security feeds in the east wing control room", "Henry Whitaker": "Attended a client dinner at Marcello's from 8 PM to 11 PM" },
  },
  detective: {
    name: "Detective Jonathan Cole",
    background: "15-year veteran, Cyber Crimes division",
    personal_stakes: "Eleanor was his former informant who helped him crack his biggest case. He owes her.",
    dire_consequence: "If unsolved in 72 hours, the DA will charge Ryan Torres, an innocent man.",
    deadline_reason: "Key digital evidence on the company servers will be overwritten by an automatic backup cycle in 72 hours.",
  },
  plot_points: [
    { id:1, action:"Examines crime scene and interviews first responders", description:"Detective Cole arrives at NovaTech. The staged robbery looks convincing, but the broken glass pattern bothers him.", suspense:4, collision:false, reveal:"Reader knows the break-in was staged by Marcus and Clara" },
    { id:2, action:"Reviews building security footage", description:"Cole discovers a 22-minute gap in cameras on floors 3-5.", suspense:5, collision:false, reveal:"Reader knows Clara deliberately deleted the footage" },
    { id:3, action:"Interviews Clara Nguyen about the camera gap", description:"Clara explains it as a 'routine server restart' with system logs. Cole accepts her explanation.", suspense:6, collision:true, reveal:"Reader watches Clara lie directly to Cole's face" },
    { id:4, action:"Investigates Ryan Torres as primary suspect", description:"Following planted evidence, Cole finds threatening emails and badge. Ryan claims innocence but has no alibi.", suspense:5, collision:false, reveal:null },
    { id:5, action:"Examines Eleanor's desk for financial documents", description:"Cole finds a forged audit report. The numbers seem off, but he needs a forensic accountant.", suspense:6, collision:false, reveal:"Reader knows this document hides proof of Marcus's embezzlement" },
    { id:6, action:"Attempts to access the victim's encrypted laptop", description:"Military-grade encryption. IT needs 48+ hours. Precious time ticking away.", suspense:7, collision:false, reveal:"Reader knows the laptop contains definitive proof" },
    { id:7, action:"Interviews the night janitor", description:"Janitor heard raised voices at 9:40 PM and saw a 'tall figure' leaving via the back stairwell.", suspense:7, collision:false, reveal:"Reader knows the 'tall figure' was Marcus" },
    { id:8, action:"Cross-references badge logs with camera gap", description:"Clara's security override was used during the blackout. Henry steps in with a 'confidential security audit' cover.", suspense:8, collision:true, reveal:"Reader watches Henry deploy the pre-arranged cover story" },
    { id:9, action:"Checks Henry's dinner alibi at Marcello's", description:"Maitre d' confirms Henry was there. But the receipt was paid in cash - no credit card trail.", suspense:7, collision:false, reveal:"Reader knows Henry arrived late after helping stage the scene" },
    { id:10, action:"Re-examines the brandy glass", description:"Cole finds a DNA trace. Lab results will take 24 hours.", suspense:8, collision:false, reveal:"Reader knows the glass was planted" },
    { id:11, action:"Obtains partial laptop decryption", description:"Fragments reference 'Project Phantom' and offshore transfers. Key files still locked.", suspense:8, collision:true, reveal:"Marcus secretly contacts IT to slow the decryption" },
    { id:12, action:"Interviews Marcus Hale about Project Phantom", description:"Marcus smoothly explains it as 'classified R&D' with doctored documentation.", suspense:9, collision:true, reveal:"Reader watches Marcus lie with practiced ease" },
    { id:13, action:"Forensic analysis of financial audit returns", description:"Audit was altered, but origin untraceable. Trail leads to a shared company printer.", suspense:8, collision:false, reveal:"Reader knows Marcus forged it" },
    { id:14, action:"DNA results from brandy glass arrive", description:"DNA matches Ryan Torres. But glass shards don't match the wound pattern.", suspense:9, collision:false, reveal:"DNA planted from Ryan's old coffee mug" },
    { id:15, action:"Final push to crack laptop encryption", description:"60% of files decrypted. Crucial financial records remain locked. Hours left.", suspense:9, collision:false, reveal:"Reader agonizes: the truth is one password away" },
    { id:16, action:"Confronts the DA with doubts", description:"DA gives him until midnight to find an alternative suspect. Charges filed otherwise.", suspense:10, collision:false, reveal:"The countdown reaches its crisis point" },
    { id:17, action:"Reviews all evidence, notices timeline gap", description:"9:40 PM timestamp, 9:22 PM blackout, Clara's override. Too tight for an outsider. But no proof.", suspense:10, collision:false, reveal:"Cole reaches the edge of truth but can't cross" },
    { id:18, action:"Files his report at midnight", description:"'Unresolved inconsistencies' noted. Ryan Torres is charged. Cole is haunted by the feeling the real killer walks free.", suspense:10, collision:false, reveal:"Marcus Hale smiles reading the news. The reader alone carries the truth." },
  ],
  evaluation: {
    logic_analyst: { score: 7.8, prediction_correct: false, issues: 2 },
    intuitive_reader: { score: 8.2, prediction_correct: false, issues: 1 },
    genre_expert: { score: 7.5, prediction_correct: false, issues: 3, pacing: "Strong build, slight plateau at points 4-5" },
  },
  refinement: { issues_found: 3, issues_fixed: 2, details: [
    "Plot points 4-5: pacing improved with added time pressure",
    "Plot point 9: strengthened the cash payment suspicion thread",
  ]},
  story_text: `# Shadows of Deception

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

The investigation deepened. Cole found Eleanor had been investigating "Project Phantom" - large financial transfers to offshore accounts. The forged audit report on her desk had been altered, but by whom?

When Cole asked Marcus about Project Phantom, the VP didn't miss a beat. "Classified R&D. I can get you the authorization documents." The paperwork arrived within the hour, complete and convincing.

*The reader knows every page is forged. Marcus spent three nights fabricating them, using Eleanor's own forensic techniques against the investigation she started.*

Meanwhile, the clock was ticking. Eleanor's laptop held encrypted files that might blow the case open, but IT needed 48 hours they didn't have. The DA was circling, ready to charge Torres.

Cole could feel the truth slipping through his fingers like smoke.

---

## Chapter 4: The Conspiracy Holds

Every path Cole followed led to a dead end - or worse, back to Ryan Torres. Clara's alibi checked out. Henry's dinner receipt placed him at Marcello's. The DNA on the brandy glass matched Torres.

But the timeline nagged at him. The 22-minute camera gap. Clara's security override. The janitor's 9:40 PM timestamp. The window was too tight for an outside intruder.

It pointed to an inside job. Cole knew it in his gut. But knowing and proving were separated by an ocean of circumstantial evidence, and he was running out of time.

---

## Chapter 5: Midnight

The DA's deadline arrived like a verdict. Cole filed his report at 11:58 PM. "Unresolved inconsistencies warrant further investigation." But without a viable alternative suspect, Ryan Torres was charged with murder.

Marcus Hale read about it the next morning over coffee, the ghost of a smile playing at his lips. Clara Nguyen called in sick. Henry Whitaker transferred funds one last time, closing the offshore accounts forever.

And Jonathan Cole sat in his car outside NovaTech, staring up at the dark fifth-floor window, haunted by the certainty that the truth was still in there somewhere - locked behind encryption he couldn't break, hidden in footage that no longer existed.

The conspiracy held. The mirror remained unbroken.

*But the reader carries the weight of what really happened - and the knowledge that sometimes, the smoke clears too late.*

---

**THE END**`,
  meta: { model: "Qwen2.5-7B-Instruct", plot_points: 18, suspense: "8.2/10", countdown: "72h" },
},

// ===== Story 2: Shadow Partner (Pharmaceutical Empire) =====
{
  crime: {
    crime_type: "murder",
    setting: "Blackmoor Estate - Pharmaceutical Empire",
    victim: { name: "Richard Harrow", occupation: "Pharmaceutical Tycoon" },
    criminal: { name: "Evelyn Cross", occupation: "Veteran Detective (Killer-Detective)", motive: "Revenge for daughter's death caused by victim's tainted drugs", means: "Insider knowledge of forensic procedures", opportunity: "Staged robbery at secluded estate" },
    conspirators: [
      { name: "Captain Lyle", occupation: "County Sheriff", leverage: "Owes Evelyn personal favors", alibi: "Facilitated Evelyn's assignment to the case" },
    ],
    evidence: [
      { id: "E1", type: "physical", description: "Antique .38 revolver from victim's collection", location: "Study", steps: 2, real_meaning: "Evelyn swapped the gun for a replica" },
      { id: "E2", type: "digital", description: "Security camera gap (1:15-1:30 AM)", location: "Estate surveillance", steps: 3, real_meaning: "Evelyn disabled cameras with old police credentials" },
      { id: "E3", type: "physical", description: "Belladonna traces in victim's system", location: "Toxicology report", steps: 2, real_meaning: "Matches rare tincture from Evelyn's narcotics work" },
      { id: "E4", type: "physical", description: "Torn glove fiber on broken glass", location: "Crime scene", steps: 2, real_meaning: "Identical to Evelyn's vehicle trunk lining" },
      { id: "E5", type: "documentary", description: "Torn page from Lily's journal", location: "Victim's trash", steps: 3, real_meaning: "Directly links victim to Lily's death and Evelyn's motive" },
    ],
  },
  fabricated: {
    fake_suspect: { name: "David Kenset", occupation: "Estranged business partner", fake_motive: "Fired under mysterious circumstances, robbery for revenge" },
    cover_story: "Disgruntled former business partner staged a robbery gone wrong. Hair fiber planted at his office implicates him.",
    alibis: { "Evelyn Cross": "At home preparing case files (unverifiable)", "Captain Lyle": "On duty at the station" },
  },
  detective: {
    name: "Detective Marcus Cole",
    background: "34, sharp-witted, idealistic, prone to trusting people",
    personal_stakes: "First major homicide case - career-defining moment. His mentor recommended him personally.",
    dire_consequence: "If he fails, an innocent man goes to prison and the real killer becomes his trusted partner forever.",
    deadline_reason: "Key forensic evidence degrades within 96 hours due to estate's environmental conditions.",
  },
  plot_points: [
    { id:1, action:"Arrives at Blackmoor Estate with partner Evelyn Cross", description:"Cole processes the study. Single bullet wound, antique revolver, staged robbery scene. His new partner Evelyn offers calm, insightful observations.", suspense:4, collision:false, reveal:"Reader knows Evelyn is the killer, standing beside the detective she must deceive" },
    { id:2, action:"Examines the murder weapon and ballistics", description:"The .38 revolver matches Harrow's collection. No fingerprints. Evelyn notes 'whoever did this knew forensics.'", suspense:5, collision:false, reveal:"Evelyn literally describing her own methodology" },
    { id:3, action:"Discovers belladonna traces in toxicology report", description:"Unusual poison found in victim's system. Evelyn suggests it could be 'self-medication' and steers Cole toward other leads.", suspense:6, collision:true, reveal:"Reader watches Evelyn actively misdirect Cole away from her signature" },
    { id:4, action:"Interviews David Kenset (planted suspect)", description:"Kenset is nervous, defensive. Hair fiber found at his office. His alibi has gaps. Evelyn subtly reinforces suspicion.", suspense:5, collision:false, reveal:"Reader knows every piece of evidence against Kenset was planted by Evelyn" },
    { id:5, action:"Investigates the security camera gap", description:"15-minute blackout at the estate. Estate manager blames a power surge. Cole is skeptical.", suspense:6, collision:false, reveal:"Evelyn used her old police credentials to disable cameras remotely" },
    { id:6, action:"Finds torn glove fiber at crime scene", description:"Forensics identifies it as high-end leather. Cole wants to trace the manufacturer. Evelyn volunteers to handle the lead.", suspense:7, collision:true, reveal:"Evelyn takes the lead specifically to bury it - the fiber matches her own vehicle" },
    { id:7, action:"Discovers Lily Cross connection in financial records", description:"Cole finds a $500K settlement to 'Lily Cross' in Harrow's files. The name rings a bell. Evelyn freezes momentarily.", suspense:8, collision:true, reveal:"Cole is inches from discovering Evelyn's motive. She deflects with practiced composure." },
    { id:8, action:"Interviews Rebecca Voss (victim's daughter)", description:"Rebecca was estranged, sent angry texts. Her alibi has holes. Evelyn pushes Cole to focus on her.", suspense:6, collision:false, reveal:"Another innocent suspect thrown into the mix by Evelyn's manipulation" },
    { id:9, action:"Analyzes the forged letter in Henry's office", description:"Handwriting analysis is inconclusive. Cole senses something is off about the letter. Evelyn dismisses it as 'a stretch.'", suspense:7, collision:false, reveal:"Evelyn forged the letter herself using forensic techniques she learned decades ago" },
    { id:10, action:"Searches for the torn journal page", description:"Cole finds fragments of Lily's journal in Harrow's trash. The entries describe threats. He wants to dig deeper.", suspense:8, collision:true, reveal:"The journal page is the one piece of evidence that could unravel everything" },
    { id:11, action:"Cross-references belladonna with known sources", description:"The poison matches a rare tincture once used in narcotics investigations. Cole checks old case files.", suspense:9, collision:true, reveal:"Evelyn intercepts the request and provides 'updated' files with the reference removed" },
    { id:12, action:"Notices Evelyn avoids discussing the manuscript", description:"Harrow was writing an expose. Cole asks Evelyn about it. She changes the subject smoothly.", suspense:8, collision:false, reveal:"The manuscript contains Evelyn's darkest secrets - if Cole reads it, the game is over" },
    { id:13, action:"Forensic timeline reconstruction", description:"The timeline is impossibly tight for an outside intruder. Cole voices doubts. Evelyn suggests a 'professional hitman.'", suspense:9, collision:false, reveal:"The only person who fits the timeline is Evelyn herself" },
    { id:14, action:"Discovers Evelyn's personal connection to the victim", description:"A colleague mentions Evelyn's daughter died in a case connected to Harrow's company. Cole confronts Evelyn.", suspense:10, collision:true, reveal:"The truth surfaces but Evelyn has prepared for this moment" },
    { id:15, action:"Evelyn provides emotional explanation", description:"She tearfully admits her daughter's death but insists it gives her MORE motivation to solve the case properly. Cole believes her.", suspense:9, collision:false, reveal:"Reader watches Evelyn weaponize her own grief as a shield" },
    { id:16, action:"Final evidence review under deadline pressure", description:"96 hours nearly up. Forensics degrading. Multiple suspects, no definitive proof pointing to anyone but Kenset.", suspense:10, collision:false, reveal:"Every path to the truth has been carefully closed by Evelyn" },
    { id:17, action:"Cole files his final report", description:"David Kenset is arrested. Cole feels uneasy but has no alternative theory. Evelyn pats his shoulder: 'You did good work, Cole.'", suspense:10, collision:false, reveal:"The killer congratulates the detective on his failure. The partnership survives." },
  ],
  evaluation: {
    logic_analyst: { score: 8.4, prediction_correct: false, issues: 1 },
    intuitive_reader: { score: 8.8, prediction_correct: false, issues: 1 },
    genre_expert: { score: 7.9, prediction_correct: false, issues: 2, pacing: "Excellent dual-detective tension, minor plateau at points 8-9" },
  },
  refinement: { issues_found: 2, issues_fixed: 2, details: [
    "Plot point 8-9: tightened pacing with deadline pressure",
    "Plot point 4: added more tension to Kenset interview",
  ]},
  story_text: `# Shadow Partner

*A Mystery Novel by SmokeMirror AI*

---

## Prologue: Blood on the Brimstone

The rain had stopped, but the air still reeked of damp earth and gunpowder. Evelyn Cross stood in the study of Richard Harrow's manor, her gloved hands steady despite the tremor in her pulse. The body lay sprawled across the Persian rug, a single bullet wound center-mass.

She crouched beside him, checking for a pulse - just habit, really - and wiped the barrel of the .38 again. No fingerprints; she'd swapped the gun for a replica from his own collection. A clever trick. He would've loved it - if he hadn't been dead.

Revenge tasted colder than she'd expected.

Richard Harrow's pharmaceutical empire had funneled tainted drugs into underserved hospitals. His cost-cutting measures led to the death of Evelyn's teenage daughter, Lily, three years ago. An "accident," they'd called it. No trial, no accountability.

Evelyn hadn't moved. She'd waited. And now, she needed to stay ahead of the investigation. To do that, she needed to be *inside* it.

By morning, she was assigned to the case - as part of a duo with Detective Marcus Cole, the department's rising star.

---

## Chapter 1: Mirrored Shadows

Detective Marcus Cole adjusted his satchel as he stepped onto the gravel drive of Harrow Manor. Inside, the study glowed with amber light over the Persian rug where Richard Harrow lay.

A woman already stood at the corpse's side. Evelyn Cross turned, offering a measured smile. "Cole." Her eyes studied him before shifting to the body. "He was clean when we found him. No signs of struggle."

"No gun in his hand?" Cole asked.

"No. But it was his own weapon. A .38 revolver." She gestured toward the hallway. "Classic setup - make it look like a suicide, but leave just enough ambiguity."

Cole liked the way she thought - not in absolutes, but in possibilities. There was a fluidity to her reasoning that reminded him of his first mentor.

*What Cole couldn't know was that every insight Evelyn offered was carefully calibrated - true enough to seem helpful, misleading enough to protect herself.*

---

## Chapter 2: The Art of Misdirection

The investigation of David Kenset proceeded exactly as Evelyn had planned. Hair fibers at his office. Financial motives. A shaky alibi. Cole built the case methodically, unaware that his partner was feeding him breadcrumbs from a trail she'd laid herself.

When Cole found the $500,000 settlement to "Lily Cross" in Harrow's records, Evelyn felt the floor shift beneath her. The name hung in the air between them.

"Lily Cross," Cole repeated. "That sounds familiar."

Evelyn forced neutrality. "I don't recognize it either. But I wouldn't be surprised if it ties back to Harrow somehow."

Cole studied her for a moment. Then he moved on. And Evelyn breathed again.

---

## Chapter 3: The Dance

Every lead Cole pursued, Evelyn was one step ahead. When he found belladonna traces, she suggested self-medication. When he traced the glove fiber, she volunteered to handle the lead - and buried it. When colleagues mentioned her daughter's connection to Harrow, she weaponized her own grief as a shield.

"You think I'd compromise an investigation over personal pain?" she asked Cole, eyes glistening with tears that were entirely real. "My daughter's death gives me MORE reason to find the truth."

Cole believed her. He had no reason not to.

*The reader watches Evelyn walk the razor's edge - genuine grief and calculated deception woven so tightly that even she can no longer tell them apart.*

---

## Chapter 4: The Curtain Falls

Ninety-six hours. That was all they had before the forensic evidence degraded beyond use. And in that window, every path to the truth was methodically closed.

David Kenset was arrested on a Tuesday. Cole wrote the report with an unease he couldn't name. The evidence was there - circumstantial but damning. The timeline worked, barely. The motive was clear.

Evelyn read the report over his shoulder and patted his arm. "You did good work, Cole."

He nodded, but something in his gut wouldn't settle. Years later, on sleepless nights, he would replay their partnership moment by moment, searching for the seam in her performance, the one tell she must have let slip.

He never found it.

*The killer and the detective shake hands in the parking lot. Evelyn drives home to an empty house where Lily's photo watches from the mantelpiece. She pours a glass of whiskey and stares at it for a long time before drinking.*

*Justice, she thinks. But the word tastes like ash.*

---

**THE END**`,
  meta: { model: "Qwen2.5-7B-Instruct", plot_points: 17, suspense: "8.4/10", countdown: "96h" },
},

// ===== Story 3: Shadows of Deception v2 (Ravenswood Estate) =====
{
  crime: {
    crime_type: "murder",
    setting: "Ravenswood Estate - Victorian Manor",
    victim: { name: "Dr. Eleanor Voss", occupation: "Retired Medical Examiner / Investigative Journalist" },
    criminal: { name: "Marcus Hale", occupation: "Senior Detective (Killer-Detective)", motive: "Revenge - victim exposed his corruption and threatened to publish a memoir", means: "Forensic expertise and police credentials", opportunity: "Charity gala cover" },
    conspirators: [
      { name: "Clara Nguyen", occupation: "Housemaid", leverage: "Eleanor discovered Clara's embezzlement of household funds", alibi: "Claims she was cleaning the east wing until 11 PM" },
      { name: "Henry Whitaker", occupation: "Business Partner", leverage: "Financial entanglement with Marcus's schemes", alibi: "Claims he was at a poker game" },
    ],
    evidence: [
      { id: "E1", type: "physical", description: "Shattered brandy glass embedded in victim's temple", location: "Study", steps: 2, real_meaning: "Murder weapon - staged as accident" },
      { id: "E2", type: "digital", description: "Security cameras stopped recording 1:15-1:30 AM", location: "Estate surveillance", steps: 3, real_meaning: "Marcus disabled them with old police credentials" },
      { id: "E3", type: "physical", description: "Belladonna traces in victim's blood", location: "Toxicology lab", steps: 2, real_meaning: "Sedative used by Marcus from his narcotics days" },
      { id: "E4", type: "physical", description: "Torn black leather glove fiber", location: "Crime scene glass", steps: 2, real_meaning: "Matches Marcus's vehicle trunk lining" },
      { id: "E5", type: "documentary", description: "Victim's unpublished manuscript draft", location: "Eleanor's safe", steps: 3, real_meaning: "Contains proof of Marcus's corruption and wife's disappearance" },
    ],
  },
  fabricated: {
    fake_suspect: { name: "Rebecca Voss", occupation: "Estranged daughter", fake_motive: "Inheritance dispute - Eleanor cut her out of the will" },
    cover_story: "The estranged daughter broke in during the gala, confronted her mother over the will, and the argument turned violent. A deepfake audio clip and planted evidence support this.",
    alibis: { "Marcus Hale": "20+ witnesses at the charity gala, deepfake audio with bartender", "Clara Nguyen": "Cleaning east wing - no logs to verify" },
  },
  detective: {
    name: "Detective Jonathan Cole",
    background: "Analytical, methodical, struggles with trust issues after recent betrayal",
    personal_stakes: "His mentor Captain recommended him for this career-defining case. Failure means returning to cold cases.",
    dire_consequence: "Rebecca Voss will be wrongfully convicted and Cole's career stalls permanently.",
    deadline_reason: "The DA's office needs charges filed within 5 days or the case goes cold.",
  },
  plot_points: [
    { id:1, action:"Arrives at Ravenswood Estate in the rain", description:"Cole processes the study - body on Persian rug, shattered glass, staged break-in. His assigned partner Marcus Hale is already on scene.", suspense:4, collision:false, reveal:"Reader knows Marcus is the killer, calmly guiding the investigation" },
    { id:2, action:"Documents the brandy glass and wound pattern", description:"Something about the glass shards doesn't match a natural fall. Cole photographs everything meticulously.", suspense:5, collision:false, reveal:"The glass was deliberately broken and positioned post-mortem" },
    { id:3, action:"Interviews the five suspects", description:"Rebecca, Henry, Clara, Olivia Grant, and Thomas Reed all have motives and shaky alibis. Marcus subtly steers focus toward Rebecca.", suspense:5, collision:false, reveal:"Marcus is orchestrating who Cole investigates and in what order" },
    { id:4, action:"Discovers belladonna in toxicology", description:"Unusual poison in Eleanor's system. Marcus suggests 'maybe she was self-medicating' and redirects to the glass wound.", suspense:6, collision:true, reveal:"Marcus deflects from the one clue that leads directly to him" },
    { id:5, action:"Finds the forged letter in Henry's office", description:"Handwriting appears to match Eleanor's. 'You'll regret this.' Henry looks guilty.", suspense:6, collision:false, reveal:"Marcus forged it using techniques he learned in forensics training" },
    { id:6, action:"Investigates the 15-minute security gap", description:"Cameras went dark at 1:15 AM. The estate manager attributes it to a power surge from the storm.", suspense:7, collision:false, reveal:"Marcus remotely disabled the cameras" },
    { id:7, action:"Traces the torn glove fiber", description:"High-end leather, custom make. Cole wants the manufacturer's records. Marcus volunteers to handle the trace.", suspense:7, collision:true, reveal:"Marcus takes the lead to ensure the fiber is never connected to his vehicle" },
    { id:8, action:"Discovers Rebecca's text messages", description:"Angry messages to Eleanor: 'You'll ruin everyone again.' Rebecca's alibi has holes.", suspense:7, collision:false, reveal:"Messages were pre-scheduled for a scam unrelated to the murder" },
    { id:9, action:"Finds mud on Thomas Reed's boots matching estate soil", description:"Thomas claims he never visited Ravenswood. The mud says otherwise. Marcus builds the case against Thomas.", suspense:8, collision:false, reveal:"Thomas hiked there days earlier to scout for a cabin purchase" },
    { id:10, action:"Locates Eleanor's manuscript draft fragments", description:"Cole finds references to a detective's corruption in Eleanor's notes. The name is redacted.", suspense:9, collision:true, reveal:"Marcus races to destroy the full manuscript before Cole can read it" },
    { id:11, action:"Traces the belladonna to a rare forensic source", description:"Old narcotics division records might identify who had access. Cole requests the files.", suspense:9, collision:true, reveal:"Marcus intercepts and provides 'updated' files with his name removed" },
    { id:12, action:"Cole notices Marcus avoids the manuscript topic", description:"Every time the unpublished book comes up, Marcus changes the subject. Cole notes this quietly.", suspense:8, collision:false, reveal:"Reader holds their breath - is Cole finally seeing through the mask?" },
    { id:13, action:"Timeline reconstruction reveals impossibility", description:"An outside intruder couldn't have entered, killed, staged the scene, and escaped in the camera gap window.", suspense:9, collision:false, reveal:"Only someone already inside - like a fellow detective - fits the timeline" },
    { id:14, action:"Confronts Marcus about his connection to Eleanor", description:"A colleague mentions Marcus and Eleanor had history. Cole asks directly. Marcus admits they were acquaintances.", suspense:10, collision:true, reveal:"Marcus admits the minimum truth and hides the rest behind emotion" },
    { id:15, action:"Final 48 hours - pressure mounts from DA", description:"Rebecca's lawyer is threatening media exposure. The DA demands an arrest. Evidence points to Rebecca.", suspense:10, collision:false, reveal:"The conspiracy's endgame: maximum pressure, minimum time" },
    { id:16, action:"Cole files his report", description:"Rebecca Voss is charged. Cole writes 'substantial doubts remain' in his personal notes. Marcus shakes his hand.", suspense:10, collision:false, reveal:"The killer congratulates Cole on 'a thorough investigation.' The mirror holds." },
  ],
  evaluation: {
    logic_analyst: { score: 7.6, prediction_correct: false, issues: 3 },
    intuitive_reader: { score: 8.0, prediction_correct: false, issues: 2 },
    genre_expert: { score: 8.1, prediction_correct: false, issues: 2, pacing: "Strong dual-detective irony, good escalation curve" },
  },
  refinement: { issues_found: 4, issues_fixed: 3, details: [
    "Plot points 3-4: added urgency to initial suspect interviews",
    "Plot point 9: Thomas Reed subplot tightened",
    "Plot point 12: strengthened Cole's growing suspicion",
  ]},
  story_text: `# Shadows of Deception

*A Mystery Novel by SmokeMirror AI*

---

## Prologue: The Perfect Lie

Detective Marcus Hale stood over the body, rainwater dripping from his trench coat onto the Persian rug. Dr. Eleanor Voss lay facedown in the study of her Ravenswood estate, a single shard of shattered brandy glass embedded in her temple.

Marcus had spent years cultivating his reputation as one of the city's most unflappable homicide detectives. But tonight, he wasn't solving a case - he was closing a chapter. Eleven years ago, Eleanor had exposed him as the corrupt officer who'd falsified evidence. His career had been salvaged by backroom deals, but Eleanor's testimony had cost him everything: his badge, his marriage, his peace of mind. When he learned she was compiling a tell-all memoir - Marcus knew she had to die.

He had planned it meticulously. Invited her to a charity gala, slipped her a sedative. The staged break-in was his masterpiece. And when morning came, he'd file the case as a botched robbery.

That detective, Jonathan Cole, was already en route to Ravenswood.

---

## Chapter 1: Rainfall of Secrets

Cole arrived as dawn broke over the estate. The study was a tableau of carefully arranged violence - overturned desk, broken window, the body on the rug. His assigned partner, the legendary Marcus Hale, was already there.

"Single wound," Marcus said, gesturing at the glass shard. "Looks like she fell and hit the brandy glass. But the break-in..." He shook his head. "This doesn't feel random."

Cole knelt beside the body. Something about the glass shards bothered him - the pattern was too uniform, as if someone had broken the glass first and then positioned the victim. He filed the observation away.

*The reader knows Marcus arranged every detail of this scene, and he's now watching Cole examine his own handiwork.*

---

## Chapter 2: Five Faces of Suspicion

The suspects lined up like characters in a play - each with motive, each with cracks in their alibis. Rebecca the estranged daughter, Henry the business partner, Clara the nervous housemaid, Olivia the rival journalist, Thomas the retired captain.

Marcus guided Cole through the interviews with practiced ease, always steering attention toward Rebecca. Her angry text messages. Her inheritance motive. Her shaky alibi.

"The daughter," Marcus said over coffee. "It's almost always family."

Cole nodded. But the belladonna traces in the toxicology report nagged at him. That wasn't a crime of passion. That was preparation.

---

## Chapter 3: The Manuscript

The breakthrough almost came on day three. Cole found fragments of Eleanor's unpublished manuscript - references to a corrupt detective, redacted names, dates that matched real cases. If he could find the full draft...

"The manuscript is probably a dead end," Marcus said quickly. "Eleanor was known for exaggeration. Let's focus on the physical evidence."

*The reader watches Marcus's composure crack for just a fraction of a second - then reassemble perfectly.*

Cole let it go. He shouldn't have.

---

## Chapter 4: Walls Closing In

The DA's deadline pressed like a vise. Five days. Rebecca's lawyer was threatening media exposure. The evidence - planted, forged, and manipulated - pointed overwhelmingly at the daughter.

Cole spent the last night reviewing everything. The timeline was too tight for an outsider. The belladonna came from a forensic source. The manuscript mentioned a corrupt detective. The glove fiber that Marcus had volunteered to trace - and never mentioned again.

The pieces were there. But without the manuscript, without the full toxicology chain, without time - they were just suspicions.

He filed his report. Rebecca Voss was charged. Marcus shook his hand. "Thorough work, Cole. Really thorough."

Cole drove home in silence, the word "thorough" echoing like a verdict. He kept his personal notes in a locked drawer: *Something is wrong. I just can't prove what.*

---

## Epilogue

Marcus Hale retired six months later to general acclaim. At his farewell dinner, he gave a speech about justice and persistence that moved half the room to tears.

Jonathan Cole transferred to a new precinct. On quiet evenings, he would pull out the Ravenswood file and stare at the timeline, at the redacted manuscript pages, at the belladonna report. Searching for the thread he'd missed.

He never found it. But he never stopped looking.

*And the reader knows that somewhere in a locked evidence room, Eleanor's full manuscript sits in a sealed box - the truth waiting patiently for someone brave enough to open it.*

---

**THE END**`,
  meta: { model: "Qwen2.5-7B-Instruct", plot_points: 16, suspense: "7.9/10", countdown: "5 days" },
},

// ===== Story 4: Shadows Over QuantumTech (Tech Startup - Qwen2.5-7B) =====
{
  crime: {
    crime_type: "murder",
    setting: "Tech Startup - QuantumTech Inc.",
    victim: { name: "Alex Chen", occupation: "CEO of QuantumTech Inc." },
    criminal: { name: "Zara Li", occupation: "Director of Operations", motive: "Wanted to take over the company; Alex refused to step down despite losing control", means: "Access to company security systems and financial records", opportunity: "Alex was working late finalizing documents that could expose her unethical practices" },
    conspirators: [
      { name: "Victor Tan", occupation: "Chief Financial Officer", leverage: "Owed money to Zara from a failed investment deal", alibi: "Claimed he was on a business trip out of town" },
      { name: "Mia Wang", occupation: "IT Manager", leverage: "Blackmailed over embezzlement scandal", alibi: "Said she was attending a conference in another city" },
      { name: "Samuel Lee", occupation: "Junior Developer", leverage: "Promised promotion and raise for his family's medical expenses", alibi: "Claimed he was working overtime in the development lab until midnight" },
    ],
    evidence: [
      { id: "E1", type: "physical", description: "Vial of unknown liquid (sedative) in Zara's desk drawer", location: "Zara Li's Office", steps: 2, real_meaning: "Confirms Zara's involvement in preparing the murder weapon" },
      { id: "E2", type: "digital", description: "Surveillance footage showing figure matching Samuel's description", location: "Security System", steps: 2, real_meaning: "Someone was there to distract security, supporting Samuel's role" },
      { id: "E3", type: "documentary", description: "Financial records with unexplained withdrawals before murder", location: "Victor Tan's Computer", steps: 2, real_meaning: "Points to Victor's involvement in covering up the murder financially" },
    ],
  },
  fabricated: {
    fake_suspect: { name: "David Kim", occupation: "Sales Representative at QuantumTech", fake_motive: "Long-standing grudge against Alex for rejecting his sales pitches and undermining his reputation" },
    cover_story: "David Kim, a disgruntled employee with a history of frustration towards Alex Chen, acted alone in a moment of rage. His possession of the sedative and a fabricated note link him to the crime.",
    alibis: { "Victor Tan": "Claimed urgent business trip to Europe with hotel reservations", "Mia Wang": "Attended a high-profile industry conference in NYC, confirmed through check-ins and social media", "Samuel Lee": "Working late at R&D lab, verified by security pass and smart home system logs" },
  },
  detective: {
    name: "Detective Zhang",
    background: "Seasoned investigator with sharp analytical skills",
    personal_stakes: "Assigned lead on QuantumTech's highest-profile case; reputation on the line",
    dire_consequence: "If unsolved, an innocent man (David Kim) will be charged with murder",
    deadline_reason: "Corporate security systems will overwrite critical logs in the automatic maintenance cycle",
  },
  plot_points: [
    { id:1, action:"Interviews Samuel Lee in development lab", description:"Zhang visits QuantumTech. Samuel shows recent code changes to explain his late-night presence. Zhang notices subtle formatting changes but can't pin them down.", suspense:4, collision:true, reveal:"Reader sees Samuel actively protecting the conspiracy" },
    { id:2, action:"Interviews Victor Tan at headquarters", description:"Victor calmly presents his business dinner alibi. Offers to review emails and financial records to verify.", suspense:6, collision:true, reveal:"Reader watches Victor deploy pre-arranged cover story" },
    { id:3, action:"Interviews Mia Wang about software glitch", description:"Mia mentions a 'software glitch' that disrupted cameras. She names Zara Li as unusually anxious that night.", suspense:7, collision:true, reveal:"Reader sees Mia deflecting attention away from her role" },
    { id:4, action:"Examines surveillance footage", description:"Footage shows figure matching Samuel's description entering/exiting during the murder window. Samuel contacts Zhang with 'new information.'", suspense:9, collision:true, reveal:"Reader sees Samuel actively steering the investigation" },
    { id:5, action:"Examines Zara Li's office desk", description:"Zhang finds evidence and verifies Victor's alibi. Business trip story appears consistent on the surface.", suspense:10, collision:false, reveal:"Reader knows Victor's alibi is fabricated" },
    { id:6, action:"Interviews David Kim in sales department", description:"David provides his version of events. Zhang also checks Mia's conference alibi - appears solid.", suspense:10, collision:false, reveal:"Reader knows Mia's alibi is fabricated" },
    { id:7, action:"Examines private meeting room", description:"Zhang searches for overlooked physical evidence. Checks Samuel's alibi - overtime story matches security logs.", suspense:10, collision:false, reveal:"Reader knows Samuel's alibi is fabricated" },
    { id:8, action:"Examines Victor's financial records", description:"Unusual withdrawals found shortly before the murder. Partial progress - amounts suspicious but origin unclear.", suspense:10, collision:false, reveal:"Reader knows these records point to Victor's involvement" },
    { id:9, action:"Re-examines meeting room", description:"Budget cuts have left security systems outdated. Camera recordings from that night are incomplete or lost.", suspense:10, collision:false, reveal:null },
    { id:10, action:"Interviews David Kim at home", description:"Kim's home security system triggers a false alarm during the interview. Local police called in.", suspense:11, collision:false, reveal:null },
    { id:11, action:"Examines David Kim's computer", description:"Zhang obtains full financial records showing unexplained withdrawals. Evidence seemingly implicates David Kim.", suspense:11, collision:false, reveal:"Reader knows the true meaning: records point to Victor's cover-up" },
    { id:13, action:"Interviews Zara Li at home", description:"Zhang obtains full surveillance footage. Figure matches Samuel but evidence is presented as implicating David.", suspense:10, collision:false, reveal:"Reader knows footage actually shows Samuel distracting security" },
    { id:16, action:"Interviews Alex Chen's former colleagues", description:"Victor suggests interviewing the new IT department head, Mr. Li, diverting the investigation further.", suspense:11, collision:true, reveal:"Reader sees Victor actively protecting the conspiracy" },
    { id:17, action:"Interviews new IT head Mr. Li", description:"Mia suggests re-examining security logs from the crime night - another misdirection.", suspense:10, collision:true, reveal:"Reader sees Mia actively protecting the conspiracy" },
    { id:20, action:"Interviews CEO's assistant Sarah Chen", description:"Zhang obtains the sedative vial evidence. It confirms involvement but is presented as implicating David Kim.", suspense:10, collision:false, reveal:"Reader knows vial confirms Zara's involvement in preparing the murder weapon" },
    { id:22, action:"Interviews new IT head Mr. Li again", description:"More evidence gathered, all seemingly pointing toward David Kim.", suspense:10, collision:false, reveal:null },
    { id:23, action:"Re-examines crime scene exterior", description:"Mia approaches Zhang and suggests re-examining IT systems for unauthorized access - more misdirection.", suspense:10, collision:true, reveal:"Reader sees Mia actively protecting the conspiracy" },
    { id:25, action:"Interviews Xiao Li's mentor", description:"Victor asks about financial discrepancies in Xiao Li's expense reports - final misdirection before case closes.", suspense:10, collision:true, reveal:"Reader sees Victor actively protecting the conspiracy" },
  ],
  evaluation: {
    logic_analyst: { score: 6.87, prediction_correct: false, issues: 0 },
    intuitive_reader: { score: 4.98, prediction_correct: false, issues: 6 },
    genre_expert: { score: 5.9, prediction_correct: false, pacing: "Flat middle section, premature peak at plot point 4" },
  },
  refinement: { issues_found: 7, issues_fixed: 5, details: [
    "Addressed sharp suspense drops at plot points 13, 20",
    "Improved false alarm at David Kim's home for better engagement",
    "Strengthened administrative obstacle realism",
    "Fixed security budget-cut documentation gaps",
    "Revised unengaging plot points 15, 21 for better pacing",
  ]},
  story_text: `# Shadows Over QuantumTech

*A Novel*

---

## Prologue

In the dimly lit atrium of QuantumTech's headquarters, shadows danced under the flickering fluorescent lights, casting elongated silhouettes across the sleek, glass walls. The air was thick with tension, palpable as the scent of fresh coffee mingled with the faint aroma of disinfectant.

Alex Chen, once the commanding figure of this bustling corporate jungle, no longer held sway. His reign had crumbled amidst internal conflicts that left him sidelined yet still holding onto the symbolic power of his position. Across town, Zara Li waited impatiently, tapping out coded messages to her co-conspirators.

Victor Tan, Mia Wang, and Samuel Lee stood as pillars of her support, their roles orchestrated with meticulous precision. They had planned every detail, each communication carefully encrypted and dispersed among a network of fake personas designed to obscure their true intentions.

David Kim, the newly appointed chief investigator, arrived at the scene just as dawn broke. He carried with him a relentless drive to uncover the truth. Yet, as he began piecing together the fragments of evidence, the pieces seemed to point towards an unlikely culprit - a junior developer named Samuel Lee, whose programming skills were more than enough to cover any digital tracks.

But in the darkness that lurked beneath the surface of QuantumTech, where lies were as common as data breaches, the truth was far from simple.

---

## Chapter 1: The Discovery

The rain was relentless, hammering against the glass windows of Detective Zhang's office. He sat behind his cluttered desk, scanning the file - Alex Chen, thirty-five years old, tech mogul, last seen alive at QuantumTech Inc. late Thursday evening.

Detective Liu entered with new evidence: unusual transactions, transfers to offshore accounts from Alex's personal account shortly after a late meeting ended. The numbers didn't add up.

Zhang drove to QuantumTech's development lab. Samuel Lee stood behind a desk covered in monitors and technical manuals, his face bearing traces of fatigue. He showed Zhang code updates for a new security protocol - a sophisticated encryption algorithm. Something caught Zhang's eye: a subtle formatting change near the bottom of one page. So minor he nearly missed it.

*The reader knows: Samuel's nervousness isn't about the code. It's about the conspiracy he's protecting.*

Victor Tan called, his voice steady, almost too composed. He offered emails and financial records to verify his alibi. Cooperative. Helpful. The perfect mask.

*The reader knows: Victor's helpfulness is itself a weapon of misdirection.*

Back at the lab, Samuel grew agitated. His hands fidgeted, his gaze darted restlessly. "I wasn't anywhere near the scene of the crime. That night, I was locked in this very room, finalizing these updates."

Zhang studied his face, searching for deceit. Something didn't ring true - perhaps the way Lee's hands kept tapping the table, the subtle hesitation when mentioning his break. But without concrete evidence, the detective moved on.

---

## Chapter 2: First Threads

Mia Wang sat at a conference table, her hair loose and tangled, looking exhausted. She mentioned a software glitch that disrupted cameras around nine o'clock - a sudden freeze, the video feed going dark.

"Zara Li was especially anxious about the delay," Mia added, "pacing around the room and checking her watch frequently."

*The reader knows: Mia is the one who engineered the camera disruption. Her mention of Zara's anxiety is calculated - just enough truth to seem helpful, wrapped in deflection.*

Zhang examined the surveillance footage showing a shadowy figure matching Samuel's description. David Kim's phone records checked out. Victor Tan's financial records showed two unusual withdrawals near the time of the murder.

At the private meeting room, budget cuts had left security systems outdated. Fire alarms were prone to false activations, cameras frequently failed. The documentation from the night of the meeting was incomplete or lost.

Zhang found a faint fingerprint indentation in the carpet. A small discovery, but combined with Victor's suspicious withdrawals, the pieces were beginning to form a picture - though not the picture the conspirators intended.

---

## Chapter 3: Following the Trail

Zhang arrived at David Kim's home for a deeper interview. The home security system triggered during the visit - a false alarm that brought local police. More disruption, more delays.

Kim's financial records showed frequent, unexplained withdrawals. "Business can be unpredictable," Kim offered, avoiding eye contact.

The surveillance footage, now fully analyzed, showed the figure entering and exiting the building. All evidence was being carefully channeled toward David Kim. The real criminals' alibis held firm: Victor's business trip, Mia's conference, Samuel's overtime.

*The reader watches helplessly as every thread Zhang follows has been pre-woven by the conspirators, leading inexorably toward the wrong man.*

---

## Chapter 4: Smoke and Mirrors

Victor Tan suggested interviewing the new IT department head, Mr. Li - another diversion. Mia approached Zhang with her own suggestion: re-examine the company's IT systems for unauthorized access. Each helpful tip was another layer of misdirection.

Zhang obtained the sedative vial from Zara's desk drawer. Critical evidence - but in context, it was presented as linking to David Kim's opportunity, not Zara's guilt.

The detective's frustration mounted. Every lead seemed to dissolve into smoke. Every mirror reflected a different suspect. The truth was right in front of him, but the conspirators had constructed such an elaborate facade that distinguishing reality from fabrication had become nearly impossible.

---

## Chapter 5: Shifting Shadows

Xiao Li, the young intern, provided a crucial detail: Zara had come into the office around seven o'clock, claimed to need supplies, then vanished. No one saw her leave.

Victor asked about financial discrepancies in expense reports - the final misdirection. The case was closing around David Kim, the innocent man whose grudge against Alex made him the perfect fall guy.

Zhang could feel something was wrong. The evidence was too clean, too convenient. But without proof of the conspiracy, without a crack in the conspirators' unified front, he was trapped.

---

## Epilogue

Weeks have passed since the trial. The town remains shrouded in misty silence.

Victor Tan, once a man of wealth and influence, now finds himself reduced to quiet evenings sipping cheap wine. His fingers tremble slightly as he pours another glass. In the dim light, shadows dance across the walls, and he hears whispers that make him jump.

Mia Wang stands before a mirror, applying her makeup meticulously. The smile is false, tinged with bitterness. The guilt gnaws at her every day.

Samuel Lee has managed to compartmentalize his actions. He continues his work smoothly, but sometimes, in the dead of night, he lies awake, wondering if his lie will eventually be discovered.

Zara Li has found her own path. Under a different identity, she lives in a small apartment on the outskirts of the city. She reads old cases, admiring the detectives' tenacity, wishing she could have been like them. Yet even here, she feels watched.

David Kim's world has collapsed around him. His reputation is irreparably damaged. He spends most days locked away, poring over old newspapers, searching for any clue that might exonerate him.

Detective Zhang, unable to let go, occasionally flips through the case files. He dreams of Zara Li, of her calculated moves, her eerie calm. The name haunts him, taunting him with the knowledge that justice may have been thwarted.

In the heart of the city, an old clock tower stands, its chimes echoing through the empty streets. Hidden within it, the true story of the crime lies sealed away forever - a silent testament to the power of deceit and the enduring human capacity for betrayal.

---

**THE END**`,
  meta: { model: "Qwen2.5-7B-Instruct", plot_points: 25, suspense: "5.96/10", countdown: "Corporate log overwrite cycle" },
},

]; // END ALL_STORIES

// ===== App Logic =====

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

let generating = false;
let currentStory = null;

$('#btn-generate').addEventListener('click', startGeneration);
$('#btn-restart')?.addEventListener('click', () => {
  $('#pipeline').classList.add('hidden');
  $('#story-output').classList.add('hidden');
  $('#hero').classList.remove('hidden');
  $$('.step').forEach(s => { s.classList.remove('active','done'); s.querySelector('.step-content').innerHTML = ''; });
  generating = false;
});

async function startGeneration() {
  if (generating) return;
  generating = true;
  $('#btn-generate').disabled = true;
  $('#btn-generate').textContent = 'Generating...';

  // Pick a random story
  currentStory = ALL_STORIES[Math.floor(Math.random() * ALL_STORIES.length)];

  $('#hero').classList.add('hidden');
  $('#pipeline').classList.remove('hidden');

  await runPhase1();
  await runPhase2();
  await runPhase3();
  await runPhase4();
  await runPhase5();
  await runPhase6();

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
  for (let i = 1; i < n; i++) { $(`#step-${i}`).classList.remove('active'); $(`#step-${i}`).classList.add('done'); }
  $(`#step-${n}`).classList.add('active');
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// Phase 1
async function runPhase1() {
  activateStep(1);
  updateProgress(5, 'Phase 1/6: Generating crime backstory...');
  await sleep(800);
  const c = currentStory.crime;
  let html = `
    <div class="info-card">
      <h4>Crime: ${c.crime_type.toUpperCase()}</h4>
      <div class="info-row"><span class="label">Setting:</span> <span class="value">${c.setting}</span></div>
      <div class="info-row"><span class="label">Victim:</span> <span class="value">${c.victim.name} (${c.victim.occupation})</span></div>
      <div class="info-row"><span class="label">Criminal:</span> <span class="value">${c.criminal.name} (${c.criminal.occupation})</span></div>
      <div class="info-row"><span class="label">Motive:</span> <span class="value">${c.criminal.motive}</span></div>
    </div>
    <div class="info-card"><h4>Conspirators</h4>
      ${c.conspirators.map(co => `<div class="info-row"><span class="tag danger">${co.name}</span> <span class="value">${co.occupation} &mdash; ${co.leverage}</span></div>`).join('')}
    </div>
    <div class="info-card"><h4>Evidence (${c.evidence.length} items)</h4>
      ${c.evidence.map(e => `<div class="info-row"><span class="tag">${e.id}</span> <span class="tag gold">${e.type}</span> <span class="value">${e.description} <small>(${e.steps} steps)</small></span></div>`).join('')}
    </div>`;
  $('#content-1').innerHTML = html;
  updateProgress(15, 'Crime backstory generated');
  await sleep(600);
}

// Phase 2
async function runPhase2() {
  activateStep(2);
  updateProgress(20, 'Phase 2/6: Building fabricated narrative...');
  await sleep(800);
  const f = currentStory.fabricated;
  let html = `
    <div class="info-card"><h4>Fake Suspect: ${f.fake_suspect.name}</h4>
      <div class="info-row"><span class="label">Occupation:</span> <span class="value">${f.fake_suspect.occupation}</span></div>
      <div class="info-row"><span class="label">Fake Motive:</span> <span class="value">${f.fake_suspect.fake_motive}</span></div>
    </div>
    <div class="info-card"><h4>Cover Story</h4><p>${f.cover_story}</p></div>
    <div class="info-card"><h4>Conspirator Alibis</h4>
      ${Object.entries(f.alibis).map(([n,a]) => `<div class="info-row"><span class="tag danger">${n}</span> <span class="value">"${a}"</span></div>`).join('')}
    </div>`;
  $('#content-2').innerHTML = html;
  updateProgress(30, 'Fabricated narrative built');
  await sleep(600);
}

// Phase 3
async function runPhase3() {
  activateStep(3);
  updateProgress(35, 'Phase 3/6: Running suspense meta-controller...');
  const d = currentStory.detective;
  let headerHtml = `
    <div class="info-card"><h4>${d.name}</h4>
      <div class="info-row"><span class="label">Stakes:</span> <span class="value">${d.personal_stakes}</span></div>
      <div class="info-row"><span class="label">If failure:</span> <span class="value" style="color:var(--accent2)">${d.dire_consequence}</span></div>
      <div class="info-row"><span class="label">Deadline:</span> <span class="value">${d.deadline_reason}</span></div>
    </div><div id="plot-points-container"></div>`;
  $('#content-3').innerHTML = headerHtml;
  await sleep(500);

  const container = $('#plot-points-container');
  const pps = currentStory.plot_points;
  const total = pps.length;
  const totalTime = total + 3;

  for (let i = 0; i < total; i++) {
    const pp = pps[i];
    const pct = 35 + Math.round((i / total) * 35);
    const timeLeft = totalTime - (i + 1);
    updateProgress(pct, `Plot point ${pp.id}/${total} | Time: ${timeLeft}/${totalTime} | Suspense: ${pp.suspense}/10`);

    const cls = pp.collision ? 'collision' : (pp.reveal ? 'progress' : '');
    const suspenseColor = pp.suspense <= 5 ? 'var(--blue)' : pp.suspense <= 7 ? 'var(--gold)' : 'var(--accent2)';

    let ppHtml = `<div class="plot-point ${cls}">
      <div class="pp-header">
        <span class="pp-id">PP-${pp.id} ${pp.collision ? '<span class="tag danger">COLLISION</span>' : ''}</span>
        <span class="pp-suspense">Suspense: ${pp.suspense}/10</span>
      </div>
      <div class="pp-body">${pp.description}</div>
      <div class="suspense-bar"><span>Suspense</span>
        <div class="suspense-track"><div class="suspense-value" style="width:${pp.suspense*10}%;background:${suspenseColor}"></div></div>
      </div>
      ${pp.reveal ? `<div class="pp-reveal">${pp.reveal}</div>` : ''}
    </div>`;
    container.insertAdjacentHTML('beforeend', ppHtml);
    container.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    await sleep(350);
  }
  updateProgress(70, `Investigation complete - ${total} plot points generated`);
  await sleep(400);
}

// Phase 4
async function runPhase4() {
  activateStep(4);
  updateProgress(75, 'Phase 4/6: Running reader simulation...');
  await sleep(800);
  const ev = currentStory.evaluation;
  const readers = [
    { key:'logic_analyst', label:'Logic Analyst', icon:'logical consistency & deduction' },
    { key:'intuitive_reader', label:'Intuitive Reader', icon:'character behavior & immersion' },
    { key:'genre_expert', label:'Genre Expert', icon:'pacing & narrative structure' },
  ];
  let html = '';
  for (const r of readers) {
    const d = ev[r.key];
    const sc = d.score >= 8 ? 'var(--green)' : d.score >= 6 ? 'var(--gold)' : 'var(--accent2)';
    html += `<div class="eval-card"><h4>${r.label}</h4><small style="color:var(--text-dim)">${r.icon}</small>
      <div class="score-row"><span>Overall Score</span> <span class="score-val" style="color:${sc}">${d.score}/10</span></div>
      <div class="score-row"><span>Identified Real Criminal?</span> <span class="score-val" style="color:var(--green)">No (good!)</span></div>
      <div class="score-row"><span>Issues Flagged</span> <span class="score-val">${d.issues}</span></div>
      ${d.pacing ? `<div class="score-row"><span>Pacing</span> <span style="color:var(--text-dim);font-size:.82rem">${d.pacing}</span></div>` : ''}
    </div>`;
  }
  $('#content-4').innerHTML = html;
  updateProgress(85, 'Reader evaluation complete');
  await sleep(600);
}

// Phase 5
async function runPhase5() {
  activateStep(5);
  updateProgress(88, 'Phase 5/6: Refining story...');
  await sleep(700);
  const ref = currentStory.refinement;
  let html = `<div class="info-card"><h4>Refinement Results</h4>
    <div class="info-row"><span class="label">Issues found:</span> <span class="value">${ref.issues_found}</span></div>
    <div class="info-row"><span class="label">Issues fixed:</span> <span class="value">${ref.issues_fixed}</span></div>
  </div><div class="info-card"><h4>Changes Applied</h4>
    ${ref.details.map(d => `<div class="info-row"><span class="tag green">Fixed</span> <span class="value">${d}</span></div>`).join('')}
  </div>`;
  $('#content-5').innerHTML = html;
  updateProgress(92, 'Refinement complete');
  await sleep(500);
}

// Phase 6
async function runPhase6() {
  activateStep(6);
  updateProgress(95, 'Phase 6/6: Assembling final narrative...');
  await sleep(1200);
  const n = currentStory.plot_points.length;
  $('#content-6').innerHTML = `<div class="info-card"><h4>Story assembled successfully</h4><p>${n} plot points woven into a dual-layer narrative with dramatic irony.</p></div>`;
  updateProgress(100, 'Generation complete!');
  await sleep(800);
  $('#step-6').classList.remove('active');
  $('#step-6').classList.add('done');
}

// Final story
function showFinalStory() {
  $('#story-output').classList.remove('hidden');
  const m = currentStory.meta;
  $('#story-meta').innerHTML = `
    <span class="tag">${m.model}</span>
    <span class="tag gold">${m.plot_points} Plot Points</span>
    <span class="tag green">Suspense: ${m.suspense}</span>
    <span class="tag">${m.countdown} Countdown</span>`;

  let html = currentStory.story_text
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^---$/gm, '<hr>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');
  $('#story-body').innerHTML = '<p>' + html + '</p>';
  $('#story-output').scrollIntoView({ behavior: 'smooth' });
}

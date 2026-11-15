from pathlib import Path
import json,csv,html,shutil,zipfile
from datetime import datetime,timedelta,timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
import pymupdf

R=Path(__file__).parent
IST=timezone(timedelta(hours=5,minutes=30))
issues=json.loads(json.loads((R/'jira-final-issues.json').read_text())[0]['text'])['data']['issues']
raw=json.loads((R/'jira-final-history.json').read_text())
hist={r['value']['key']:json.loads(r['value']['response'][0]['text'])['data']['values'] for r in raw if r['status']=='fulfilled'}
def dt(s): return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(IST)
def changes(k): return sorted([(dt(v['created']),x) for v in hist[k] for x in v['items'] if x['field']=='status'],key=lambda a:a[0])
def done_at(k,day):
 a=[x for t,x in changes(k) if t.date().isoformat()<=day]
 return bool(a) and a[-1].get('toString')=='Done'
rows=[]
for i in sorted(issues,key=lambda i:int(i['key'][4:])):
 f=i['fields']; c=changes(i['key']);d=[t.isoformat() for t,x in c if x.get('toString')=='Done'];s=[t.isoformat() for t,x in c if x.get('toString')=='In Progress']
 rows.append(dict(key=i['key'],summary=f['summary'],sprint=1 if int(i['key'][4:])<22 else 2,points=f['customFields']['Story Points']['value'],due=f['duedate'],done=d[-1] if d else '',started=s[0] if s else '',status=f['status']['name']))
with (R/'issue-history-final.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
for sp,start,end,baseline in [(1,'2026-11-02','2026-11-06',24),(2,'2026-11-07','2026-11-13',32),(2,'2026-11-07','2026-11-15',32)]:
 dates=[datetime.fromisoformat(start)+timedelta(days=n) for n in range((datetime.fromisoformat(end)-datetime.fromisoformat(start)).days+1)]
 rem=[baseline-sum(r['points'] for r in rows if r['sprint']==sp and done_at(r['key'],d.date().isoformat())) for d in dates]
 fig,ax=plt.subplots(figsize=(9,4.6));ax.plot(dates,rem,'o-',color='#087e8b',label='Recorded remaining points')
 if end.endswith('15'): ax.axvline(datetime(2026,11,13),color='#b5651d',linestyle='--',label='Original deadline')
 else: ax.plot(dates,[baseline*(1-n/(len(dates)-1)) for n in range(len(dates))],'--',color='#b5651d',label='Illustrative linear reference')
 ax.set(title=f'Sprint {sp}: '+('late closeout' if end.endswith('15') else 'original reporting window'),ylabel='Story points remaining',ylim=(0,baseline+2));ax.legend();ax.grid(alpha=.18);fig.autofmt_xdate();fig.tight_layout()
 fig.savefig(R/(f'sprint-{sp}-burndown'+('-closeout' if end.endswith('15') else '')+'.png'),dpi=170);plt.close(fig)
deadline=[sum(r['points'] for r in rows if r['sprint']==s and done_at(r['key'],e)) for s,e in [(1,'2026-11-06'),(2,'2026-11-13')]]
close=[sum(r['points'] for r in rows if r['sprint']==s and r['status']=='Done') for s in [1,2]]
assert deadline==[24,16],deadline
assert close==[24,26],close
fig,ax=plt.subplots(figsize=(9,4.7))
for off,vals,label,col in [(-.25,[24,32],'Committed','#aab9c4'),(0,deadline,'Done by planned deadline','#087e8b'),(.25,close,'Done at final closeout','#203c58')]:
 b=ax.bar([off,1+off],vals,width=.24,label=label,color=col);ax.bar_label(b,padding=3)
ax.set(xticks=[0,1],xticklabels=['Sprint 1','Sprint 2'],ylabel='Story points',ylim=(0,40),title='Velocity: deadline performance and late closeout');ax.legend(fontsize=9);fig.tight_layout();fig.savefig(R/'velocity.png',dpi=170);plt.close(fig)
fig,ax=plt.subplots(figsize=(12,12))
for y,r in enumerate(rows):
 ax.scatter(datetime.fromisoformat(r['due']),y,marker='|',s=160,color='#b5651d',label='Planned due date' if y==0 else None)
 if r['done']:
  end=dt(r['done']).replace(tzinfo=None);start=dt(r['started']).replace(tzinfo=None) if r['started'] else end
  ax.plot([start,end],[y,y],color='#087e8b',lw=3);ax.scatter(end,y,color='#087e8b',s=20)
ax.set(yticks=range(len(rows)),yticklabels=[r['key']+' '+r['summary'][:44] for r in rows],title='Planned and observed timeline through 15 November',xlabel='IST dates | tick = due | dot = latest Done | bar = recorded In Progress to Done');ax.invert_yaxis();ax.grid(axis='x',alpha=.18);ax.legend();fig.autofmt_xdate();fig.tight_layout();fig.savefig(R/'planned-actual-gantt.png',dpi=160);plt.close(fig)
(R/'CHART-NOTES.md').write_text('''# Final chart provenance
Sources: jira-final-issues.json and jira-final-history.json, captured 15 November 2026 after PR38 merge and sprint closure. Original pre-closeout snapshots retained separately.
All dates normalized to Asia/Kolkata (UTC+05:30); status events sorted chronologically. Daily burndown uses end-of-day status, not commit date. Estimates use recorded issue points; no estimate-change reconstruction is claimed.
Sprint1 committed 24, deadline Done24, closeout Done24. Nine pre-start setup points excluded. Sprint2 committed32, deadline Done16, final closeout Done26, presentation carryover6.
Sprint1 planned2-6Nov; actually closed5Nov. Sprint2 planned9-13Nov; actually started7Nov and closed15Nov10:30:16UTC. No dates changed to hide delay.
Velocity here is a history-derived report; Jira native reports may use actual close time and show26 rather than16 for Sprint2. These are different cutoffs, not conflicting completion claims.
Gantt is a planned/observed timeline: due-date ticks, first recorded In Progress to latest Done bars; missing starts show dots. It does not measure coding effort. IWM17 was reopened and reclosed8Nov; its latestDone dot differs from its Done status at the Sprint1 deadline.
Burndown linear reference is illustrative. Batch Jira updates are not evidence of equal daily coding. Four presentation issues remain incomplete in backlog, preserving historical sprint membership.
''',encoding='utf-8')

W,H=960,600
NAVY='#18334b';TEAL='#087e8b';INK='#243745';MUTED='#526775'
class Book:
 def __init__(self,name,title):
  self.path=R/name;self.c=canvas.Canvas(str(self.path),pagesize=(W,H));self.c.setTitle(title);self.c.setAuthor('Prepared for S Anuj Srijan with AI assistance');self.n=0
 def page(self,kicker,title):
  if self.n:self.c.showPage()
  self.n+=1;c=self.c;c.setFillColor(HexColor('#f7f9fb'));c.rect(0,0,W,H,fill=1,stroke=0)
  c.setFillColor(HexColor(TEAL));c.rect(40,H-47,38,5,fill=1,stroke=0)
  self.text(kicker.upper(),90,H-48,830,10,TEAL);self.text(title,40,H-95,880,25,NAVY)
  c.setStrokeColor(HexColor('#d8e2e8'));c.line(40,35,W-40,35)
  self.text('INSURANCE WORKFLOW  |  TEAM 07  |  15 NOV 2026',40,20,800,8,MUTED);self.text(str(self.n),900,20,30,8,MUTED)
 def text(self,s,x,y,w=870,size=13,col=INK):
  p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=size*1.37,textColor=HexColor(col)))
  _,h=p.wrap(w,1000);p.drawOn(self.c,x,y-h+size);return y-h-10
 def bullets(self,items,x=45,y=460,w=870,size=15):
  for s in items:y=self.text('• '+s,x,y,w,size)
  return y
 def note(self,s):
  self.c.setFillColor(HexColor('#e2eff1'));self.c.roundRect(40,52,880,65,8,fill=1,stroke=0)
  self.text('<b>Say:</b> '+s,55,96,850,12)
 def pic(self,name,x,y,w,h):
  im=ImageReader(str(R/name));iw,ih=im.getSize();scale=min(w/iw,h/ih);self.c.drawImage(im,x+(w-iw*scale)/2,y+(h-ih*scale)/2,iw*scale,ih*scale,mask='auto')
 def save(self):self.c.save()

b=Book('Presentation-and-Speaking-Guide.pdf','Insurance Workflow - presentation and speaking guide')
b.page('Final demonstration','Insurance Workflow Management')
b.text('A six-page frontend demonstration developed through reviewed pull requests and two Jira sprints.',45,450,850,23)
b.bullets(['Anuj Srijan • Renetta Isabel Nathan • Aswin Adithya • Raghav Hariharan','HTML, CSS and vanilla JavaScript; Vite handles development and build.','Final application commit: eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b','Development sprint closed 15 November. Team presentation still to be delivered.'],y=350,size=15)
b.note('We built and tested a frontend demonstration. Our evidence shows both the delivered UI and the actual development process, including late completion.')
b.page('01 / purpose and scope','Explain what the product actually does')
b.bullets(['Applicant journey: landing → demo login → dashboard → application form → sample application list.','Staff journey: inspect fictional records and change a selected card to Approved (Demo) or Rejected (Demo).','Login does not authenticate. Form submission is cancelled and displays a no-save message.','Sample records are fixed. Staff changes stay only in the current page and reset on refresh.','No API, database, document upload, claim engine, notification service or real insurer processing.'],size=16)
b.note('The original proposal described a larger backend system. We intentionally narrowed this release to frontend learning; the final baseline documents that deviation.')
b.page('02 / architecture','A small architecture you can explain')
b.bullets(['Browser: six HTML entry pages share css/style.css and js/main.js.','js/main.js attaches handlers from js/demo-forms.js. Handlers update DOM text; they do not call an application server.','Vite: runs the local dev server and bundles all six entry points into dist/.','Node test runner + jsdom: assert links, field validation, notices, independent review actions and reset behavior.','GitHub Actions: npm ci → test:coverage → build → verify six output HTML files.'],size=16)
b.note('Node is tooling here. It is not our insurance backend. Plain HTML and small DOM handlers are sufficient for this agreed scope.')
b.page('03 / preparation','Before the evaluator arrives')
b.bullets(['Use a clean clone of main. Install Node 22.12 or newer, then run npm ci, npm run test:coverage and npm run build.','Run npm run dev and open the localhost address printed by Vite. Open all six routes once.','Keep Jira board 36, PR #38, GitHub Actions and this PDF ready in separate tabs.','Use fictional input only: Demo Applicant, demo@example.com, Health, 1000.','Download the ZIP locally. Keep screenshots and MP4s as fallback evidence; they are screenshot walkthroughs, not live demonstrations.'],size=15)
b.note('I will first demonstrate the current working site, then show the traceable issues, review approval and test evidence behind it.')
b.page('04 / timed live demo','A two-minute route-by-route demonstration')
b.bullets(['0:00-0:15 | Anuj: state frontend-only scope and show landing navigation.','0:15-0:35 | Renetta: show login notice and dashboard links. No authentication occurs.','0:35-0:55 | Renetta: leave required fields blank, then enter valid fictional values and show the no-save confirmation.','0:55-1:10 | Renetta: open applications list; explain these are static samples, not submitted values.','1:10-1:40 | Aswin: approve first staff card, reject second, show isolation, refresh and show reset.','1:40-2:00 | Anuj/Raghav: point to passing CI and explain the final scope and test limits.'],size=14)
b.note('Rehearse these handoffs. The names describe the proposed speaking allocation; they do not claim anyone has already presented.')
b.page('05 / staff behavior','Show the action, then prove its limit')
b.pic('staff-actions.png',45,125,590,350)
b.bullets(['Approve affects one card.','Reject affects another card.','Status feedback uses aria-live.','Refresh restores fixtures.','Applicant list does not synchronize.','View details remains disabled.'],x=660,y=440,w=250,size=13)
b.note('This is an interface simulation of review, not an insurance decision. There is no persisted application state.')
b.page('06 / sprint process','Show evidence, not just a green board')
b.bullets(['Sprint1 planned2-6Nov: foundation, collaboration setup, applicant screens. Started2Nov and closed5Nov.','Sprint2 planned9-13Nov: application list, staff page, approved optional behavior, integration and demonstration. Actually started7Nov; closed15Nov.','Workflow: Jira item → branch → focused commit → PR → independent review → passing CI → merge → evidence-based Jira transition.','PR36 and37: Raghav interaction/manual-check work. PR38: Anuj integration fixes, approved by Renetta at the same head commit before merge.','Story points are relative estimates of scope/complexity. They are not hours or a measure of individual productivity.'],size=14)
b.note('Takeover work keeps the original assignment in history, but actual Git authorship stays with the person who did the work.')
for s in [1,2]:
 b.page('07 / burndown' if s==1 else '08 / burndown',f'Sprint {s}: remaining work across the original window')
 b.pic(f'sprint-{s}-burndown.png',100,135,760,345)
 b.note('The vertical axis is remaining story points; the horizontal axis is date. Drops are recorded Jira completions. '+('24 points were Done by the planned deadline.' if s==1 else '16 of 32 points were Done by13Nov; later merges must not erase this delay.'))
b.page('09 / velocity','Separate deadline delivery from late closeout')
b.pic('velocity.png',100,135,760,345)
b.note('Sprint1:24 committed and24 completed. Sprint2:32 committed,16 completed by13Nov,26 at15Nov closeout. Six presentation points remain. Native Jira may show26 using actual sprint closure.')
b.page('10 / timeline','How to explain the Gantt-style timeline')
b.pic('planned-actual-gantt.png',40,120,520,370)
b.bullets(['Amber tick: planned due date.','Teal dot: latest recorded Done.','Teal bar: recorded In Progress to Done.','Missing start means no reliable duration.','This measures recorded workflow timing, not hours spent coding.','Open the full-resolution PNG to inspect every row.'],x=590,y=450,w=325,size=14)
b.note('IWM17 was reopened and reclosed after Sprint1; the latest completion dot differs from its earlier Done status at the deadline. History is preserved.')
b.page('11 / validation','What the test evidence proves')
b.bullets(['Final merged main: 10/10 automated tests passed; six-page production build passed; post-merge GitHub CI passed.','demo-forms.js coverage: 100% lines, 100% functions, 87.5% branches. This is one selected module, not whole-system coverage.','Browser evidence: all six routes rendered; keyboard Enter approved a card; reject changed another card independently; refresh restored fixtures; captured console errors empty.','Raghav manual report is historical and predates the final integration fixes; retain its original date/scope.','No claim of penetration testing, full accessibility certification, backend test success or performance SLA verification.'],size=15)
b.note('Passing tests are scoped evidence. We also disclose what was not tested and what the product does not implement.')
b.page('12 / deliverables','What to open during the viva')
b.bullets(['Presentation-and-Speaking-Guide.pdf: this narrative and rehearsal guide.','Final-SRS-SAD-Test-Plan.pdf: revised frontend requirements, diagrams, design decisions, traceability, test cases and deviations.','index.html: local evidence hub with burndown, velocity and planned/actual charts.','issue-history-final.csv + Jira JSON snapshots: chart provenance and actual issue states.','Screenshots, unit/coverage/build evidence, original planning reference and both screenshot-walkthrough MP4s.','Repository PR39 will publish this evidence package after independent review. Final presentation tasks stay open until actually delivered.'],size=14)
b.note('Use the PDF to tell the story and the repository/Jira links to prove it. A prepared script is not evidence that a presentation happened.')
b.page('13 / viva questions','Short answers to likely questions')
b.bullets(['Why no backend? The agreed implementation plan reduced scope to a six-page frontend. The baseline records deferred original features.','Why did Sprint2 miss its deadline? At13Nov only16/32 points were recorded Done. Integration closed late; avoid guessing causes not recorded in issues.','Why 87.5% branches? Some defensive handler paths are not covered;100% line coverage does not prove every branch.','Why do approvals disappear? State is only in the DOM. Refresh reloads the fixed HTML fixtures.','Who wrote what? Show specific PR commits and reviews. Explain AI assistance and takeover work honestly.','What comes next? Present the demo, finish submission approvals and only then plan real authentication, APIs and persistence as a separate scope.'],size=14)
b.note('If you do not know an answer, open the relevant code or test and explain what it actually does. Do not claim a backend feature based on a UI label.')
b.page('14 / closing checklist','What each teammate must do next')
b.bullets(['Anuj: lead scope/process/charts, show merge evidence and coordinate final submission.','Renetta: rehearse applicant pages and no-save form behavior; explain only actual contributions and reviews.','Aswin: rehearse staff controls, independent status changes and refresh reset.','Raghav: explain actual tests, coverage boundaries, manual results and setup commands.','One teammate must review the documentation publication PR before it can merge.','Deliver the live presentation; record it if your assessor requires live video. Confirm participation afterwards so IWM36-39 can be completed.'],size=15)
b.note('Our development release is frozen at eb232fb. Presentation is the remaining human activity; no completion or attendance is fabricated.')
b.save()

t=Book('Final-SRS-SAD-Test-Plan.pdf','Insurance Workflow - final frontend SRS SAD and test plan')
t.page('Controlled baseline / version 2.0','Final frontend specification and test baseline')
t.bullets(['Prepared15Nov2026 for Team07 and Anuj; implementation baseline eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b.','Three specifications in one book: SRS (pages2-4), SAD (pages5-8), STP (pages9-12), deviation/submission record (page13).','This version supersedes implementation expectations in the October v1.1 proposal for this frontend release only. The original documents remain historical references.','Structured to the supplied academic SRS/SAD/STP checklist; no formal IEEE certification or evaluator acceptance is claimed.','Prepared with AI assistance. Documentation peer review and evaluator acceptance remain pending; software PR38 approval does not approve this new document.'],size=15)
t.page('SRS / 1. introduction and 2. overall description','Purpose, actors and scope')
t.bullets(['Purpose: demonstrate applicant navigation, client-side form feedback and staff review UI in a reproducible academic website.','Actors: demo applicant, demo staff reviewer, development team/evaluator. These are demonstration roles, not authenticated security roles.','Environment: modern browser; Node22.12+ and npm for tooling; Vite8.3.5; static built assets.','Constraints: six HTML pages, plain CSS/JS, fictional data, no application backend or persistent data store.','User expectations: labels explicitly state demo behavior. Staff state is page-local and the applications list is fixed.','Acceptance boundary: this release does not satisfy the original full insurance automation SRS. Deferred requirements are recorded in the deviation register.'],size=15)
t.page('SRS / 3. specific requirements','Measurable frontend requirements')
t.bullets(['FR01 Navigation: all internal links on six pages resolve to existing pages or anchors. Evidence FE01.','FR02 Login: submit is cancelled, no sign-in occurs and entered credentials are not echoed in feedback. FE06.','FR03 Application: four labelled required fields; valid email; positive whole-number requested amount. FE02-04.','FR04 Confirmation: valid form shows no-save notice; editing clears stale feedback; fresh page clears result. FE05,07,10.','FR05 Tracking: applications list contains clearly labelled synthetic examples. Verify through page review and screenshot.','FR06 Staff: approve/reject affects only selected card, feedback announced, refresh restores fixtures; details disabled. FE09.','NFR01 Reproducibility: npm ci, tests and build succeed; dist has six entry pages. CI/build. NFR02 Usability: labels, skip targets and live regions present; keyboard behavior checked, full accessibility audit not claimed. FE01,02,09,10 + browser evidence.'],size=13)
t.page('SRS / 4. security and use cases','Security boundaries and use-case view')
t.bullets(['Objective SO01: avoid accidental exposure or persistence of demo credentials/input. Objective SO02: prevent users mistaking simulated actions for real processing.','SR01: form handlers prevent default submission, do not echo credentials, and do not write localStorage. FE05/06/10 and code inspection.','SR02: feedback states no sign-in/no-save; staff actions use fixed text and per-card DOM scope; no backend permissions are claimed. FE06/09.'],y=465,size=13)
c=t.c;c.setStrokeColor(HexColor(TEAL));c.roundRect(260,135,450,200,8,stroke=1,fill=0)
t.text('Frontend demo system',385,315,280,12,TEAL)
for label,x,y in [('Applicant',95,245),('Staff',790,245)]:
 c.circle(x+30,y+12,9);c.line(x+30,y+3,x+30,y-30);c.line(x+10,y-10,x+50,y-10);c.line(x+30,y-30,x+12,y-48);c.line(x+30,y-30,x+48,y-48);t.text(label,x-5,y-65,100,11)
for txt,yy in [('Navigate / demo sign-in',280),('Enter form / view samples',230),('Simulate review / reset',180)]:
 c.ellipse(325,yy-19,650,yy+18);t.text(txt,360,yy+3,260,11)
c.line(150,235,325,280);c.line(150,235,325,230);c.line(790,235,650,180)
t.page('SAD / 1-2. introduction and overview','Architecture, components and rationale')
t.bullets(['Pattern: static multi-page frontend with a small shared DOM behavior module. Six entry points preserve simple page ownership.','C01 Pages: index/login/dashboard/application/applications/staff HTML. C02 Presentation: css/style.css.','C03 Bootstrap: js/main.js. C04 Behavior: js/demo-forms.js. C05 Tooling: Vite, Node test runner and jsdom.','Runtime data: constants in HTML plus current DOM text only. No datastore, API service, email adapter or worker.','Tradeoff: easy local build and review; deliberate limitations include no persistence, no shared state and no authorization.','Trust boundary: this is an untrusted demo browser. It cannot enforce access to sensitive insurance data.'],size=14)
t.page('SAD / 3. architecture','Component view and traceability')
for x,txt in [(65,'C01 HTML pages'),(355,'C03 main.js'),(645,'C04 demo-forms.js')]:
 t.c.setFillColor(HexColor('#e2eff1'));t.c.roundRect(x,355,245,70,7,fill=1,stroke=0);t.text('&lt;&lt;component&gt;&gt;<br/>'+txt,x+15,400,215,14)
for x in [310,600]:t.c.setStrokeColor(HexColor(TEAL));t.c.line(x,390,x+45,390);t.c.line(x+45,390,x+37,395);t.c.line(x+45,390,x+37,385)
t.bullets(['C02 styles all pages; C04 attaches events and updates page DOM. C05 builds assets and executes tests outside runtime.','FR01 → C01 → FE01. FR02 → C01/C04 → FE06. FR03 → C01 → FE02-04.','FR04 → C04 → FE05/07/10. FR05 → C01 → browser/screenshot. FR06 → C01/C04 → FE09.','NFR01 → C05 → CI/build. NFR02 → C01/C04 → labels, links, live regions and keyboard evidence.','Security architecture: no server boundary exists; do not treat demo login or hidden/disabled UI as authorization.'],y=305,size=14)
def sequence(book,title,actors,msgs):
 book.page('SAD / 4. detailed design',title);c=book.c;xs=[110,370,650,850][:len(actors)]
 for x,label in zip(xs,actors):
  book.text(label,x-70,455,150,12,TEAL);c.setStrokeColor(HexColor('#aab9c4'));c.setDash(3,3);c.line(x,425,x,135);c.setDash()
 for n,(src,dst,label) in enumerate(msgs):
  y=405-n*49;a,z=xs[src],xs[dst];c.setStrokeColor(HexColor(NAVY));c.line(a,y,z,y);sign=1 if z>a else -1;c.line(z,y,z-7*sign,y+4);c.line(z,y,z-7*sign,y-4);book.text(label,min(a,z)+12,y+20,abs(z-a)-20,10)
sequence(t,'Sequence 1: applicant form feedback',['Applicant','Browser form','Demo handler'],[(0,1,'Enter fictional values and submit'),(1,0,'Invalid: browser validation feedback'),(1,2,'Valid: submit event'),(2,1,'preventDefault + fixed no-save notice'),(1,0,'Show polite live-region feedback')])
t.note('Native validation normally gates user submission. Directly dispatching submit in a unit test bypasses that gate; it tests handler behavior separately.')
sequence(t,'Sequence 2: staff review simulation',['Staff','Selected card','Demo handler'],[(0,1,'Click Approve or Reject'),(1,2,'Click event with card-scoped handler'),(2,1,'Set status text + no-save announcement'),(1,0,'Visible selected-card result'),(0,1,'Refresh: reload original HTML fixtures')])
t.note('Interface contract: attachDemoForms(root: Document) returns no value and attaches DOM listeners. No REST API exists; disabled details has no endpoint. Missing staff controls are skipped.')
t.page('STP / 1-2. introduction and test items','Test scope and execution environment')
t.bullets(['Plan ID FE-STP-2.0. Purpose: verify frontend requirements against frozen implementation eb232fb.','Items: six source pages, shared CSS, js/main.js, js/demo-forms.js, tests/frontend.test.js and Vite build configuration.','Environment: GitHub Actions ubuntu-latest/Node22 plus local Windows/Chrome checks. jsdom tests do not replace a real browser.','Entry criteria: reviewed code, lockfile, fictional fixtures, Node22.12+ and available npm dependencies.','Exit criteria:10 automated tests pass, six output pages build, known limitations documented, PR review complete. Live presentation is a separate pending activity.','Regression rule: rerun tests/build after source changes; rerun affected browser checks. Original backend TC001-037 remain deferred/not executed for this release.'],size=15)
t.page('STP / 3-5. approach, resources and validation','Execution strategy and security validation')
t.bullets(['3. Approach: automated DOM/unit tests for deterministic behaviors; manual real-browser navigation, action/reset and console checks; CI production-build verification.','4. Resources: Anuj integrates evidence; contributor reports retain their actual author/date. GitHub stores commits/reviews/checks; Jira stores planning/status history. No invented tester sign-off.','5. Validation: compare expected UI output to assertions/screenshots, record exact commit and command, preserve failed or historical reports.','5.1 Security validation: FE05/06/10 check cancelled submission, no credential echo and empty localStorage; FE09 checks isolated fixed-text status changes. Code inspection shows no insurance API call.','These checks do not validate TLS, authentication, authorization, encryption, audit immutability, upload scanning or production privacy. Such original requirements are unimplemented.'],size=14)
t.page('STP / 6. cases and requirement traceability','Ten executed frontend tests')
cases=[('FE01','FR01/NFR02','Inspect all six pages; internal page/anchor targets exist.'),('FE02','FR03/NFR02','Four application controls labelled/required; blank form invalid.'),('FE03','FR03','Bad email invalid; demo@example.com accepted.'),('FE04','FR03','0, -1,1.5 invalid amounts;1000 valid.'),('FE05','FR04/SR01','Valid fictional form: cancelled submit, no-save notice, no storage/navigation.'),('FE06','FR02/SR01-02','Login: cancelled submit, no authentication/credential echo/storage.'),('FE07','FR04','Input event clears old result message.'),('FE08','NFR01','Shared handler tolerates pages without forms.'),('FE09','FR06/NFR02','Enable attached controls; independent approve/reject; live feedback; refresh reset.'),('FE10','FR04/NFR02','Applicant live region has confirmation; fresh page has empty result/storage.')]
t.bullets([f'<b>{a} / {r}</b> - {d} <b>PASS</b>' for a,r,d in cases],y=470,size=12)
t.page('STP / 7. results and limitations','Final evidence and residual risks')
t.bullets(['Local merged-main run15Nov:10 tests passed,0 failed/skipped; build emitted index, login, dashboard, application, applications and staff HTML.','Selected-module coverage js/demo-forms.js:100% line,100% function,87.5% branch. Uncovered defensive paths remain; do not claim whole-product coverage.','Post-merge GitHub Frontend build check: completed/success. CI includes clean npm ci, tests/coverage, build and output-page checks.','Real Chrome evidence captured on same application content before merge: six routes render, Enter approves first card, reject changes second, refresh resets, captured errors empty.','Manual report IWM35 is historical and predates final integration. Full screen-reader audit, exhaustive responsive matrix, performance/security testing and live team demonstration are not evidenced.'],size=14)
t.page('Change record / original proposal to release','Deviation register and submission readiness')
t.bullets(['Original INS-F001-018: real identity, application/claim workflows, documents, assignment, decisions, notifications, audit, search and concurrency were proposed. They are NOT delivered as backend features. FR01-06 define the narrower demonstrated UI.','Original INS-NF001-006: service performance, availability, recovery and audit retention are not measured/implemented. Usability/reproducibility are partially addressed by frontend evidence only.','Original INS-SR001-007: production transport, access, session, input, storage, audit and throttling controls remain deferred. Browser no-save behavior does not satisfy those controls.','Final artifacts: this revised baseline + presentation PDF, raw Jira exports, charts, source and reviewed PRs, test/build evidence and labelled screenshot videos.','Submission gaps: publication PR review/merge; actual team presentation; verify linked GitHub Project requirement and evaluator acceptance of scope/video format. No automatic checklist approval is claimed.'],size=13)
t.save()
(R/'DELIVERY-STATUS.md').write_text('''# Final delivery status - 15 November 2026
PR38 merged after Renetta approval; merge eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b. PR36 and37 already merged. Local main10/10 tests and six-page build passed; main CI success.
Both Jira sprints closed. Sprint2 closed15Nov10:30:16UTC.26/32 points Done at closeout; four presentation tasks IWM36-39 (6points) carried to backlog. User confirmed nobody presented yet.
Original-deadline delivery: Sprint1 24/24; Sprint2 16/32. Late work is separately reported; no backdating.
Presentation-and-Speaking-Guide.pdf is ready for rehearsal. Final-SRS-SAD-Test-Plan.pdf reconciles the frontend release with the original backend proposal. Original October DOCX files are historical, not claims of delivered backend behavior.
Software baseline frozen at eb232fb. Package publication requires a new documentation PR and independent review. No claim of formal IEEE certification, evaluator scope acceptance or teammate presentation.
Videos are screenshot walkthroughs, not narrated live recordings. Verify assessor acceptance; perform/record a real demo if required. Linked GitHub Project compliance remains to verify.
''',encoding='utf-8')
(R/'MERGE-AND-TEST-EVIDENCE.md').write_text('''# Final application merge and verification
PR: https://github.com/insurance-workflow-automation/se_mini_project/pull/38
Reviewer: Renetta-Nathan, APPROVED15Nov2026 at10:21:04UTC, commit f2e03dabc1e0b12f726e59a71097c9bf030d85f9.
Merge commit: eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b.
Verified current main after fast-forward: npm run test:coverage10/10 pass,0 fail; npm run build pass, six HTML pages. Main GitHub Frontend build completed success; workflow runs npm ci, coverage, build and six-entry check.
Coverage filter is js/demo-forms.js:100% line/function,87.5% branch. Raw prior same-content run remains in final-tests-coverage.txt; this record separately documents post-merge rerun.
''',encoding='utf-8')
files=sorted(p.name for p in R.iterdir() if p.is_file() and p.name!='index.html')
(R/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Final Insurance Workflow delivery</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;color:#18334b}img{max-width:100%}a{color:#087e8b}</style><h1>Final Insurance Workflow delivery</h1><p>PR38 merged. Both sprints closed. Presentation tasks remain in backlog.</p><p>Deadline points:24/24 and16/32. Sprint2 final closeout:26/32.</p><p><a href="Presentation-and-Speaking-Guide.pdf">Presentation guide</a> | <a href="Final-SRS-SAD-Test-Plan.pdf">Final specification and test plan</a></p>'+''.join('<h2>'+html.escape(n)+'</h2><img src="'+n+'">' for n in ['sprint-1-burndown.png','sprint-2-burndown.png','sprint-2-burndown-closeout.png','velocity.png','planned-actual-gantt.png'])+'<h2>Deliverables and evidence</h2><ul>'+''.join('<li><a href="'+html.escape(n)+'">'+html.escape(n)+'</a></li>' for n in files)+'</ul>',encoding='utf-8')
qa=R.parent/'pdf-qa';qa.mkdir(exist_ok=True)
for file in ['Presentation-and-Speaking-Guide.pdf','Final-SRS-SAD-Test-Plan.pdf']:
 doc=pymupdf.open(R/file)
 for j,page in enumerate(doc):
  page.get_pixmap(matrix=pymupdf.Matrix(.8,.8)).save(qa/f'{file[:4]}-{j+1:02}.png')
 print(file,len(doc),'pages')
print('Deadline',deadline,'closeout',close)

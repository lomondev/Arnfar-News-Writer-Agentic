# Original flat illustrations, one per event, 1080x1920, no text (subtitles carry the words).
from playwright.sync_api import sync_playwright
BG={'r':'radial-gradient(circle at 50% 38%,#3a1022 0%,#12060c 55%,#06040a 100%)',
    'b':'radial-gradient(circle at 50% 38%,#0f2a4a 0%,#07101d 55%,#04070d 100%)',
    'g':'radial-gradient(circle at 50% 38%,#0e3a2c 0%,#06140f 55%,#04080a 100%)',
    'y':'radial-gradient(circle at 50% 38%,#3a2a08 0%,#140e04 55%,#08060a 100%)'}
PHONE='<rect x="-150" y="-280" width="300" height="560" rx="44" fill="#1d1b24" stroke="#4a4552" stroke-width="10"/><rect x="-128" y="-240" width="256" height="470" rx="18" fill="{scr}"/>'
def phone(x,y,s=1,scr="#0f1a2b",inner=""): return f'<g transform="translate({x},{y}) scale({s})">'+PHONE.format(scr=scr)+inner+'</g>'
def kip(x,y,r=0,s=1,c="#2ee59d"): return f'<g transform="translate({x},{y}) rotate({r}) scale({s})"><rect x="-90" y="-45" width="180" height="90" rx="10" fill="{c}" stroke="#0b3d2c" stroke-width="5"/><circle cx="0" cy="0" r="26" fill="none" stroke="#0b3d2c" stroke-width="6"/><rect x="-75" y="-32" width="30" height="64" rx="6" fill="#0b3d2c" opacity=".35"/><rect x="45" y="-32" width="30" height="64" rx="6" fill="#0b3d2c" opacity=".35"/></g>'
S={}
# 1 hacker at laptop
S['i-hacker']=('r','''<circle cx="540" cy="560" r="330" fill="#ff3b55" opacity=".10"/>
<path d="M540 300 C420 300 360 390 360 500 L360 640 C360 700 400 760 450 780 L630 780 C680 760 720 700 720 640 L720 500 C720 390 660 300 540 300Z" fill="#0b0910"/>
<path d="M540 330 C445 330 395 410 395 505 L395 640 L685 640 L685 505 C685 410 635 330 540 330Z" fill="#17131f"/>
<ellipse cx="540" cy="560" rx="105" ry="125" fill="#050407"/>
<circle cx="500" cy="560" r="12" fill="#ff3b55"/><circle cx="580" cy="560" r="12" fill="#ff3b55"/>
<path d="M300 820 L780 820 L840 1040 L240 1040Z" fill="#26222f"/><rect x="330" y="640" width="420" height="190" rx="14" fill="#1f1b28" stroke="#3b3546" stroke-width="8"/>
<rect x="350" y="660" width="380" height="150" rx="6" fill="#120a10"/>
<g fill="#ff3b55" opacity=".9"><rect x="370" y="680" width="160" height="12" rx="6"/><rect x="370" y="706" width="240" height="12" rx="6"/><rect x="370" y="732" width="120" height="12" rx="6"/><rect x="370" y="758" width="210" height="12" rx="6"/><rect x="370" y="784" width="90" height="12" rx="6"/></g>
<circle cx="540" cy="730" r="300" fill="url(#gl)" opacity=".0"/>''')
# 2 phishing hook through chat bubble on phone
S['i-hook']=('b',phone(540,760,1.25,"#0f1a2b",'<rect x="-100" y="-150" width="200" height="90" rx="26" fill="#2a2833"/><rect x="-100" y="-30" width="170" height="70" rx="22" fill="#2f6fe0"/><rect x="-80" y="-8" width="120" height="14" rx="7" fill="#cfe3ff"/>')+'''
<line x1="540" y1="0" x2="540" y2="690" stroke="#c9d3e0" stroke-width="6"/>
<path d="M540 690 L540 770 C540 840 640 840 640 770 L640 745" fill="none" stroke="#e8edf5" stroke-width="16" stroke-linecap="round"/>
<path d="M640 720 L660 760 L620 755Z" fill="#e8edf5"/>
<circle cx="540" cy="690" r="14" fill="#ff3b55"/>''')
# 3 money draining out of phone + clock
S['i-drain']=('r',phone(420,820,1.1,"#140a10",'<rect x="-90" y="-60" width="180" height="120" rx="16" fill="#2a1520" stroke="#ff3b55" stroke-width="6"/><path d="M-30 -20 L30 20 M30 -20 L-30 20" stroke="#ff3b55" stroke-width="12" stroke-linecap="round"/>')+
  kip(640,560,-18,1)+kip(760,420,12,.9)+kip(860,290,-8,.75)+kip(700,700,24,.8)+'''
<g transform="translate(800,1180)"><circle r="150" fill="#1d1b24" stroke="#ffc845" stroke-width="14"/><line x1="0" y1="0" x2="0" y2="-100" stroke="#ffc845" stroke-width="14" stroke-linecap="round"/><line x1="0" y1="0" x2="70" y2="40" stroke="#ff3b55" stroke-width="12" stroke-linecap="round"/><circle r="16" fill="#ffc845"/></g>''')
# 4 mask over chat bubble (impersonation)
S['i-mask']=('r','''<path d="M260 420 h560 a60 60 0 0 1 60 60 v300 a60 60 0 0 1 -60 60 h-360 l-120 110 v-110 h-80 a60 60 0 0 1 -60 -60 v-300 a60 60 0 0 1 60 -60z" fill="#2a2833"/>
<g transform="translate(540,640)"><path d="M-260 -110 C-150 -170 150 -170 260 -110 C270 30 200 160 0 190 C-200 160 -270 30 -260 -110Z" fill="#f3eef8"/>
<ellipse cx="-110" cy="-20" rx="70" ry="44" fill="#12060c"/><ellipse cx="110" cy="-20" rx="70" ry="44" fill="#12060c"/>
<path d="M-80 90 Q0 140 80 90" fill="none" stroke="#12060c" stroke-width="16" stroke-linecap="round"/>
<path d="M-260 -110 L-330 -150 M260 -110 L330 -150" stroke="#ff3b55" stroke-width="12"/></g>''')
# 5 gift cards
S['i-gift']=('y',''.join(f'<g transform="translate({540+dx},{700+dy}) rotate({r})"><rect x="-230" y="-140" width="460" height="280" rx="30" fill="{c}"/><rect x="-190" y="40" width="250" height="40" rx="12" fill="#ffffff" opacity=".55"/><circle cx="150" cy="-70" r="40" fill="#ffffff" opacity=".35"/><path d="M-230 -40 h460" stroke="#ffffff" stroke-width="14" opacity=".25"/></g>' for dx,dy,r,c in [(-60,140,-12,"#8b5cf6"),(40,40,6,"#f59e0b"),(-10,-80,-4,"#ef4444")])+
  '<g transform="translate(760,1120)"><rect x="-150" y="-60" width="300" height="120" rx="20" fill="#1d1b24" stroke="#ffc845" stroke-width="8"/><g fill="#ffc845"><circle cx="-90" cy="0" r="14"/><circle cx="-45" cy="0" r="14"/><circle cx="0" cy="0" r="14"/><circle cx="45" cy="0" r="14"/><circle cx="90" cy="0" r="14"/></g></g>')
# 6 fake bank: bank facade + warning
S['i-bank']=('b','''<g transform="translate(540,720)"><path d="M-330 -130 L0 -300 L330 -130Z" fill="#cbd5e1"/><rect x="-330" y="-130" width="660" height="40" fill="#94a3b8"/>
<g fill="#e2e8f0"><rect x="-290" y="-80" width="60" height="330"/><rect x="-150" y="-80" width="60" height="330"/><rect x="90" y="-80" width="60" height="330"/><rect x="230" y="-80" width="60" height="330"/></g>
<rect x="-360" y="250" width="720" height="50" fill="#94a3b8"/></g>
<g transform="translate(760,1120)"><path d="M0 -170 L170 130 L-170 130Z" fill="#ffc845" stroke="#12060c" stroke-width="10" stroke-linejoin="round"/><rect x="-14" y="-70" width="28" height="120" rx="12" fill="#12060c"/><circle cx="0" cy="90" r="18" fill="#12060c"/></g>''')
# 7 PIN/OTP keypad with lock
S['i-keypad']=('g',phone(540,760,1.25,"#0c1f18",''.join(f'<circle cx="{x}" cy="{y}" r="30" fill="#1d3a30"/>' for x in (-70,0,70) for y in (-80,0,80,160))+'<g fill="#2ee59d"><circle cx="-60" cy="-170" r="14"/><circle cx="-20" cy="-170" r="14"/><circle cx="20" cy="-170" r="14"/><circle cx="60" cy="-170" r="14"/></g>')+
  '<g transform="translate(800,1160)"><rect x="-110" y="-60" width="220" height="180" rx="26" fill="#2ee59d"/><path d="M-70 -60 V-120 A70 70 0 0 1 70 -120 V-60" fill="none" stroke="#2ee59d" stroke-width="30"/><circle cx="0" cy="20" r="24" fill="#06140f"/><rect x="-10" y="20" width="20" height="60" fill="#06140f"/></g>')
# 8 cloned pages (stack of identical cards)
S['i-clone']=('r',''.join(f'<g transform="translate({300+i*60},{430+i*70})"><rect width="480" height="560" rx="30" fill="{"#2ee59d" if i==4 else "#2a2230"}" stroke="{"#2ee59d" if i==4 else "#ff5a6a"}" stroke-width="6" {"" if i==4 else "stroke-dasharray=\"22 14\""} opacity="{1 if i==4 else .85}"/><circle cx="80" cy="80" r="44" fill="{"#06140f" if i==4 else "#ff5a6a"}" opacity=".8"/><rect x="140" y="58" width="220" height="22" rx="11" fill="{"#06140f" if i==4 else "#6b4a5a"}"/><rect x="40" y="160" width="400" height="220" rx="18" fill="{"#0b3d2c" if i==4 else "#3a2a36"}"/></g>' for i in range(5)))
# 9 prize box with hook
S['i-prize']=('y','''<g transform="translate(540,820)"><rect x="-260" y="-80" width="520" height="360" rx="24" fill="#ef4444"/><rect x="-300" y="-180" width="600" height="120" rx="20" fill="#f87171"/>
<rect x="-40" y="-180" width="80" height="460" fill="#ffc845"/><path d="M0 -180 C-120 -330 -260 -250 -150 -190 M0 -180 C120 -330 260 -250 150 -190" fill="none" stroke="#ffc845" stroke-width="30" stroke-linecap="round"/></g>
<line x1="540" y1="0" x2="540" y2="560" stroke="#c9d3e0" stroke-width="6"/><path d="M540 560 L540 610 C540 660 610 660 610 610" fill="none" stroke="#e8edf5" stroke-width="14" stroke-linecap="round"/>''')
# 10 phone call with AI waveform face
S['i-aicall']=('r',phone(540,780,1.3,"#140a1f",'<circle cx="0" cy="-110" r="80" fill="#6d28d9"/><g fill="none" stroke="#c4b5fd" stroke-width="8" stroke-linecap="round"><path d="M-90 40 v40 M-60 20 v80 M-30 0 v120 M0 -10 v140 M30 0 v120 M60 20 v80 M90 40 v40"/></g><circle cx="-60" cy="190" r="30" fill="#dc2626"/><circle cx="60" cy="190" r="30" fill="#16a34a"/>')+
  '<g fill="none" stroke="#ff5a6a" stroke-width="12" stroke-linecap="round" opacity=".8"><path d="M770 520 a90 90 0 0 1 0 140"/><path d="M820 470 a160 160 0 0 1 0 240"/><path d="M310 520 a90 90 0 0 0 0 140"/><path d="M260 470 a160 160 0 0 0 0 240"/></g>')
# 11 empty parcel box
S['i-parcel']=('y','''<g transform="translate(540,860)"><path d="M-300 -120 L0 -220 L300 -120 L0 -20Z" fill="#c08a4a"/><path d="M-300 -120 L0 -20 L0 300 L-300 200Z" fill="#a8743a"/><path d="M300 -120 L0 -20 L0 300 L300 200Z" fill="#8f6130"/>
<path d="M-300 -120 L-420 -260 L-120 -360 L0 -220Z" fill="#d49a58"/><path d="M300 -120 L420 -260 L120 -360 L0 -220Z" fill="#b8803f"/>
<ellipse cx="0" cy="-120" rx="200" ry="60" fill="#3a2a14"/></g>
<g transform="translate(540,420)"><circle r="110" fill="#1d1b24" stroke="#ff5a6a" stroke-width="12"/><path d="M-30 -40 Q-30 -80 0 -80 Q40 -80 40 -45 Q40 -15 0 0 V30" fill="none" stroke="#ff5a6a" stroke-width="18" stroke-linecap="round"/><circle cx="0" cy="70" r="14" fill="#ff5a6a"/></g>''')
# 12 bank card chained by handcuff (mule)
S['i-mule']=('r','''<g transform="translate(470,760) rotate(-10)"><rect x="-260" y="-160" width="520" height="320" rx="34" fill="#2563eb"/><rect x="-200" y="-70" width="90" height="70" rx="12" fill="#ffc845"/><rect x="-200" y="60" width="300" height="26" rx="13" fill="#bfdbfe"/></g>
<g fill="none" stroke="#cbd5e1" stroke-width="26"><circle cx="760" cy="980" r="90"/><circle cx="760" cy="1240" r="90"/></g><rect x="745" y="1060" width="30" height="110" fill="#94a3b8"/>
<path d="M650 900 L590 860" stroke="#cbd5e1" stroke-width="26" stroke-linecap="round"/>''')
# 13 gavel + handcuffs (criminal penalty)
S['i-law']=('b','''<g transform="translate(540,720) rotate(-35)"><rect x="-60" y="-200" width="120" height="260" rx="20" fill="#a16207"/><rect x="-170" y="-260" width="340" height="110" rx="24" fill="#ca8a04"/><rect x="-24" y="40" width="48" height="380" rx="20" fill="#854d0e"/></g>
<rect x="250" y="1080" width="580" height="80" rx="20" fill="#713f12"/>
<g fill="none" stroke="#cbd5e1" stroke-width="24"><circle cx="760" cy="420" r="80"/><circle cx="900" cy="560" r="80"/></g><path d="M815 475 L845 505" stroke="#94a3b8" stroke-width="20"/>''')
# 14 shield check
S['i-shield']=('g','''<g transform="translate(540,760)"><path d="M0 -360 L300 -250 V20 C300 200 160 320 0 380 C-160 320 -300 200 -300 20 V-250Z" fill="#14532d" stroke="#2ee59d" stroke-width="18"/>
<path d="M-130 10 L-40 110 L150 -110" fill="none" stroke="#2ee59d" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/></g>''')
# 15 family with phone
S['i-family']=('y','''<g fill="#fbbf24"><circle cx="380" cy="560" r="90"/><path d="M240 980 C240 760 300 680 380 680 C460 680 520 760 520 980Z"/></g>
<g fill="#f59e0b"><circle cx="700" cy="600" r="80"/><path d="M570 980 C570 790 620 715 700 715 C780 715 830 790 830 980Z"/></g>
<g fill="#fde68a"><circle cx="540" cy="760" r="60"/><path d="M450 980 C450 860 490 820 540 820 C590 820 630 860 630 980Z"/></g>
<g transform="translate(540,1180)"><rect x="-70" y="-120" width="140" height="240" rx="24" fill="#1d1b24" stroke="#ffc845" stroke-width="8"/><path d="M-30 0 L-5 30 L40 -30" fill="none" stroke="#2ee59d" stroke-width="16" stroke-linecap="round"/></g>''')
# 16 police siren + phone
S['i-police']=('b','''<g transform="translate(540,640)"><rect x="-220" y="80" width="440" height="80" rx="20" fill="#334155"/><path d="M-160 80 V-40 A160 160 0 0 1 160 -40 V80Z" fill="#2563eb"/><path d="M-110 80 V-30 A110 110 0 0 1 0 -140 V80Z" fill="#60a5fa" opacity=".6"/>
<g stroke="#60a5fa" stroke-width="16" stroke-linecap="round"><path d="M-260 -120 L-210 -80"/><path d="M260 -120 L210 -80"/><path d="M0 -260 V-200"/><path d="M-160 -220 L-130 -170"/><path d="M160 -220 L130 -170"/></g></g>'''
  +phone(540,1200,.7,"#0f1a2b",'<path d="M-50 -60 C-50 -110 50 -110 50 -60 L40 40 C30 70 -30 70 -40 40Z" fill="#2ee59d"/>'))
# 17 chat threat lock-out (account closing)
S['i-threat']=('r',phone(540,780,1.25,"#140a10",'<rect x="-110" y="-180" width="220" height="110" rx="24" fill="#2a2833"/><rect x="-90" y="-150" width="160" height="16" rx="8" fill="#ff5a6a"/><rect x="-90" y="-115" width="110" height="16" rx="8" fill="#6b5a66"/><g transform="translate(0,90)"><rect x="-80" y="-30" width="160" height="130" rx="20" fill="#ff3b55"/><path d="M-50 -30 V-70 A50 50 0 0 1 50 -70 V-30" fill="none" stroke="#ff3b55" stroke-width="22"/></g>'))
html_tpl='<html><body style="margin:0;width:1080px;height:1920px;background:{bg}"><svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;top:-170px">{svg}</svg></body></html>'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1920})
    for n,(c,svg) in S.items():
        pg.set_content(html_tpl.format(bg=BG[c],svg=svg)); pg.wait_for_timeout(150); pg.screenshot(path=f"photos/{n}.jpg",type="jpeg",quality=90)
    b.close()
print("ok",len(S))

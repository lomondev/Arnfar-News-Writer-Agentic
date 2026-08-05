## POST (copy from here ↓)

🚨🤖 ຂ່າວດ່ວນດ້ານຄວາມປອດໄພ! ມີ AI ໂຄດດິ້ງ "Agentjacking" — ແຮກເກີສັ່ງໃຫ້ AI ຂອງທ່ານ run ໂຄດອັນຕະລາຍໂດຍບໍ່ຕ້ອງເຈາະລະບົບ ⚡️🇱🇦

ສະບາຍດີຊາວ Arnfar! ຖ້າທ່ານໃຊ້ AI ຊ່ວຍຂຽນໂຄດ ເຊັ່ນ Claude Code, Cursor ຫຼື Codex — ຂ່າວນີ້ສຳຄັນຫຼາຍ. ບໍລິສັດຄວາມປອດໄພ Tenet Security ຫາກໍເປີດເຜີຍວິທີໂຈມຕີແບບໃໝ່ຊື່ "Agentjacking" ທີ່ປ່ຽນ AI ຜູ້ຊ່ວຍທີ່ເຮົາໄວ້ໃຈ ໃຫ້ກາຍເປັນ "ມືປືນ" run ຄຳສັ່ງຂອງແຮກເກີຢູ່ເທິງເຄື່ອງຂອງນັກພັດທະນາເອງ. ເປີດເຜີຍວັນທີ 12 ມິຖຸນາ 2026.

🔍 ມັນເກີດຫຍັງຂຶ້ນ?
ການໂຈມຕີນີ້ໃຊ້ຊ່ອງຫວ່າງລະຫວ່າງ Sentry (ເຄື່ອງມືຕິດຕາມ error ຂອງແອັບ) ກັບ MCP (Model Context Protocol — ມາດຕະຖານທີ່ AI ໃຊ້ເຊື່ອມຕໍ່ກັບເຄື່ອງມືພາຍນອກ). ອີງຕາມ Tenet ຂັ້ນຕອນເປັນດັ່ງນີ້:
• ແຮກເກີຫາ "DSN" ຂອງເປົ້າໝາຍ — ເປັນ key ສາທາລະນະທີ່ມັກຝັງໄວ້ໃນ JavaScript ໜ້າເວັບ ແລະ ຄົ້ນຫາໄດ້ທົ່ວໄປ
• ແຮກເກີສົ່ງ "error ປອມ" ເຂົ້າ Sentry ໂດຍໃຊ້ DSN ນັ້ນ, ໂດຍຝັງຄຳສັ່ງອັນຕະລາຍໄວ້ໃນຮູບແບບ markdown ທີ່ເບິ່ງຄືກັບ "ຂັ້ນຕອນແກ້ໄຂ" ປົກກະຕິ
• ເມື່ອນັກພັດທະນາສັ່ງ AI ວ່າ "ຊ່ວຍແກ້ Sentry issue ໃຫ້ແດ່", AI ໄປດຶງ error ນັ້ນຜ່ານ MCP ແລ້ວ run ຄຳສັ່ງຂອງແຮກເກີ — ດ້ວຍສິດຂອງນັກພັດທະນາເອງ
• AI ບໍ່ສາມາດແຍກໄດ້ວ່າ error ໃດແທ້ ແລະ error ໃດປອມ ເພາະ MCP ສົ່ງມາໃຫ້ເບິ່ງຄື "ຂໍ້ມູນລະບົບທີ່ໄວ້ໃຈໄດ້"

ໝາກຜົນ: Tenet ພົບ 2,388 ອົງກອນທີ່ມີ DSN ສ່ຽງຖືກໂຈມຕີ (ລວມທັງບໍລິສັດໃຫຍ່ມູນຄ່າ 250 ຕື້ USD ລົງມາຮອດນັກພັດທະນາຄົນດຽວ) ແລະ ໃນການທົດສອບໄດ້ສຳເລັດເຖິງ 85%. ສິ່ງທີ່ອາດຮົ່ວ: environment variables, AWS keys, GitHub/git credentials, npm tokens ແລະ URL ຂອງ repo ສ່ວນຕົວ.

✅ ຂໍ້ດີ (ສິ່ງທີ່ເຮົາໄດ້ຮຽນຮູ້)
✅ ເປັນການເຕືອນໄພລ່ວງໜ້າ — ນັກວິໄຈເປີດເຜີຍກ່ອນແຮກເກີຈິງຈະໃຊ້ຢ່າງກວ້າງຂວາງ
✅ Tenet ປ່ອຍເຄື່ອງມືແກ້ໄຂ "agent-jackstop" ແບບ open-source ໃຫ້ນຳໄປໃຊ້ໄດ້ຟຣີ
✅ ການປ້ອງກັນທຳອິດ (ປິດ MCP ທີ່ບໍ່ໃຊ້, rotate key) ເຮັດໄດ້ທັນທີ ບໍ່ຕ້ອງລໍ patch

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ການໂຈມຕີ "ຖືກກົດໝາຍ" ທຸກຂັ້ນຕອນ — EDR, WAF, IAM, VPN, Firewall ກວດບໍ່ພົບ ເພາະບໍ່ມີ malware ໃຫ້ກວດ
❌ ແຮກເກີບໍ່ຕ້ອງແຕະລະບົບຂອງເຫຍື່ອເລີຍ — ໃຊ້ພຽງຂໍ້ມູນທີ່ອົງກອນເຜີຍແຜ່ເອງ
❌ Sentry ຍອມຮັບບັນຫາແຕ່ບໍ່ແກ້ເຕັມຮູບແບບ (ບອກວ່າ "ປ້ອງກັນທາງເທັກນິກບໍ່ໄດ້"), ພຽງ block payload string ສະເພາະ — ໜ້າທີ່ປ້ອງກັນຍ້າຍໄປຢູ່ຝັ່ງ AI/MCP

🛠️ ວິທີປ້ອງກັນ (ເຮັດໄດ້ມື້ນີ້)
• ປິດ Sentry MCP integration ຖ້າບໍ່ໄດ້ໃຊ້ ແລະ ລຶບ MCP server ທີ່ບໍ່ໄດ້ໃຊ້ອອກ
• Rotate (ປ່ຽນ) DSN ທີ່ເຄີຍເປີດເຜີຍ ແລະ ເພີ່ມ pattern ຂອງ DSN ເຂົ້າ pre-commit secret scanning
• ຢ່າສັ່ງ AI ໃຫ້ "auto-fix" Sentry issue ໂດຍບໍ່ກວດເບິ່ງຄຳສັ່ງກ່ອນ run (human-in-the-loop)
• ໃຊ້ເຄື່ອງມື "agent-jackstop" ຂອງ Tenet ເພື່ອ harden Cursor/Claude Code
• ຢ່າໄວ້ໃຈ output ຈາກ MCP ແບບ 100% — ປະຕິບັດກັບມັນຄືກັບ "ຂໍ້ມູນຈາກພາຍນອກທີ່ບໍ່ໄວ້ໃຈ"

📌 ສະຫຼຸບ: ໃນຍຸກ AI Agent, ໂຕ AI ເອງກາຍເປັນ "ໜ້າດ່ານໂຈມຕີ" ໃໝ່ — ການໄວ້ໃຈເຄື່ອງມືພາຍນອກແບບບໍ່ມີຂອບເຂດ ຄືຄວາມສ່ຽງທີ່ໃຫຍ່ທີ່ສຸດ.

👉 ທ່ານໃຊ້ AI ຊ່ວຍຂຽນໂຄດບໍ? ເຊື່ອມຕໍ່ MCP ກັບເຄື່ອງມືໃດແດ່? ມາແບ່ງປັນ ແລະ ລະວັງນຳກັນ! 💬

#arnfar #Agentjacking #AISecurity #MCP #LaoDev

## (copy to here ↑)

---

## Sources
- Agentjacking Attack Tricks AI Coding Agents Into Running Malicious Code — The Hacker News — https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html
- One Fake Bug Report Hijacked a $250B Company's AI Agent — Tenet Security — https://tenetsecurity.ai/blog/agentjacking-coding-agents-with-fake-sentry-errors/
- New "Agentjacking" Attacks Could Hijack AI Coding Agents — Infosecurity Magazine — https://www.infosecurity-magazine.com/news/agentjacking-attacks-hijack-ai/
- A public Sentry key is all it takes to hijack Claude Code, Cursor, and Codex — The New Stack — https://thenewstack.io/agentjacking-sentry-mcp-attack/
- New Agentjacking Attack Hijacks Your AI Coding Agent — Cybersecurity News — https://cybersecuritynews.com/agentjacking-attack-hijacks-ai-coding-agent/

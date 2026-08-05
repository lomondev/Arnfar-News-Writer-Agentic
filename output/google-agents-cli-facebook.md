## POST (copy from here ↓)

🚀🤖 Google ຫາກໍປ່ອຍ "Agents CLI" — ເຄື່ອງມືທີ່ປ່ຽນ AI ຊ່ວຍຂຽນໂຄ້ດຂອງທ່ານໃຫ້ກາຍເປັນ "ຜູ້ຊ່ຽວຊານ" ສ້າງ AI Agent ຂຶ້ນໃຊ້ຈິງ! ⚡️🇱🇦

ສະບາຍດີຊາວ Arnfar! ຖ້າທ່ານຢາກສ້າງ AI Agent (ໂປຣແກຣມ AI ທີ່ເຮັດວຽກແທນເຮົາໄດ້) ແຕ່ບໍ່ຮູ້ຈະເລີ່ມຈາກໃສ — ຂ່າວນີ້ສຳລັບທ່ານ. Google ໄດ້ເປີດໂຕ **Agents CLI in Agent Platform** (ຊື່ສັ້ນ `agents-cli`) ເຄື່ອງມືແບບ Open Source ທີ່ຊ່ວຍໃຫ້ການສ້າງ, ທົດສອບ ແລະ ນຳໃຊ້ AI Agent ຂຶ້ນ Cloud ງ່າຍຂຶ້ນຫຼາຍ.

🔍 ມັນເກີດຫຍັງຂຶ້ນ?
Google ເປີດໂຕ `agents-cli` ຢ່າງເປັນທາງການຜ່ານ Google Developers Blog ເມື່ອວັນທີ 22 ເດືອນເມສາ 2026, ປັດຈຸບັນຮອດເວີຊັນ v0.6.1 (ອອກວັນທີ 28 ເດືອນມິຖຸນາ 2026) ແລະ ມີດາວ (star) ເທິງ GitHub ແລ້ວກວ່າ 3,400 ດວງ.

ຈຸດເດັ່ນຄື ມັນ **ບໍ່ແມ່ນ AI ຂຽນໂຄ້ດເອງ** ແຕ່ເປັນ "ຕົວຊ່ວຍ" ທີ່ເອົາໄປໃສ່ AI ຂຽນໂຄ້ດທີ່ທ່ານໃຊ້ຢູ່ (ເຊັ່ນ Claude Code, Codex, Gemini CLI, Antigravity CLI) ເພື່ອໃຫ້ມັນເກັ່ງເລື່ອງການສ້າງ Agent ຂຶ້ນ. ອີງຕາມ Google, ມັນສ້າງຢູ່ເທິງ ADK (Agent Development Kit) — ເຟຣມເວີກ Open Source ຂອງ Google ສຳລັບສ້າງ Agent.
• License: Apache 2.0 (Open Source, ໃຊ້ຟຣີ) — ຍັງຢູ່ໃນຂັ້ນ Preview / Pre-GA
• ຕິດຕັ້ງດ້ວຍຄຳສັ່ງດຽວ: `uvx google-agents-cli setup`
• ຕ້ອງມີ: Python 3.11+, uv ແລະ Node.js
• ຄຳສັ່ງຫຼັກ: `scaffold` (ສ້າງໂປຣເຈັກ) → `run` (ລອງແລ່ນ) → `eval` (ວັດຄຸນນະພາບ) → `deploy` (ຂຶ້ນ Cloud) → `publish`
• ນຳໃຊ້ໄດ້ 3 ບ່ອນ: Agent Runtime, Cloud Run, ຫຼື GKE
• ມາພ້ອມ 7 skills ຄຸມທັງວົງຈອນ: ຂຽນໂຄ້ດ ADK, ປະເມີນຜົນ, deploy, publish ແລະ observability (ຕິດຕາມ/ກວດສອບ)

✅ ຂໍ້ດີ
✅ Open Source (Apache 2.0) — ໃຊ້ ແລະ ດັດແປງໄດ້ຟຣີ
✅ ພັດທະນາໃນເຄື່ອງໄດ້ໂດຍໃຊ້ພຽງ AI Studio API key — ບໍ່ຈຳເປັນຕ້ອງມີ Google Cloud ຕັ້ງແຕ່ຕົ້ນ
✅ ບໍ່ຜູກກັບ AI ຕົວໃດຕົວໜຶ່ງ — ໃຊ້ຮ່ວມກັບ Claude Code, Codex, Gemini CLI ໄດ້
✅ ຄຸມຕັ້ງແຕ່ສ້າງ ຮອດການ deploy ຂຶ້ນ production ໃນເຄື່ອງມືດຽວ (create-to-production)

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ຍັງເປັນ Preview (Pre-GA) — ອາດມີການປ່ຽນແປງ ຫຼື ບັກ, ຍັງບໍ່ຄວນເອົາໄປໃຊ້ວຽກສຳຄັນທັນທີ
❌ ການ deploy ຈິງຕ້ອງມີ Google Cloud project — ມີຄ່າໃຊ້ຈ່າຍຕາມການໃຊ້ງານ (ຄິດ USD)
❌ ຜູກກັບລະບົບນິເວດ Google (ADK, Gemini, Vertex) — ຍ້າຍໄປ platform ອື່ນອາດຫຍຸ້ງຍາກ
❌ ຕ້ອງມີພື້ນຖານ command line ແລະ Python — ຍັງບໍ່ເໝາະສຳລັບຜູ້ເລີ່ມຕົ້ນທີ່ບໍ່ເຄີຍຂຽນໂຄ້ດ

📌 ສະຫຼຸບ: `agents-cli` ຄືການທີ່ Google ພະຍາຍາມເຮັດໃຫ້ການສ້າງ AI Agent ຂຶ້ນໃຊ້ຈິງ "ໄວ ແລະ ງ່າຍ" ໂດຍໃຊ້ AI ຂຽນໂຄ້ດທີ່ທ່ານມັກຢູ່ແລ້ວ.

👉 ຖ້າມີເຄື່ອງມືແບບນີ້ ທ່ານຢາກສ້າງ AI Agent ໄປເຮັດວຽກຫຍັງໃຫ້ທຸລະກິດ ຫຼື ຊີວິດປະຈຳວັນຂອງທ່ານ? ມາແບ່ງປັນກັນ! 💬

#arnfar #GoogleCloud #AIagent #ADK #LaoTech

## (copy to here ↑)

---

## Sources
- Agents CLI in Agent Platform: create to production in one CLI — Google Developers Blog — https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/
- google/agents-cli (README, commands, skills, license, v0.6.1) — GitHub — https://github.com/google/agents-cli
- agents-cli documentation — Google — https://google.github.io/agents-cli/
- google-agents-cli — PyPI — https://pypi.org/project/google-agents-cli/

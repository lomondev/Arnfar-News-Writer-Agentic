# Model Context Protocol ປ່ອຍສະບັບແກ້ໄຂໃຫຍ່ທີ່ສຸດນັບແຕ່ເປີດໂຕ ປ່ຽນເປັນ "Stateless" — ສະບັບສົມບູນຈະອອກ 28 ກໍລະກົດ 2026

**ສະຫຼຸບ:** ໂຄງການ Model Context Protocol (MCP) — ມາດຕະຖານເປີດ (open standard) ສຳລັບເຊື່ອມຕໍ່ແອັບ AI ເຂົ້າກັບຂໍ້ມູນ, ເຄື່ອງມື ແລະ ລະບົບພາຍນອກ — ໄດ້ປ່ອຍ "release candidate" (ສະບັບທົດສອບກ່ອນອອກຈິງ) ຂອງສະເປັກສະບັບໃໝ່ລະຫັດ `2026-07-28` ອອກມາ, ໂດຍລັອກສະບັບໃນວັນທີ 21 ພຶດສະພາ 2026 ແລະ ກຳນົດປ່ອຍສະບັບສົມບູນໃນວັນທີ 28 ກໍລະກົດ 2026. ທີມຜູ້ດູແລລະບຸວ່ານີ້ແມ່ນການແກ້ໄຂໃຫຍ່ທີ່ສຸດນັບແຕ່ MCP ເປີດໂຕມາ, ໂດຍຈຸດປ່ຽນຫຼັກແມ່ນການເຮັດໃຫ້ໂປຣໂຕຄໍກາຍເປັນ "stateless" (ບໍ່ຕ້ອງຈື່ສະຖານະການເຊື່ອມຕໍ່), ພ້ອມການປ່ຽນແປງທີ່ມີຜົນກະທົບແບບ breaking change ຫຼາຍຢ່າງ.

MCP ເປັນມາດຕະຖານເປີດທີ່ Anthropic ສ້າງຂຶ້ນເພື່ອໃຫ້ແອັບ AI ເຊັ່ນ Claude ຫຼື ChatGPT ສາມາດເຊື່ອມຕໍ່ກັບແຫຼ່ງຂໍ້ມູນ (ໄຟລ໌, ຖານຂໍ້ມູນ), ເຄື່ອງມື (search, ເຄື່ອງຄິດໄລ່) ແລະ ຂັ້ນຕອນວຽກຕ່າງໆ — ເອກະສານທາງການປຽບທຽບມັນຄືກັບ "ຮູສຽບ USB-C ສຳລັບ AI" ຄື ມາດຕະຖານດຽວທີ່ເຮັດໃຫ້ເຊື່ອມຕໍ່ກັນໄດ້ທົ່ວ.

ການປ່ຽນແປງສຳຄັນທີ່ສຸດໃນສະບັບ `2026-07-28` ແມ່ນ MCP ກາຍເປັນ stateless ໃນລະດັບໂປຣໂຕຄໍ. ອີງຕາມ blog ຂອງໂຄງການ, ການ "handshake" ແບບ initialize/initialized ແລະ header `Mcp-Session-Id` ຖືກຖອດອອກ, ໝາຍຄວາມວ່າທຸກ request ສາມາດສົ່ງໄປຫາ server instance ໃດກໍ່ໄດ້. ຜົນທີ່ໄດ້ໃນທາງປະຕິບັດແມ່ນ remote MCP server ທີ່ແຕ່ກ່ອນຕ້ອງໃຊ້ sticky session ແລະ session store ຮ່ວມກັນ, ດຽວນີ້ສາມາດແລ່ນຫຼັງ load balancer ແບບ round-robin ທຳມະດາໄດ້ ແລະ route ດ້ວຍ header `Mcp-Method`. ນັກພັດທະນາທີ່ຕ້ອງການເກັບສະຖານະຍັງເຮັດໄດ້ ໂດຍໃຫ້ tool ສ້າງ handle ຊັດເຈນ (ເຊັ່ນ `basket_id`) ແລ້ວສົ່ງກັບເຂົ້າມາເປັນ argument ໃນການເອີ້ນຄັ້ງຕໍ່ໄປ.

ສະບັບໃໝ່ນີ້ຍັງຍົກ "Extensions" (ສ່ວນຂະຫຍາຍ) ຂຶ້ນເປັນ first-class ພ້ອມຂັ້ນຕອນທາງການ, ໂດຍປ່ອຍ 2 extension ທາງການ. ອັນທຳອິດແມ່ນ MCP Apps ທີ່ໃຫ້ server ສົ່ງໜ້າຕາ UI ແບບ HTML ໂຕ້ຕອບໄດ້ ເຊິ່ງ host ຈະ render ໃນ sandboxed iframe; ອັນທີສອງແມ່ນ Tasks (ສຳລັບວຽກໄລຍະຍາວ) ທີ່ຍ້າຍຈາກ feature ທົດລອງໃນ core ມາເປັນ extension. ນອກນັ້ນ ຍັງມີການ "hardening" ດ້ານ authorization ໃຫ້ສອດຄ່ອງກັບ OAuth 2.0 ແລະ OpenID Connect ຫຼາຍຂຶ້ນ, ການຍົກ tool schema ໄປໃຊ້ JSON Schema 2020-12 ເຕັມຮູບແບບ, ແລະ ນະໂຍບາຍ deprecation ທາງການເປັນຄັ້ງທຳອິດ.

ພ້ອມກັນນັ້ນ, ຄຸນສົມບັດຫຼັກ 3 ຢ່າງ ຄື Roots, Sampling ແລະ Logging ຖືກປະກາດ deprecated (ເຊົາສະໜັບສະໜູນໃນອະນາຄົດ) ພາຍໃຕ້ນະໂຍບາຍ lifecycle ໃໝ່ ທີ່ກຳນົດໄລຍະຢ່າງໜ້ອຍ 12 ເດືອນ ກ່ອນຈະຖອດອອກໄດ້. ທີມງານເຕືອນວ່າສະບັບນີ້ມີ breaking changes ແລະ ໄດ້ກຳນົດໄລຍະທົດສອບ 10 ອາທິດ ໃຫ້ຜູ້ພັດທະນາ SDK ແລະ client ກວດສອບກັບວຽກຈິງກ່ອນສະບັບສົມບູນຈະອອກ.

ການປ່ຽນແປງດ້ານເຕັກນິກນີ້ເກີດຂຶ້ນຫຼັງຈາກ MCP ມີການປ່ຽນແປງດ້ານການຄຸ້ມຄອງຄັ້ງໃຫຍ່. ໃນເດືອນທັນວາ 2025, Anthropic ໄດ້ບໍລິຈາກ MCP ໃຫ້ Agentic AI Foundation (AAIF) ເຊິ່ງເປັນກອງທຶນພາຍໃຕ້ Linux Foundation ທີ່ Anthropic, Block ແລະ OpenAI ຮ່ວມກັນກໍ່ຕັ້ງ — ເຮັດໃຫ້ມາດຕະຖານນີ້ກາຍເປັນກາງ ບໍ່ຂຶ້ນກັບບໍລິສັດດຽວ. ຕໍ່ມາ ໃນເດືອນເມສາ 2026, AAIF ໄດ້ຈັດງານ MCP Dev Summit North America ທີ່ນະຄອນ New York ໂດຍມີຜູ້ເຂົ້າຮ່ວມປະມານ 1,200 ຄົນ.

ໃນດ້ານການນຳໃຊ້, MCP ໄດ້ກາຍເປັນມາດຕະຖານອຸດສາຫະກຳໄປແລ້ວ. ມີລາຍງານວ່າ MCP ມີຍອດດາວໂຫຼດ SDK ປະມານ 97 ລ້ານຄັ້ງຕໍ່ເດືອນ ແລະ ມີ server ສາທາລະນະທີ່ໃຊ້ງານຫຼາຍກວ່າ 10,000 ໂຕ. ຜູ້ນຳໃຊ້ລາຍໃຫຍ່ປະກອບມີ Anthropic (Claude Desktop, Claude Code), OpenAI (ChatGPT), Google (Gemini/DeepMind), Microsoft (Copilot, Visual Studio Code), Cursor, Salesforce (Agentforce), Block, Cloudflare ແລະ Replit.

ສິ່ງທີ່ຕ້ອງຕິດຕາມຕໍ່ແມ່ນວັນທີ 28 ກໍລະກົດ 2026 ເຊິ່ງເປັນມື້ປ່ອຍສະບັບສົມບູນ. ສຳລັບນັກພັດທະນາ ແລະ ທຸລະກິດລາວທີ່ກຳລັງສ້າງ ຫຼື ໃຊ້ MCP server, ການປ່ຽນເປັນ stateless ໝາຍຄວາມວ່າຈະ deploy ແບບ scale ໄດ້ງ່າຍຂຶ້ນ ແຕ່ກໍ່ຕ້ອງກຽມແກ້ໂຄດ ເພາະມີ breaking change ໃນ transport, session, Tasks ແລະ ລະຫັດ error ບາງຢ່າງ.

---

## ແຫຼ່ງຂໍ້ມູນ (Sources)
- What is the Model Context Protocol (MCP)? — modelcontextprotocol.io — https://modelcontextprotocol.io/docs/getting-started/intro
- The 2026-07-28 MCP Specification Release Candidate — Model Context Protocol Blog — https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
- The 2026 MCP Roadmap — Model Context Protocol Blog — https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- Donating the Model Context Protocol and establishing the Agentic AI Foundation — Anthropic — https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
- Model Context Protocol — Wikipedia — https://en.wikipedia.org/wiki/Model_Context_Protocol
- MCP Adoption Statistics 2026 — DigitalApplied — https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol

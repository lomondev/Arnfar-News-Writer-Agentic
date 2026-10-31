# LiteLLM ພົບຊ່ອງໂຫວ່ຮ້າຍແຮງ ຄວນອັບເດດເປັນ 1.83.9 ດ່ວນ

## POST (copy from here ↓)

ໃຜໃຊ້ LiteLLM ເປັນ gateway ເອີ້ນ AI ຢູ່, ມື້ນີ້ຄວນອັບເດດກ່ອນເຮັດວຽກອື່ນ.

Check Point Research ເປີດເຜີຍຊ່ອງໂຫວ່ 2 ຈຸດໃນ LiteLLM ເຊິ່ງເປັນ AI gateway ແບບ open source ທີ່ມີຄົນດາວໂຫຼດຫຼາຍກວ່າ 90 ລ້ານຄັ້ງຕໍ່ເດືອນ ແລະ ເຊື່ອມຕໍ່ກັບຜູ້ໃຫ້ບໍລິການ AI ປະມານ 140 ເຈົ້າ ເຊັ່ນ OpenAI ແລະ Anthropic.

ຈຸດທຳອິດ CVE-2026-35029 (ຄະແນນ 8.7/10) ຮ້າຍແຮງທີ່ສຸດ. ຜູ້ໃຊ້ທີ່ມີສິດໜ້ອຍສາມາດເຂົ້າໄປແກ້ການຕັ້ງຄ່າຂອງ admin ຜ່ານ /config/update ໄດ້. ຈາກນັ້ນສາມາດອ່ານໄຟລ໌ລັບໃນເຊີບເວີ, ປ່ຽນລະຫັດ admin ເພື່ອຍຶດລະບົບ, ຈົນເຖິງໂຫຼດໂຄດອັນຕະລາຍມາແລ່ນ.

ຈຸດທີສອງ CVE-2026-59823 (ຄະແນນ 5.3/10) ເປັນແບບ SSRF. ຜູ້ໃຊ້ສາມາດສັ່ງໃຫ້ LiteLLM ສົ່ງຄຳຂໍໄປຫາເຊີບເວີຂອງຕົນເອງ ພ້ອມ API key ຂອງຜູ້ໃຫ້ບໍລິການ AI ທີ່ເກັບໄວ້. ໄດ້ key ໄປແລ້ວ ຄົນອື່ນກໍເອົາໄປໃຊ້ AI ໃຫ້ບໍລິສັດທ່ານເປັນຄົນຈ່າຍບິນ.

ທຸກເວີຊັນກ່ອນ 1.83.9 ໄດ້ຮັບຜົນກະທົບ. ສິ່ງທີ່ທີມ dev ຄວນເຮັດມື້ນີ້:
• ອັບເດດເປັນ 1.83.9 ຫຼື ໃໝ່ກວ່າ: pip install -U "litellm>=1.83.9"
• ກວດວ່າໃຜມີບັນຊີເຂົ້າ gateway ໄດ້ແດ່ ແລະ ລຶບບັນຊີທີ່ບໍ່ໃຊ້
• ຖ້າສົງໄສວ່າມີຄົນເຂົ້າມາໂດຍບໍ່ໄດ້ຮັບອະນຸຍາດ ໃຫ້ປ່ຽນ API key ຂອງ OpenAI, Anthropic ແລະ ອື່ນໆ ທັນທີ
• ຊອກເບິ່ງວ່າມີ LiteLLM ຝັງຢູ່ໃນເຄື່ອງມືອື່ນທີ່ທີມບໍ່ໄດ້ຕິດຕັ້ງເອງ

ນີ້ບໍ່ແມ່ນເທື່ອທຳອິດຂອງປີ. ໃນເດືອນມີນາ ມີກຸ່ມແຮັກເກີປ່ອຍແພັກເກັດ LiteLLM ປອມ ເວີຊັນ 1.82.7 ແລະ 1.82.8 ຂຶ້ນ PyPI ມາແລ້ວ. AI gateway ຖື key ທີ່ມີມູນຄ່າເງິນແທ້, ສະນັ້ນຄວນດູແລມັນຄືກັບລະບົບການເງິນ.

ທີມທ່ານໃຊ້ຫຍັງເປັນ gateway ເອີ້ນ AI: LiteLLM, OpenRouter ຫຼື ຂຽນເອງ?

ຕິດຕາມເພຈ Arnfar ໄວ້ ເພື່ອຮູ້ທັນເລື່ອງຄວາມປອດໄພຂອງລະບົບ AI.

#arnfar #LiteLLM #CyberSecurity #AI

## (copy to here ↑)

---

## Sources
- Check Point Reports LiteLLM Flaws Enabling Admin Takeover and API Key Theft — Hackread — https://hackread.com/check-point-litellm-flaws-admin-takeover-api-key-theft/
- Security flaws found in top open source AI gateway — TechRadar Pro — https://www.techradar.com/pro/security/security-flaws-found-in-top-open-source-ai-gateway-litellm-vulnerabilties-could-affect-millions-of-users

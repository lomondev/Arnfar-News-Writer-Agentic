# Kimi ຂຽນ code ສ້າງ 3D ໄດ້ — ອອກແບບເຮືອນ 3D ຈາກຄຳສັ່ງ

## POST (copy from here ↓)

🏠🤖 ບອກ AI ເປັນຄຳເວົ້າ ແລ້ວໄດ້ແບບເຮືອນ 3D ທີ່ໝູນເບິ່ງໄດ້! Kimi ຂຽນ code ສ້າງ 3D ໃຫ້ອັດຕະໂນມັດ ⚡️

ສະບາຍດີຊາວ Arnfar! AI ຊື່ Kimi ຈາກບໍລິສັດ Moonshot AI (ຈີນ) ດຽວນີ້ຂຽນ code ສ້າງ scene 3D ແບບໂຕ້ຕອບໄດ້ຈາກຄຳສັ່ງທີ່ພິມເຂົ້າໄປ — ໝາຍຄວາມວ່າ ທ່ານສາມາດໃຫ້ມັນສ້າງແບບຈຳລອງເຮືອນ ຫຼື ຫ້ອງ 3D ໄດ້ ໂດຍບໍ່ຕ້ອງເປັນຊ່ຽວຊານດ້ານ 3D.

🔍 ເຫດການທີ່ເກີດຂຶ້ນ
Kimi K2.5 ເປັນ AI multimodal (ຮັບໄດ້ທັງຂໍ້ຄວາມ, ຮູບ ແລະ video) ແບບ open-source ຈາກ Moonshot AI, ເປີດໂຕເມື່ອວັນທີ 27 ເດືອນມັງກອນ 2026. ຈຸດເດັ່ນຄື "visual-to-code" — ປ່ຽນຄຳບັນຍາຍ ຫຼື ຮູບແບບ ໃຫ້ກາຍເປັນ code ໜ້າເວັບທີ່ໃຊ້ໄດ້ຈິງ.

ຕໍ່ມາ Moonshot AI ໄດ້ປ່ອຍ Kimi K2.7-Code ໃນວັນທີ 12 ເດືອນມິຖຸນາ 2026 ເຊິ່ງເນັ້ນວຽກຂຽນ code ໂດຍສະເພາະ. ອີງຕາມ Moonshot AI:
• ເປັນໂມເດລ 1 ລ້ານລ້ານ parameter (ແບບ MoE, ໃຊ້ງານ 32B ຕໍ່ token)
• Context window ໃຫຍ່ເຖິງ 256K token — ຈັດການ project ຫຼາຍໄຟລ໌ໄດ້
• ປ່ອຍນ້ຳໜັກໂມເດລແບບ open-source (ໃບອະນຸຍາດ Modified MIT) ຢູ່ Hugging Face
• ຄົນທົດລອງໃຫ້ Kimi ຂຽນ code ສ້າງ scene 3D ເທິງເວັບໄດ້ຈິງ ເຊັ່ນ ເກມ 3D ແລະ ການຈຳລອງຕ່າງໆ ພຽງແຕ່ພິມຄຳສັ່ງ

ຂໍ້ສຳຄັນ: Kimi ບໍ່ໄດ້ມີ "ໂປຣແກຣມອອກແບບເຮືອນ" ສຳເລັດຮູບ. ມັນຂຽນ code (ເຊັ່ນ Three.js/HTML) ໃຫ້ ແລ້ວທ່ານເອົາໄປ run ແລະ ດັດແກ້ຕໍ່ເອງ.

✅ ຂໍ້ດີ
✅ ບໍ່ຕ້ອງເປັນຊ່ຽວຊານ 3D — ບັນຍາຍເປັນຄຳເວົ້າ ຫຼື ໃສ່ຮູບແປລນ ກໍໄດ້ code 3D
✅ Open-source (Modified MIT) — ດາວໂຫຼດນ້ຳໜັກໄດ້ ແລະ host ເອງໄດ້
✅ ລາຄາໃຊ້ຜ່ານ API ຖືກກວ່າໂມເດລປິດຫຼາຍ (input ~0.95 USD/ລ້ານ token, output ~4.00 USD/ລ້ານ token)
✅ Context 256K token — ຮັບໄດ້ທັງ project ໃຫຍ່

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ບໍ່ແມ່ນໂປຣແກຣມ CAD/BIM ມືອາຊີບ — ຜົນທີ່ໄດ້ເປັນ code ເວັບ ຕ້ອງກວດ ແລະ ແກ້ເອງ
❌ ຄຸນນະພາບຍັງບໍ່ແນ່ນອນ ໂດຍສະເພາະແບບທີ່ຊັບຊ້ອນ
❌ ຕົວເລກ benchmark ຍັງມາຈາກການທົດສອບຂອງ Moonshot ເອງ ຍັງບໍ່ມີຜົນທົດສອບອິດສະຫຼະຈາກພາຍນອກ
❌ ການ host ໂມເດລ 1 ລ້ານລ້ານ parameter ເອງ ຕ້ອງໃຊ້ hardware ແຮງສູງ

📌 ສະຫຼຸບ: Kimi ບໍ່ໄດ້ "ອອກແບບເຮືອນ" ໃຫ້ໂດຍກົງ, ແຕ່ຄວາມສາມາດ visual-to-code ຂອງມັນເຮັດໃຫ້ທ່ານສ້າງແບບຈຳລອງເຮືອນ 3D ແບບໝູນເບິ່ງໄດ້ຈາກຄຳສັ່ງ.

👉 ຖ້າ AI ຊ່ວຍທ່ານສ້າງແບບເຮືອນ 3D ໄດ້ ທ່ານຢາກລອງອອກແບບຫຍັງກ່ອນ? ມາແບ່ງປັນກັນ! 💬

#arnfar #KimiK2 #AICoding #3D

## (copy to here ↑)

---

## Sources
- Moonshot AI Releases Kimi K2.7-Code, a 1T-Parameter Open-Source Coding Model — noqta.tn — https://noqta.tn/en/news/moonshot-kimi-k2-7-code-open-source-coding-model-2026
- Moonshot AI Releases Kimi K2.7-Code: +21.8% on Kimi Code Bench v2 — MarkTechPost — https://www.marktechpost.com/2026/06/12/moonshot-ai-releases-kimi-k2-7-code-a-coding-model-reporting-21-8-on-kimi-code-bench-v2-over-k2-6/
- Kimi K2.5 | Open Visual Agentic Model for Real Work — Moonshot AI (kimi.com) — https://www.kimi.com/ai-models/kimi-k2-5
- Kimi K2.5: Visual Agentic Intelligence (Technical Report) — arXiv — https://arxiv.org/pdf/2602.02276
- Discover Kimi K2: A Trillion Parameter AI Model for Coding — Geeky Gadgets — https://www.geeky-gadgets.com/kimi-k2-open-source-ai-model/
- Kimi K2: A Guide With 6 Practical Examples — DataCamp — https://www.datacamp.com/tutorial/kimi-k2

# PageIndex — RAG ແບບບໍ່ໃຊ້ Vector ທີ່ຕອບຖືກ 98.7% ເທິງ FinanceBench

## POST (copy from here ↓)

🚀🧠 RAG ໂຕໃໝ່ທີ່ "ຖິ້ມ vector database" ຖິ້ມ — ແຕ່ຕອບຖືກເຖິງ 98.7%?! ນີ້ຄື PageIndex ⚡️🇱🇦

ສະບາຍດີຊາວ Arnfar! ຫຼັງຈາກໂພສກ່ອນເລົ່າເລື່ອງ RAG ພື້ນຖານ, ມື້ນີ້ມາຮູ້ຈັກ PageIndex — RAG ແນວທາງໃໝ່ຈາກ VectifyAI ທີ່ "ບໍ່ໃຊ້ vector, ບໍ່ຫັ່ນ chunk" ແຕ່ໃຫ້ LLM ໃຊ້ການ "ຄິດ" ຄົ້ນຫາຄຳຕອບ ຄືກັບຜູ້ຊ່ຽວຊານເປີດອ່ານປຶ້ມ. ສຳລັບໃຜທີ່ເຮັດ AI ອ່ານເອກະສານຍາວ (ສັນຍາ, ບົດລາຍງານການເງິນ, ກົດໝາຍ) ນີ້ຄືແນວທາງທີ່ໜ້າຈັບຕາທີ່ສຸດຂອງປີ.

🔍 ມັນຕ່າງຈາກ RAG ທຳມະດາແນວໃດ?
RAG ແບບເກົ່າຫັ່ນເອກະສານເປັນຕ່ອນ ແລ້ວຄົ້ນຫາດ້ວຍ vector similarity. PageIndex ໃຊ້ວິທີຄິດຄົນລະແບບ:
• ບໍ່ໃຊ້ Vector DB — ໃຊ້ໂຄງສ້າງເອກະສານ + ການ reasoning ຂອງ LLM ແທນການວັດຄວາມຄ້າຍ
• ບໍ່ຫັ່ນ chunk — ຈັດເອກະສານເປັນ tree ຕາມໂຄງສ້າງຈິງ (ບົດ, ຫົວຂໍ້, ໜ້າ)
• ຄົ້ນຫາແບບຄົນ — LLM "ເດີນ" ຜ່ານ tree ຄືກັບຜູ້ຊ່ຽວຊານເປີດຫາຂໍ້ມູນໃນປຶ້ມ
• ໃຊ້ tree search ໄດ້ແຮງບັນດານໃຈຈາກ AlphaGo — ບໍ່ຄົ້ນທຸກບ່ອນ ແຕ່ໃຊ້ກົນລະຍຸດເລືອກເສັ້ນທາງທີ່ຖືກ
• ຜົນທົດສອບ: Mafin 2.5 (agent ທີ່ສ້າງເທິງ PageIndex) ໄດ້ 98.7% ເທິງ FinanceBench ທຽບກັບ RAG vector ທຳມະດາ ~30–50% — ອີງຕາມ VectifyAI
• Open Source (MIT) — GitHub ຮອດ 23,000+ ດາວ (ທ້າຍ ມີນາ 2026)

✅ ຂໍ້ດີ
✅ ຕອບຖືກສູງກັບເອກະສານທີ່ມີໂຄງສ້າງ ແລະ ການອ້າງອີງໄຂ້ວກັນ (ການເງິນ, ກົດໝາຍ, ວິຊາການ)
✅ ຕິດຕາມທີ່ມາຂອງຄຳຕອບໄດ້ຊັດເຈນ (explainable) — ຮູ້ວ່າ AI ດຶງມາຈາກບົດ/ໜ້າໃດ
✅ ບໍ່ຕ້ອງຕັ້ງ ແລະ ດູແລ vector database — ຫຼຸດຄວາມຫຍຸ້ງຍາກ infra
✅ Open Source (MIT) — ທົດລອງ ແລະ ນຳໄປໃຊ້ກັບເອກະສານພາສາລາວໄດ້ຟຣີ

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ເພິ່ງ LLM reasoning ຫຼາຍ — ແຕ່ລະ query ຍິງ LLM ຫຼາຍຮອບ = ຕົ້ນທຶນ ແລະ latency ອາດສູງກວ່າ vector search
❌ ເໝາະກັບເອກະສານທີ່ມີໂຄງສ້າງຊັດເຈນ — ຂໍ້ມູນຫຍາບ ຫຼື chat log ອາດບໍ່ໄດ້ປະໂຫຍດເທົ່າ
❌ ຄຸນນະພາບຂຶ້ນກັບການແປງເອກະສານເປັນ tree — PDF ສະແກນ/ຈັດໜ້າຮ້າຍ ຕ້ອງເຮັດ OCR ໃຫ້ດີກ່ອນ
❌ ຍັງໃໝ່ — ລະບົບນິເວດ ແລະ tooling ຍັງບໍ່ໃຫຍ່ເທົ່າ vector RAG ແບບເກົ່າ

📌 ສະຫຼຸບ: PageIndex ພິສູດວ່າ RAG ບໍ່ຈຳເປັນຕ້ອງໃຊ້ vector ສະເໝີໄປ — ສຳລັບເອກະສານທີ່ມີໂຄງສ້າງ, ການໃຫ້ LLM "ຄິດ" ຄົ້ນຫາ ອາດຖືກກວ່າ ແລະ ອະທິບາຍໄດ້ດີກວ່າ.

👉 ທ່ານຢາກລອງ PageIndex ກັບເອກະສານປະເພດໃດ? ສັນຍາ, ບົດລາຍງານ ຫຼື ກົດໝາຍ? ມາຄຸຍກັນ! 💬

#arnfar #PageIndex #RAG #VectorlessRAG #LaoTech

## (copy to here ↑)

---

## Sources
- PageIndex: Document Index for Vectorless, Reasoning-based RAG — VectifyAI (GitHub) — https://github.com/VectifyAI/PageIndex
- Mafin 2.5 FinanceBench evaluation — VectifyAI (GitHub) — https://github.com/VectifyAI/Mafin2.5-FinanceBench
- PageIndex: The RAG Framework That Threw Out Vector Databases and Still Hit 98.7% Accuracy — Towards AI — https://pub.towardsai.net/pageindex-the-rag-framework-that-threw-out-vector-databases-and-still-hit-98-7-accuracy-d194e0549478
- Vectorless RAG: How PageIndex Works (2026 Guide) — Build Fast with AI — https://www.buildfastwithai.com/blogs/vectorless-rag-pageindex-guide

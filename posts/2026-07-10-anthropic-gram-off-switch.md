# Anthropic ສ້າງ "ສະວິດປິດ" ຄວາມຮູ້ອັນຕະລາຍໃນ AI — ຖອດອອກໄດ້ໂດຍບໍ່ກະທົບຄວາມສະຫຼາດ

## POST (copy from here ↓)

— — — [ English Below ⬇️ ] — — —

🔒🧠 ຂ່າວໃຫຍ່ດ້ານຄວາມປອດໄພ AI! Anthropic ຫາກໍເປີດເຜີຍວິທີໃໝ່ຊື່ GRAM — ຄ້າຍ "ສະວິດປິດ" ທີ່ຖອດຄວາມຮູ້ອັນຕະລາຍ (ເຊັ່ນ ໄວຣັດ, ອາວຸດ) ອອກຈາກ AI ໄດ້ ໂດຍບໍ່ເຮັດໃຫ້ AI ໂງ່ລົງ ⚡️🇱🇦

ສະບາຍດີຊາວ Arnfar! ວັນທີ 8 ກໍລະກົດ 2026 ບໍລິສັດ Anthropic (ຜູ້ສ້າງ Claude) ຮ່ວມກັບ AE Studio ໄດ້ເປີດເຜີຍງານຄົ້ນຄວ້າໃໝ່ ວ່າດ້ວຍວິທີ "ຄວບຄຸມ" ຄວາມຮູ້ແບບໃຊ້ໄດ້ສອງທາງ (dual-use) ໃນ AI. dual-use ໝາຍເຖິງຄວາມຮູ້ທີ່ໃຊ້ໄດ້ທັງທາງດີ ແລະ ທາງຮ້າຍ — ຕົວຢ່າງ ຄວາມຮູ້ດ້ານໄວຣັດວິທະຍາ (virology) ຊ່ວຍສ້າງວັກຊິນກໍໄດ້ ຫຼື ຊ່ວຍຄົນຮ້າຍອອກແບບເຊື້ອພະຍາດກໍໄດ້. ນີ້ເປັນເລື່ອງທີ່ຄົນລາວທີ່ສົນໃຈ AI ຄວນຮູ້ ເພາະມັນແຕະບັນຫາ "ຈະໃຫ້ AI ເກັ່ງ ແຕ່ບໍ່ອັນຕະລາຍ ໄດ້ແນວໃດ".

🔍 ມັນເກີດຫຍັງຂຶ້ນ?
ອີງຕາມ Anthropic, ວິທີໃໝ່ນີ້ຊື່ GRAM (Gradient-Routed Auxiliary Modules). ແທນທີ່ຈະຝຶກ AI ຫຼາຍໂຕເພື່ອແຍກຄວາມສາມາດ (ຊຶ່ງແພງຫຼາຍ) GRAM ໃສ່ "ຫ້ອງເກັບຄວາມຮູ້" ແຍກໄວ້ໃນ AI ໂຕດຽວ ແລ້ວຖອດອອກເມື່ອຕ້ອງການ:
• ເພີ່ມ neuron ພິເສດເຂົ້າທຸກຊັ້ນຂອງໂມເດລ ແລ້ວແບ່ງເປັນ "module" ໜຶ່ງ module ຕໍ່ໜຶ່ງໝວດຄວາມຮູ້ອັນຕະລາຍ
• ເມື່ອ AI ຮຽນຈາກຂໍ້ມູນ dual-use ຈະໃຫ້ສະເພາະ module ນັ້ນ "ຈື່" ສ່ວນສະໝອງຫຼັກຖືກ freeze ໄວ້ — ຄວາມຮູ້ຈຶ່ງບໍ່ກະຈາຍໄປທົ່ວເຄືອຂ່າຍ
• ຢາກປິດຄວາມສາມາດໃດ ກໍລຶບ module ນັ້ນຖິ້ມ ຄືກັບວ່າ AI ບໍ່ເຄີຍຮຽນເລື່ອງນັ້ນມາກ່ອນ; ຢາກເປີດໃຫ້ນັກຄົ້ນຄວ້າທີ່ເຊື່ອຖືໄດ້ ກໍໃສ່ຄືນ
• ໃນການທົດລອງໃຊ້ 4 ໝວດ (ໄວຣັດວິທະຍາ, ຄວາມປອດໄພໄຊເບີ, ຟີຊິກນິວເຄຼຍ ແລະ ພາສາຂຽນໂປຣແກຣມສະເພາະ) ຝຶກເທື່ອດຽວ ແຕ່ຕັ້ງຄ່າໄດ້ເຖິງ 16 ແບບ (ເປີດ/ປິດ ແຕ່ລະໝວດ)
• ທົດສອບໃນໂມເດລ 7 ຂະໜາດ ຕັ້ງແຕ່ 50 ລ້ານ ຫາ 5 ຕື້ພາຣາມິເຕີ — ຖອດ module ອອກ ລົບຄວາມສາມາດອັນຕະລາຍໄດ້ ໂດຍປະສິດທິພາບລວມຂອງ AI ບໍ່ຫຼຸດລົງ
• Anthropic ລະບຸວ່າ GRAM ທົນທານຕໍ່ການ "ຝຶກກັບຄືນ" ຂອງຄົນຮ້າຍໄດ້ດີກວ່າວິທີ unlearning ທີ່ພຽງແຕ່ກົດຄວາມຮູ້ໄວ້ (ຍັງ fine-tune ດຶງກັບມາໄດ້ງ່າຍ)

✅ ຂໍ້ດີ
✅ ຄວບຄຸມຄວາມສ່ຽງໄດ້ຕົງຈຸດ — ຖອດສະເພາະຄວາມຮູ້ອັນຕະລາຍ ໂດຍບໍ່ເຮັດໃຫ້ AI ໂງ່ລົງ ຫຼື ຕອບຄຳຖາມທຳມະດາບໍ່ໄດ້
✅ ປະຢັດຕົ້ນທຶນ — ຝຶກ AI ເທື່ອດຽວ ໄດ້ຫຼາຍລຸ້ນ ແທນທີ່ຈະຝຶກຫຼາຍໂຕທີ່ແພງ
✅ ຢືດຢຸ່ນ — ຫ້ອງແລັບ ຫຼື ນັກຄົ້ນຄວ້າທີ່ໄດ້ຮັບການກວດສອບ ຍັງໃຊ້ຄວາມຮູ້ເຕັມໄດ້ ສ່ວນຄົນທົ່ວໄປໃຊ້ລຸ້ນທີ່ຖອດຄວາມສ່ຽງອອກ
✅ ທົນທານກວ່າ jailbreak ແລະ unlearning — ຄວາມຮູ້ຖືກ "ລຶບ" ບໍ່ແມ່ນພຽງແຕ່ "ເຊື່ອງ"

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ຍັງເປັນງານຄົ້ນຄວ້າຂັ້ນຕົ້ນ — Anthropic ຍັງບໍ່ໄດ້ນຳໄປໃຊ້ໃນ Claude ຕົວຈິງ ແລະ ບໍ່ແນ່ໃຈວ່າຈະໃຊ້ຫຼືບໍ່
❌ ຍັງບໍ່ໄດ້ທົດສອບໃນລະດັບໂມເດລໃຫຍ່ສຸດ (frontier) ຫຼື ໃນສາຍການຝຶກຈິງ
❌ ຄວາມຮູ້ບາງຢ່າງພົວພັນກັນແໜ້ນ (ເຊັ່ນ ຊີວະວິທະຍາທົ່ວໄປ ກັບ ໄວຣັດອັນຕະລາຍ) — ອາດແຍກອອກຈາກກັນຍາກ
❌ ວັດແທກຜົນຈາກການ "ທາຍຄຳຕໍ່ໄປ" ຍັງບໍ່ແມ່ນການທົດສອບໃນວຽກຈິງ

📌 ສະຫຼຸບ: GRAM ຄື "ສະວິດປິດ" ຄວາມຮູ້ອັນຕະລາຍໃນ AI ໂຕດຽວ — ຖອດອອກ ຫຼື ໃສ່ຄືນໄດ້ຕາມການນຳໃຊ້ ໂດຍບໍ່ກະທົບຄວາມສະຫຼາດ; ແຕ່ຍັງເປັນຂັ້ນທົດລອງ ຍັງບໍ່ໄດ້ໃຊ້ຈິງ.

👉 ທ່ານຄິດວ່າ AI ຄວນມີ "ສະວິດປິດ" ຄວາມຮູ້ອັນຕະລາຍແບບນີ້ບໍ? ມາແບ່ງປັນຄວາມເຫັນ! 💬

🔒🧠 Big AI-safety news! Anthropic just unveiled GRAM — essentially an "off switch" that can strip dangerous, dual-use knowledge (think viruses, weapons) out of an AI without making it any dumber ⚡️🇱🇦

Hey Arnfar community! On July 8, 2026, Anthropic (the makers of Claude), together with AE Studio, published new research on how to *control* dual-use knowledge inside an AI. "Dual-use" means knowledge that cuts both ways — virology can help design vaccines, or help a bad actor engineer a pathogen. If you follow AI, this one matters, because it goes straight at the hardest question in the field: how do you keep an AI capable but not dangerous?

🔍 What actually happened
According to Anthropic, the method is called GRAM (Gradient-Routed Auxiliary Modules). Instead of training several separate models to wall off risky skills (which is expensive), GRAM tucks that knowledge into removable "compartments" inside a single model:
• It adds extra neurons to each layer of the model, grouped into a "module" — one module per dangerous knowledge category
• When the model learns from dual-use data, only that module "remembers" it; the main network is frozen — so the knowledge never spreads across the whole system
• Want a capability gone? Delete its module and the model behaves as if it never learned the topic. Want to grant it to a vetted researcher? Add the module back
• Tested across 4 categories (virology, cybersecurity, nuclear physics, and a niche programming language) — trained once, but configurable up to 16 ways (each category on/off)
• Tried on 7 model sizes from 50 million to 5 billion parameters — removing a module erased the dangerous capability while overall performance stayed intact
• Anthropic says GRAM holds up against adversarial fine-tuning far better than "unlearning" methods, which only suppress knowledge that can still be coaxed back

✅ Pros
✅ Precise risk control — remove only the dangerous knowledge, without making the AI dumber or unable to answer normal questions
✅ Cost-effective — train once and get many variants, instead of training multiple expensive models
✅ Flexible — vetted labs or researchers keep full access, while public deployments ship with the risky module removed
✅ More robust than jailbreaks and unlearning — the knowledge is "deleted," not merely "hidden"

❌ Cons / Watch-outs
❌ Still early-stage research — Anthropic hasn't applied it to production Claude and hasn't committed to doing so
❌ Not yet tested at the largest (frontier) scale or in a real training pipeline
❌ Some knowledge is deeply entangled (e.g. general biology vs. dangerous virology) — hard to cleanly separate
❌ Results come from "next-token prediction" tests, not real-world task evaluations

📌 Bottom line: GRAM is an "off switch" for dangerous knowledge inside a single AI — remove it or add it back depending on who's using the model, without hurting its intelligence — but it's still experimental, not deployed.

👉 Do you think AI should have an "off switch" like this for dangerous knowledge? Share your take! 💬

#arnfar #Anthropic #AISafety #Claude #AInews

## (copy to here ↑)

---

## Sources
- An off switch for dual-use knowledge in AI models — Anthropic — https://www.anthropic.com/research/off-switch-dual-use
- Modular pretraining (Alignment Science blog) — Anthropic — https://alignment.anthropic.com/2026/modular-pretraining/
- Anthropic Research Introduces GRAM For Isolating Dangerous AI Knowledge — Dataconomy — https://dataconomy.com/2026/07/09/anthropic-gram-method-isolate-dangerous-ai-knowledge/

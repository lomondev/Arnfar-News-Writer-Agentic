# ວິທີສ້າງ Skill ໃຫ້ Claude — ສິ່ງທີ່ຕ້ອງຮູ້

## POST (copy from here ↓)

🛠️🤖 ຢາກໃຫ້ Claude ເຮັດວຽກແບບ "ມືອາຊີບສະເພາະດ້ານ" ຂອງທ່ານບໍ? ສ້າງ Skill ເອງໄດ້ ດ້ວຍໄຟລ໌ Markdown ໄຟລ໌ດຽວ! ⚡️

ສະບາຍດີຊາວ Arnfar! ຕອນນີ້ Anthropic ເປີດໃຫ້ທຸກຄົນສ້າງ "Agent Skills" — ຊຸດຄຳສັ່ງ + ສະຄຣິບ ທີ່ສອນ Claude ໃຫ້ຮູ້ວິທີເຮັດວຽກສະເພາະຂອງເຮົາ ເຊັ່ນ ຂຽນລາຍງານຕາມຟອມບໍລິສັດ, ສ້າງເອກະສານ, ຫຼື ໂພສ Facebook ຕາມແບຣນ. ໃຊ້ໄດ້ທັງ Claude.ai, Claude Code ແລະ API — ສ້າງເທື່ອດຽວ ໃຊ້ໄດ້ທຸກບ່ອນ 🇱🇦

🔍 ວິທີສ້າງ Skill — ຫຼັກການສຳຄັນ
ອີງຕາມເອກະສານທາງການຂອງ Anthropic, Skill ໜຶ່ງແມ່ນ folder ທີ່ມີໄຟລ໌ SKILL.md ເປັນຫົວໃຈ:
• ເລີ່ມດ້ວຍ YAML frontmatter: `name` (ຕົວພິມນ້ອຍ + ຂີດກາງ, ບໍ່ເກີນ 64 ຕົວອັກສອນ) ແລະ `description` (ບໍ່ເກີນ 1,024 ຕົວອັກສອນ)
• `description` ສຳຄັນທີ່ສຸດ — ຕ້ອງບອກທັງ "ເຮັດຫຍັງ" ແລະ "ໃຊ້ຕອນໃດ" ເພາະ Claude ໃຊ້ມັນຕັດສິນວ່າຈະເອີ້ນ Skill ນີ້ຫຼືບໍ່
• ເນື້ອໃນແມ່ນຄຳແນະນຳເປັນຂັ້ນຕອນ + ຕົວຢ່າງ input/output — ຄວນສັ້ນກວ່າ 500 ແຖວ ຖ້າຍາວກວ່ານັ້ນ ໃຫ້ແຍກເປັນໄຟລ໌ອ້າງອີງ (ເຊັ່ນ REFERENCE.md)
• ລະບົບເຮັດວຽກແບບ "Progressive Disclosure" 3 ຊັ້ນ: Claude ໂຫຼດແຕ່ name/description ກ່ອນ (~100 token), ອ່ານ SKILL.md ເຕັມເມື່ອຈຳເປັນ, ແລະ ເປີດໄຟລ໌ເສີມ/ສະຄຣິບ ສະເພາະຕອນໃຊ້ແທ້ — ປະຢັດ context ຫຼາຍ
• ອັບໂຫຼດງ່າຍ: zip folder ແລ້ວໄປທີ່ Customize > Skills ໃນ Claude.ai ຫຼື ໃຊ້ skill-creator ໃຫ້ Claude ຊ່ວຍສ້າງ Skill ໃຫ້ເລີຍ

✅ ຂໍ້ດີ
✅ ບໍ່ຕ້ອງຂຽນໂປຣແກຣມກໍສ້າງໄດ້ — ແກ່ນຫຼັກແມ່ນ Markdown ທຳມະດາ
✅ ສ້າງເທື່ອດຽວ ໃຊ້ໄດ້ທັງ Claude.ai, Claude Code ແລະ API ໂດຍບໍ່ຕ້ອງແກ້
✅ ປະຢັດ token — Skill ຖືກໂຫຼດເຂົ້າ context ສະເພາະຕອນຈຳເປັນເທົ່ານັ້ນ
✅ ເໝາະສຳລັບທຸລະກິດລາວ: ຝັງຟອມເອກະສານ, ສູດຄິດໄລ່, ຫຼື ສະຕາຍແບຣນ ໃຫ້ທີມໃຊ້ຮ່ວມກັນ

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ຕ້ອງເປີດ code execution ກ່ອນ Skill ຈຶ່ງເຮັດວຽກໄດ້
❌ ຖ້າຂຽນ description ບໍ່ຊັດເຈນ Claude ອາດບໍ່ເອີ້ນ Skill ຕອນທີ່ຄວນ — ຕ້ອງທົດສອບ ແລະ ປັບແກ້ເລື້ອຍໆ
❌ Skill ສາມາດແລ່ນສະຄຣິບໄດ້ — ຕິດຕັ້ງສະເພາະ Skill ຈາກແຫຼ່ງທີ່ເຊື່ອຖືໄດ້ເທົ່ານັ້ນ

📌 ສະຫຼຸບ: Skill ແມ່ນວິທີປ່ຽນ Claude ຈາກ "ຜູ້ຊ່ວຍທົ່ວໄປ" ໃຫ້ກາຍເປັນ "ພະນັກງານທີ່ຮູ້ວຽກຂອງເຮົາ" — ເລີ່ມຈາກໄຟລ໌ Markdown ໄຟລ໌ດຽວ.

👉 ທ່ານຢາກສ້າງ Skill ຫຍັງເປັນອັນທຳອິດ? ມາແບ່ງປັນໄອເດຍກັນ! 💬

#arnfar #ClaudeSkills #AIAgent #LaoDev #Anthropic

## (copy to here ↑)

---

## Sources
- Agent Skills overview — Claude Platform Docs — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Skill authoring best practices — Claude Platform Docs — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- How to create custom skills — Claude Help Center — https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- Use skills in Claude — Claude Help Center — https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Equipping agents for the real world with Agent Skills — Anthropic Engineering — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

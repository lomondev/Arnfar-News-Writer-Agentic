# ເຄື່ອງມືບໍລິຫານໂຄງການແບບ Open Source ແທນ Jira

## POST (copy from here ↓)

📋 ເຄື່ອງມືບໍລິຫານໂຄງການແບບ Open Source ແທນ Jira ກຳລັງມາແຮງ — ຕິດຕັ້ງເທິງ server ຂອງຕົນເອງໄດ້ ແລະ ເລີ່ມໃຊ້ໄດ້ຟຣີ!

Plane, ໂປຣແກຣມບໍລິຫານໂຄງການແບບ Open Source ທີ່ຖືກສ້າງຂຶ້ນມາແທນ Jira, Linear ແລະ ClickUp, ໄດ້ຮັບຫຼາຍກວ່າ 55,000 ດາວ (stars) ເທິງ GitHub ແລະ ຂຶ້ນ GitHub Trending ເມື່ອເດືອນສິງຫາ 2026. ໃນຂະນະດຽວກັນ OpenProject ກໍອອກເວີຊັນ 17.6 ແລະ ມີເຄື່ອງມືຍ້າຍຂໍ້ມູນຈາກ Jira ໂດຍກົງ.

ເປັນຫຍັງຈຶ່ງໄດ້ຮັບຄວາມສົນໃຈຫຼາຍ? Atlassian ຈະຢຸດຊ່ວຍເຫຼືອ Jira ແລະ Confluence ແບບຕິດຕັ້ງເອງ (Data Center) ພາຍໃນເດືອນມີນາ 2029. ອົງກອນທີ່ຕ້ອງການເກັບຂໍ້ມູນໄວ້ເທິງ server ຂອງຕົນເອງ ຈຶ່ງເລີ່ມຊອກຫາທາງເລືອກໃໝ່ຕັ້ງແຕ່ຕອນນີ້.

ເຄື່ອງມືທີ່ຄວນຮູ້ຈັກ:
• Plane (AGPL-3.0): ແທນ Jira ແລະ Linear. ມີ work item, cycle (sprint) ພ້ອມກຣາຟ burn-down, module, ໜ້າເອກະສານ ແລະ ການວິເຄາະຂໍ້ມູນ. ຕິດຕັ້ງໄດ້ດ້ວຍ Docker ຫຼື Kubernetes.
• OpenProject 17.6 (ອອກວັນທີ 8 ກໍລະກົດ 2026): ເພີ່ມເປົ້າໝາຍຂອງ sprint, ໜ້າລວມ sprint ທັງໝົດ, ເຊື່ອມກັບ XWiki ແລະ ປ່ຽນຫົວຂໍ້ປະຊຸມເປັນໜ້າວຽກໄດ້. ມີ Jira Migrator ທີ່ນຳເຂົ້າໂຄງການ, issue, ຜູ້ໃຊ້ ແລະ custom field ພື້ນຖານຈາກ Jira Server/Data Center.
• Vikunja 1.0 (ອອກວັນທີ 27 ມັງກອນ 2026): ເໝາະກັບທີມນ້ອຍ — ລາຍການວຽກ, Kanban, Gantt chart, ເຂົ້າລະບົບດ້ວຍ LDAP/OpenID ແລະ ເກັບໄຟລ໌ເທິງ S3 ໄດ້.
• Huly (EPL-2.0): ລວມ tracker, ເອກະສານ, chat, ການໂທ ແລະ ແຜນວຽກໄວ້ໃນບ່ອນດຽວ, ແທນ Jira, Notion ແລະ Slack ໄປພ້ອມກັນ.

ແຕ່ຕ້ອງລະວັງ: ການຕິດຕັ້ງເອງໝາຍເຖິງວຽກດູແລລະບົບເອງ — ອັບເດດ, backup ແລະ ແກ້ໄຂບັນຫາຄວາມປອດໄພ. Huly ຕ້ອງການ server ຢ່າງໜ້ອຍ 2 vCPU ແລະ RAM 8 GB (ແນະນຳ 4 vCPU ແລະ 16 GB). ການຍ້າຍຈາກ Jira ກໍບໍ່ງ່າຍ: Jira Migrator ຂອງ OpenProject ຍັງບໍ່ຍ້າຍ workflow ແລະ ສິດການເຂົ້າເຖິງ, ສ່ວນ Plane ແລະ OpenProject ມີບາງຄວາມສາມາດຢູ່ໃນເວີຊັນເສຍເງິນ.

ທາງເລືອກທີ່ເໝາະກັບແຕ່ລະທີມ:
• ທີມພັດທະນາ software → Plane
• ອົງກອນ ແລະ ໂຄງການຂະໜາດໃຫຍ່ → OpenProject
• ທີມນ້ອຍ ຫຼື ວຽກສ່ວນຕົວ → Vikunja
• ຢາກໄດ້ທຸກຢ່າງໃນບ່ອນດຽວ ແລະ ມີ server ພຽງພໍ → Huly
• ທົດລອງກັບໂຄງການດຽວກ່ອນ, ກວດການສະແດງຜົນພາສາລາວ ແລະ ວາງແຜນ backup ໃຫ້ຊັດເຈນ ກ່ອນຍ້າຍທັງອົງກອນ

📌 ສະຫຼຸບ: ເຄື່ອງມືບໍລິຫານໂຄງການແບບ Open Source ມີຄຸນນະພາບສູງຂຶ້ນຫຼາຍ ແລະ ຊ່ວຍໃຫ້ອົງກອນຄວບຄຸມຂໍ້ມູນຂອງຕົນເອງໄດ້, ແຕ່ຕ້ອງມີຄົນດູແລລະບົບ ແລະ ວາງແຜນການຍ້າຍໃຫ້ດີ.
👉 ທີມຂອງທ່ານໃຊ້ເຄື່ອງມືຫຍັງບໍລິຫານໂຄງການຢູ່? ເຄີຍລອງ Plane ຫຼື OpenProject ແລ້ວບໍ? 💬

ຕິດຕາມເພຈ Arnfar ເພື່ອອັບເດດຂ່າວເຕັກໂນໂລຊີ ແລະ ເຄື່ອງມືໃໝ່ໆ ທຸກມື້.

#arnfar #OpenSource #ProjectManagement #Plane

## (copy to here ↑)

---

## Sources
- makeplane/plane — GitHub — https://github.com/makeplane/plane
- Plane hit GitHub Trending — remio — https://www.remio.ai/post/makeplane-plane-hit-github-trending-but-the-real-test-starts-after-the-stars
- OpenProject 17.6.0 release notes — OpenProject — https://www.openproject.org/docs/release-notes/17-6-0/
- Atlassian Data Center alternative (Jira Migrator, DC ending 2029) — OpenProject — https://www.openproject.org/alternative-atlassian-jira-data-center/
- What's new in Vikunja 1.0.0 — Vikunja — https://vikunja.io/changelog/whats-new-in-vikunja-1.0.0/
- Self-host Huly — Elestio — https://blog.elest.io/self-host-huly-one-open-source-app-to-replace-jira-linear-and-notion/

## POST (copy from here ↓)

⚙️🦀 ຢາກໃຫ້ statusline ຂອງ Claude Code ໄວ ແລະ ບອກຂໍ້ມູນຄົບ? ລອງ CCometixLine — ຂຽນດ້ວຍ Rust 🇱🇦

ສະບາຍດີຊາວ Arnfar! ມື້ນີ້ພາມາຮູ້ຈັກ CCometixLine (ຄຳສັ່ງ: ccline) — ເຄື່ອງມື statusline ປະສິດທິພາບສູງສຳລັບ Claude Code, ຂຽນດ້ວຍພາສາ Rust (96% ຂອງໂຄ້ດ), ໃບອະນຸຍາດ MIT, ໄດ້ດາວເຖິງ 3.1k ດາວໃນ GitHub. ມັນສະແດງ Model · Directory · Git · Context Window ໄວ້ໃນແຖບດຽວ.

🔍 ມັນແມ່ນຫຍັງ ແລະ ເຮັດວຽກແນວໃດ?
statusline ຄືແຖບຂໍ້ມູນທີ່ Claude Code ເອີ້ນຂຶ້ນມາ render ໃໝ່ທຸກໆ turn. ການຂຽນດ້ວຍ Rust (binary native, ບໍ່ມີ runtime) ເຮັດໃຫ້ມັນ render ໄດ້ໄວ ແລະ ກິນ resource ໜ້ອຍ. ມັນອ່ານ context ຈາກ Claude Code ຜ່ານ stdin (JSON) ແລ້ວວິເຄາະ:
• Git: branch, ສະຖານະ (✓ clean · ● dirty · ⚠ conflict), tracking (↑n ahead · ↓n behind)
• Model: ຫຍໍ້ຊື່ ເຊັ່ນ claude-4-sonnet → "Sonnet 4"
• Context Window: % ການໃຊ້ token ຈາກການວິເຄາະ transcript
• ໃຊ້ Nerd Font icons — ຕ້ອງຕັ້ງ terminal ໃຫ້ໃຊ້ Nerd Font ກ່ອນ

🛠️ ວິທີຕິດຕັ້ງ & ຕັ້ງຄ່າ
• ຕິດຕັ້ງ: npm install -g @cometix/ccline (ຫຼື ໂຫຼດ binary ຈາກ Releases)
• ເພີ່ມໃນ settings.json ຂອງ Claude Code:
 "statusLine": { "type": "command", "command": "~/.claude/ccline/ccline", "padding": 0 }
• ເປີດ TUI ຕັ້ງຄ່າ (preview ສົດ): ccline -c
• ສ້າງ config ເລີ່ມຕົ້ນ: ccline --init → ~/.claude/ccline/config.toml
• ປ່ຽນ theme: ccline --theme nord (ມີ cometix · minimal · gruvbox · nord · powerline-dark)
• Segments ທີ່ຮອງຮັບ: Directory · Git · Model · Usage · Time · Cost · OutputStyle (ເປີດ/ປິດ ແລະ ປັບສີ/icon ໄດ້ລາຍ segment)

✅ ຂໍ້ດີ
✅ Rust native binary — render ໄວ, ກິນ RAM/CPU ໜ້ອຍກວ່າ statusline ທີ່ໃຊ້ Node
✅ ຕັ້ງຄ່າຄົບ ຜ່ານ TOML + TUI ທີ່ preview ໄດ້ສົດ, ມີ theme ສຳເລັດຮູບ
✅ models.toml ກຳນົດ context_limit ເອງໄດ້ — ຮອງຮັບໂມເດລ third-party (GLM, Kimi)
✅ ມີ utility ປິດຂໍ້ຄວາມ "Context low" + verbose mode (patch cli.js, backup ໃຫ້ອັດຕະໂນມັດ)
✅ Cross-platform: Windows · macOS · Linux (static binary ໃຊ້ໄດ້ທຸກ distro)

❌ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ
❌ ຕ້ອງມີ Nerd Font ໃນ terminal — ບໍ່ດັ່ງນັ້ນ icon ຈະເພ້ຍນ
❌ ການ --patch cli.js ແກ້ໄຟລ໌ພາຍໃນ Claude Code — ມີຄວາມສ່ຽງເມື່ອ CC ອັບເດດ (ເຖິງຈະມີ backup)
❌ Git ຕ້ອງ 1.5+ (ແນະນຳ 2.22+) ສຳລັບການກວດ branch ໃຫ້ຖືກຕ້ອງ
❌ ບາງ feature ຕ້ອງເຂົ້າໃຈ TOML ໜ້ອຍໜຶ່ງ — ບໍ່ແມ່ນ GUI ລ້ວນ

📌 ສະຫຼຸບ: CCometixLine ເໝາະກັບຄົນທີ່ໃຊ້ Claude Code ໜັກ ແລະ ຢາກໄດ້ statusline ທີ່ໄວ, ບອກ Git + context % ຄົບ, ແລະ ປັບແຕ່ງໄດ້ເລິກ — ທັງໝົດດ້ວຍ binary Rust ດຽວ.

👉 ທ່ານໃຊ້ statusline ແບບໃດກັບ Claude Code ຢູ່ປະຈຸບັນ? ມາແບ່ງປັນ setup ກັນ! 💬

#arnfar #ClaudeCode #Rust #DevTools #LaoDev

## (copy to here ↑)

---

## Sources
- Haleclipse/CCometixLine — GitHub (README, v1.1.2) — https://github.com/Haleclipse/CCometixLine
- @cometix/ccline — npm — https://www.npmjs.com/package/@cometix/ccline
- CCometixLine Releases — GitHub — https://github.com/Haleclipse/CCometixLine/releases

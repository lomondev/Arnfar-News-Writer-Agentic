# ໂປຣແກຣມແທນ Photoshop ແລະ Illustrator ແບບ Open Source

## POST (copy from here ↓)

🎨 ໂປຣແກຣມແທນ Photoshop ແລະ Illustrator ແບບ Open Source ກຳລັງມາແຮງ — ໃຊ້ໄດ້ຟຣີ ບໍ່ຕ້ອງຈ່າຍລາຍເດືອນ!

ຕົ້ນເດືອນຕຸລາ 2026, ນັກພັດທະນາ Brandon Thomas ຈາກ ArtCraft ໄດ້ເປີດຕົວໂປຣແກຣມ 7 ຕົວ ທີ່ສ້າງຂຶ້ນມາແທນຊຸດໂປຣແກຣມຂອງ Adobe, ລວມທັງ PhotoCraft (ແທນ Photoshop) ແລະ VectorCraft (ແທນ Illustrator). ທັງໝົດເປັນ Open Source ຂຽນດ້ວຍພາສາ Rust ໂດຍມີ AI ຊ່ວຍຂຽນໂຄດເປັນສ່ວນໃຫຍ່. ພາຍໃນບໍ່ເທົ່າໃດມື້, PhotoCraft ໄດ້ຮັບປະມານ 43,000 ດາວ (stars) ເທິງ GitHub.

ເປັນຫຍັງຈຶ່ງໄດ້ຮັບຄວາມສົນໃຈຫຼາຍ? ຄ່າບໍລິການຂອງ Adobe ສູງຂຶ້ນເລື້ອຍໆ: ແພັກເກດ Photography (Photoshop + Lightroom) ຂຶ້ນຈາກ 9.99 USD ເປັນ 14.99 USD ຕໍ່ເດືອນ (ເພີ່ມຂຶ້ນ 50%), ສ່ວນ Photoshop ຢ່າງດຽວແມ່ນ 22.99 USD ຕໍ່ເດືອນ. ນັກອອກແບບ ແລະ ທຸລະກິດຂະໜາດນ້ອຍຈຶ່ງຊອກຫາທາງເລືອກທີ່ບໍ່ຕ້ອງຈ່າຍລາຍເດືອນ.

ເຄື່ອງມືທີ່ຄວນຮູ້ຈັກ:
• GIMP 3.2 (ອອກວັນທີ 14 ມີນາ 2026): ແທນ Photoshop ສຳລັບງານແຕ່ງຮູບ. ເພີ່ມ layer ແບບບໍ່ທຳລາຍຕົ້ນສະບັບ (non-destructive), vector layer, link layer ທີ່ຄ້າຍກັບ Smart Object ແລະ ເຮັດວຽກກັບໄຟລ໌ Photoshop ໄດ້ດີຂຶ້ນ.
• Krita 6.0 (ອອກວັນທີ 24 ມີນາ 2026): ເໝາະກັບງານແຕ້ມຮູບ ແລະ illustration. ມີເຄື່ອງມືຂໍ້ຄວາມໃໝ່ທີ່ຮອງຮັບ OpenType, ຮອງຮັບ HDR ແລະ ເປີດໄຟລ໌ PSD ໄດ້ດີຂຶ້ນ.
• Inkscape 1.4: ແທນ Illustrator ສຳລັບງານ vector (SVG) ເຊັ່ນ ໂລໂກ້ ແລະ ໂປສເຕີ. ເວີຊັນ 1.4.3 ແກ້ໄຂບັນຫາ 124 ຈຸດ ແລະ ນຳເຂົ້າໄຟລ໌ PDF ໄດ້ດີຂຶ້ນ.
• PhotoCraft / VectorCraft (ArtCraft): ໃບອະນຸຍາດ MIT / Apache-2.0, ໃຊ້ໄດ້ທັງ Windows, macOS, Linux ແລະ ເທິງ browser.

ແຕ່ຕ້ອງລະວັງ: ໂປຣແກຣມຂອງ ArtCraft ຍັງເປັນເວີຊັນທົດລອງ (alpha), ມີລາຍງານວ່າຍັງມີຂໍ້ຜິດພາດ ແລະ ເຄື່ອງມືບາງຢ່າງເຮັດວຽກບໍ່ສະໝ່ຳສະເໝີ. ຕົວເລກທີ່ອ້າງວ່າເປີດ ແລະ ບັນທຶກໄຟລ໌ PSD ໄດ້ 134 ຈາກ 135 ໄຟລ໌ ແມ່ນທີມງານລະບຸເອງ ແລະ ຍັງບໍ່ມີການກວດສອບຈາກພາຍນອກ. ຖ້ານຳໄປໃຊ້ກັບວຽກລູກຄ້າໂດຍບໍ່ທົດສອບກ່ອນ, layer, effect ຫຼື ສີ ອາດຜິດພ້ຽນໄດ້.

ທາງເລືອກທີ່ເໝາະກັບແຕ່ລະວຽກ:
• ງານແຕ່ງຮູບ → GIMP 3.2
• ງານແຕ້ມຮູບ ແລະ illustration → Krita 6.0
• ໂລໂກ້ ແລະ ງານ vector → Inkscape
• PhotoCraft ແລະ VectorCraft: ຕິດຕາມ ແລະ ທົດລອງໄປກ່ອນ, ຍັງບໍ່ຄວນໃຊ້ກັບວຽກທີ່ຕ້ອງສົ່ງລູກຄ້າ
• ກ່ອນສົ່ງໄຟລ໌ໃຫ້ໂຮງພິມ ຫຼື ລູກຄ້າ: ກວດສີ ແລະ ຟອນລາວໃຫ້ຖືກຕ້ອງທຸກຄັ້ງ

📌 ສະຫຼຸບ: ໂປຣແກຣມອອກແບບແບບຟຣີມີຄຸນນະພາບດີຂຶ້ນຫຼາຍ ແລະ ໃຊ້ແທນ Adobe ໄດ້ໃນຫຼາຍວຽກແລ້ວ, ແຕ່ການເລືອກໃຫ້ເໝາະກັບວຽກ ແລະ ການທົດສອບກ່ອນໃຊ້ຈິງ ຍັງເປັນສິ່ງສຳຄັນ.
👉 ທ່ານໃຊ້ໂປຣແກຣມຫຍັງແຕ່ງຮູບ ແລະ ອອກແບບຢູ່? ເຄີຍລອງ GIMP, Krita ຫຼື Inkscape ແລ້ວບໍ? 💬

ຕິດຕາມເພຈ Arnfar ເພື່ອອັບເດດຂ່າວເຕັກໂນໂລຊີ ແລະ ເຄື່ອງມືໃໝ່ໆ ທຸກມື້.

#arnfar #OpenSource #GIMP #Inkscape

## (copy to here ↑)

---

## Sources
- ArtCraft Adobe alternatives in Rust — Gadget Pilipinas — https://www.gadgetpilipinas.net/2026/10/artcraft-adobe-alternatives-rust/
- ArtCraft: the free open-source Adobe suite that racked up 43,000 stars — LinuxCompatible — https://www.linuxcompatible.org/story/artcraft-the-free-opensource-adobe-suite-that-racked-up-43000-stars-in-days/
- GIMP 3.2 Released — Phoronix — https://www.phoronix.com/news/GIMP-3.2-Released
- GIMP 3.2 with vector and link layers — CG Channel — https://www.cgchannel.com/tag/acv
- Krita 6.0 Released — Phoronix — https://www.phoronix.com/news/Krita-6.0-Released
- Inkscape 1.4.3 delivers 124 bug and crash fixes — Linuxiac — https://linuxiac.com/inkscape-1-4-3-vector-graphic-editor-delivers-124-bug-and-crash-fixes/

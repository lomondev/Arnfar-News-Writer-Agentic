# PHP2Shell: PHP ອອກແພັດດ່ວນ ປິດຊ່ອງໂຫວ່ຮ້າຍແຮງ 2 ຈຸດ

Slot: 2026-10-22 morning (posted after the 08:00 slot), written on Lomon's request
Image: output/cards/php2shell-critical-patch/arnfar-php2shell-critical-patch-facebook.png
TikTok title: ເວັບໄຊທີ່ໃຊ້ PHP ຕ້ອງອັບເດດດ່ວນ

## POST (copy from here ↓)
ຖ້າທ່ານມີເວັບໄຊ ໂດຍສະເພາະເວັບ WordPress ມື້ນີ້ຄວນຖາມທີມ IT ຫຼື ເຈົ້າຂອງໂຮສຕິ້ງໄວ້ຈັກຄຳ: ອັບເດດ PHP ແລ້ວບໍ?

ເມື່ອວັນທີ 21 ຕຸລາ ທີມພັດທະນາ PHP ອອກແພັດຄວາມປອດໄພແບບດ່ວນ ເພື່ອປິດຊ່ອງໂຫວ່ຮ້າຍແຮງ 2 ຈຸດ ທີ່ນັກຄົ້ນຄວ້າເອີ້ນວ່າ PHP2Shell. ທັງສອງຈຸດໄດ້ຄະແນນຄວາມຮ້າຍແຮງ 9.2 ຈາກ 10.

ອັນຕະລາຍຢູ່ບ່ອນໃດ? ຊ່ອງໂຫວ່ນີ້ອາດເປີດທາງໃຫ້ແຮັກເກີສັ່ງລັນໂຄດຂອງຕົນເອງໃນເຊີບເວີໄດ້ ໂດຍບໍ່ຕ້ອງລັອກອິນ. PHP ບອກວ່າທຸກເຊີບເວີທີ່ໃຊ້ PHP ໃຫ້ບໍລິການເວັບມີຄວາມສ່ຽງ ລວມທັງ PHP-FPM, Apache mod_php ແລະ LiteSpeed. ສ່ຽງສູງສຸດແມ່ນ mod_php ເຊິ່ງມີການສາທິດແລ້ວວ່າໂຈມຕີໄດ້ ກ່ອນໂຄດຂອງເວັບຈະເລີ່ມເຮັດວຽກ.

ເວີຊັນທີ່ແກ້ແລ້ວ:
- PHP 8.5.12
- PHP 8.4.27
- PHP 8.3.36
- PHP 8.2.35

ໃຜທີ່ຍັງໃຊ້ PHP 8.1 ຫຼື ເກົ່າກວ່ານັ້ນ ໂຄງການ PHP ບໍ່ອອກອັບເດດໃຫ້ແລ້ວ ຕ້ອງຖາມຜູ້ໃຫ້ບໍລິການ ຫຼື ຍ້າຍໄປເວີຊັນທີ່ຍັງຮອງຮັບ.

ອີກເລື່ອງທີ່ໜ້າສົນໃຈ: OpenAI ບອກວ່າບໍລິສັດຄວາມປອດໄພ Calif ໃຊ້ GPT-5.6 Sol ຊ່ວຍຊອກພົບຊ່ອງໂຫວ່ນີ້ ແລະ Wiz ກໍລາຍງານເຂົ້າມາຕ່າງຫາກ. ຕາມທີ່ OpenAI ຮູ້ ຄັ້ງນີ້ AI ຊອກພົບກ່ອນແຮັກເກີ.

ສຳລັບຮ້ານຄ້າ ແລະ ບໍລິສັດຢູ່ລາວ ທີ່ເຊົ່າໂຮສຕິ້ງ ຫຼື ໃຊ້ cPanel ລອງເຂົ້າໄປເບິ່ງເວີຊັນ PHP ໃນໜ້າຕັ້ງຄ່າ ຖ້າຍັງບໍ່ແມ່ນເວີຊັນຂ້າງເທິງ ໃຫ້ແຈ້ງຜູ້ໃຫ້ບໍລິການມື້ນີ້ເລີຍ.

ເວັບຂອງທ່ານໃຊ້ PHP ເວີຊັນໃດຢູ່? ລອງກວດແລ້ວບອກກັນໃນຄອມເມັ້ນ.

ຊ່ວຍແຊຣ໌ໂພສນີ້ໃຫ້ຄົນທີ່ດູແລເວັບໄຊ ແລະ ກົດຕິດຕາມເພຈ Arnfar ໄວ້
ທຸກມື້ເວລາ 8:00, 12:00 ແລະ 19:00 ເຮົາສະຫຼຸບຂ່າວເຕັກ, AI ແລະ ຄວາມປອດໄພໄຊເບີເປັນພາສາລາວ

#arnfar #PHP #CyberSecurity #WordPress
## (copy to here ↑)

## PODCAST SCRIPT (copy from here ↓)
ສະບາຍດີ ທຸກຄົນ ນີ້ແມ່ນ Arnfar ມື້ນີ້ມີຂ່າວດ່ວນສຳລັບທຸກຄົນທີ່ມີເວັບໄຊ.
ເມື່ອວັນທີ ຊາວເອັດ ເດືອນຕຸລາ ທີມພັດທະນາ PHP ອອກແພັດຄວາມປອດໄພແບບດ່ວນ.
ແພັດນີ້ປິດຊ່ອງໂຫວ່ຮ້າຍແຮງ ສອງ ຈຸດ ທີ່ນັກຄົ້ນຄວ້າເອີ້ນວ່າ PHP ທູ ເຊວ.
ທັງສອງຈຸດໄດ້ຄະແນນຄວາມຮ້າຍແຮງ ເກົ້າ ຈຸດ ສອງ ຈາກ ສິບ.
ບັນຫາຄື ແຮັກເກີອາດສັ່ງລັນໂຄດຂອງຕົນເອງໃນເຊີບເວີໄດ້ ໂດຍບໍ່ຕ້ອງລັອກອິນເລີຍ.
PHP ບອກວ່າທຸກເຊີບເວີທີ່ໃຊ້ PHP ໃຫ້ບໍລິການເວັບ ມີຄວາມສ່ຽງທັງໝົດ.
ເວີຊັນທີ່ແກ້ແລ້ວ ມີ ແປດ ຈຸດ ຫ້າ ຈຸດ ສິບສອງ ແລະ ແປດ ຈຸດ ສີ່ ຈຸດ ຊາວເຈັດ.
ສ່ວນສາຍເກົ່າ ໃຫ້ອັບເດດເປັນ ແປດ ຈຸດ ສາມ ຈຸດ ສາມສິບຫົກ ຫຼື ແປດ ຈຸດ ສອງ ຈຸດ ສາມສິບຫ້າ.
ໃຜທີ່ຍັງໃຊ້ ແປດ ຈຸດ ໜຶ່ງ ຫຼື ເກົ່າກວ່າ ໂຄງການ PHP ບໍ່ອອກອັບເດດໃຫ້ແລ້ວ.
ເລື່ອງທີ່ໜ້າສົນໃຈຄື OpenAI ບອກວ່າ ຊ່ອງໂຫວ່ນີ້ຖືກຊອກພົບໂດຍມີ GPT ຫ້າ ຈຸດ ຫົກ Sol ຊ່ວຍ.
ຕາມທີ່ OpenAI ຮູ້ ເທື່ອນີ້ AI ຊອກພົບກ່ອນແຮັກເກີ.
ສຳລັບຮ້ານຄ້າ ແລະ ບໍລິສັດຢູ່ລາວ ທີ່ໃຊ້ WordPress ຫຼື ເຊົ່າໂຮສຕິ້ງ ໃຫ້ກວດເວີຊັນ PHP ມື້ນີ້ເລີຍ.
ຖ້າບໍ່ແນ່ໃຈ ໃຫ້ໂທຖາມຜູ້ໃຫ້ບໍລິການໂຮສຕິ້ງ ຫຼື ທີມ IT ຂອງທ່ານ.
ເວັບຂອງທຸກຄົນໃຊ້ PHP ເວີຊັນໃດຢູ່ ລອງກວດແລ້ວພິມບອກໃນຄອມເມັ້ນເດີ້.
ຖ້າຂ່າວນີ້ມີປະໂຫຍດ ຝາກກົດຕິດຕາມເພຈ Arnfar ແລະ ແບ່ງປັນໃຫ້ຄົນທີ່ດູແລເວັບໄຊນຳເດີ້.
## (podcast script end ↑)

## Sources
- php.net security advisory, 21 Oct 2026 (fixed versions, CVE-2026-109618, CVE-2026-109619, who is at risk): https://www.php.net/archive/2026.php#2026-10-21-5
- php.net pre-announcement, 20 Oct 2026 (both rated CVSS v4.0 9.2): https://www.php.net/archive/2026.php#2026-10-20-1
- OpenAI, "Patch the Planet" coordinated disclosure (Calif + GPT-5.6 Sol, Wiz): https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/
- Reuters, PHP developers issue new version fixing critical vulnerabilities (21 Oct 2026): https://www.reuters.com/business/php-programming-language-developers-issue-new-version-fixing-critical-2026-10-21/
- The Verge, critical PHP vulnerability (21 Oct 2026): https://www.theverge.com/tech/1015257/php-vulnerability-patch-website-security-wordpress
- Wired, critical PHP vulnerabilities (21 Oct 2026): https://www.wired.com/story/this-is-not-a-drill-2-php-vulnerabilities-are-setting-the-internet-on-fire/

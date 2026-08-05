#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

# Add tools directory to path to import lao_fix
REPO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_DIR / "tools"))
from lao_fix import Options, normalize_lao

def normalize_obj(obj, opts):
    if isinstance(obj, str):
        # We only normalize if there are Lao characters
        if any("\u0e80" <= c <= "\u0eff" for c in obj):
            normalized, _ = normalize_lao(obj, opts)
            return normalized
        return obj
    elif isinstance(obj, list):
        return [normalize_obj(x, opts) for x in obj]
    elif isinstance(obj, dict):
        return {k: normalize_obj(v, opts) for k, v in obj.items()}
    return obj

def main():
    spec = {
      "size": "portrait",
      "prefix": "arnfar-nano-banana",
      "category": "ຂ່າວເຕັກໂນໂລຊີ",
      "footer_tags": "#arnfar   #Gemini   #NanoBanana   #AIImage",
      "cards": [
        {
          "kind": "feature",
          "eyebrow": "GOOGLE GEMINI IMAGE MODELS",
          "headline": ["Gemini 3.1 & 3 GA"],
          "accent": "Google Nano Banana",
          "subhead": "ໂມເດລສ້າງຮູບຮຸ່ນເຕັມ ພ້ອມໃຊ້ງານຈິງແລ້ວ!",
          "mockup": {
            "type": "video",
            "title": "video_to_image_demo.mp4",
            "tag": "Flash 3.1",
            "time": "0:04 / 0:12"
          },
          "badges": ["GA Version", "Video-to-Image"],
          "features": [
            {"icon": "play", "text": "ສ້າງຮູບຈາກວິດີໂອ / YouTube"},
            {"icon": "bolt", "text": "ໄວຂຶ້ນ ແລະ ຕົ້ນທຶນຕ່ຳລົງ"},
            {"icon": "layers", "text": "ຮອງຮັບຮູບລະອຽດສູງເຖິງ 4K"},
            {"icon": "globe", "text": "ໃຊ້ງານຜ່ານ API / Studio"}
          ]
        },
        {
          "kind": "points",
          "eyebrow": "🔍 ມັນເກີດຫຍັງຂຶ້ນ?",
          "title": "ລາຍລະອຽດແຕ່ລະໂມເດລ",
          "items": [
            {"mark": "dot", "text": "Gemini 3.1 Flash Image (Nano Banana 2): ເນັ້ນຄວາມໄວສູງ ແລະ ຕົ້ນທຶນປະຢັດ"},
            {"mark": "dot", "text": "Gemini 3 Pro Image (Nano Banana Pro): ເນັ້ນຄຸນນະພາບສູງ ຮອງຮັບຄວາມລະອຽດ 1K-4K"},
            {"mark": "check", "text": "ຟີເຈີ Video-to-Image ສ້າງຮູບ/Thumbnail ຈາກວິດີໂອໄດ້ງ່າຍໆ (ສະເພາະ Flash)"},
            {"mark": "cross", "text": "ໂມເດລ preview ເກົ່າປິດບໍລິການແລ້ວ 25 ມິຖຸນາ 2026 — ຕ້ອງຍ້າຍດ່ວນ"}
          ]
        },
        {
          "kind": "stat",
          "category": "ລາຄາເລີ່ມຕົ້ນ",
          "value": "$0.067",
          "label": "ຕໍ່ຮູບ (Flash Image 1K)",
          "note": "ຄິດໄລ່ຈາກລາຄາ API $0.50 / 1M input tokens",
          "badges": ["Google AI Studio", "Gemini API"],
          "chips": ["Flash: ~$0.067/ຮູບ", "Pro: ~$0.134/ຮູບ (1K-2K)", "Pro 4K: ~$0.240/ຮູບ"]
        },
        {
          "kind": "points",
          "eyebrow": "ANALYSIS",
          "title": "ຂໍ້ດີ ແລະ ຂໍ້ເສຍ / ສິ່ງທີ່ຕ້ອງລະວັງ",
          "items": [
            {"mark": "check", "text": "ຂໍ້ດີ: ຕົ້ນທຶນຕໍ່ຮູບຖືກຫຼາຍ ຫຼຸດຄ່າໃຊ້ຈ່າຍໂຄສະນາໄດ້ຫຼາຍເທົ່າ"},
            {"mark": "check", "text": "ຂໍ້ດີ: ໂມເດລ GA ມີຄວາມໝັ້ນຄົງສູງ ເໝາະສົມສຳລັບ Production"},
            {"mark": "cross", "text": "ລະວັງ: ບໍ່ມີ free tier ສຳລັບໂມເດລສ້າງຮູບເຫຼົ່ານີ້ — ຕ້ອງໃຊ້ບັນຊີເສຍເງິນ"},
            {"mark": "cross", "text": "ລະວັງ: ລາຄາຄິດໄລ່ຕາມ token ຫາກສ້າງຮູບ 4K ຈະແພງກວ່າຫຼາຍ"}
          ]
        }
      ]
    }

    opts = Options()
    normalized_spec = normalize_obj(spec, opts)

    spec_path = REPO_DIR / "output" / "gemini-image-models-spec.json"
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(normalized_spec, f, ensure_ascii=False, indent=2)
    print(f"Saved normalized spec to {spec_path}")

    # Run the news card generator
    script_path = REPO_DIR / "skills" / "breaking-news-report" / "scripts" / "arnfar_news_card.py"
    out_dir = REPO_DIR / "posts" / "images"
    
    cmd = [
        "python3",
        str(script_path),
        str(spec_path),
        "--outdir",
        str(out_dir)
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("Successfully generated cards!")
        print(res.stdout)
    else:
        print("Failed to generate cards:")
        print(res.stderr)
        sys.exit(res.returncode)

if __name__ == "__main__":
    main()

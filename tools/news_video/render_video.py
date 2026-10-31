#!/usr/bin/env python3
"""Arnfar news video renderer (1080x1920, 30 fps, H.264 + AAC).

Scenes follow the approved Claude Design template ("Arnfar News Video 9:16").
All Lao text is browser DOM text (never ffmpeg drawtext). Timing comes from the
voice WAV produced by LaoVoice AI Studio (Quick Script Studio, monologue mode):
sentence boundaries are found with ffmpeg silencedetect and matched to the
script lines, so subtitles and scene cuts follow the voice.

usage: render_video.py <story.json> <voice.wav> <out.mp4> [--fps 30] [--preview] [--web]
  Output <out.mp4> is the HQ master (1080x1920, CRF 16 <=12 Mbps) and is the file to upload.
  --preview  writes <out>-sheet.jpg (one frame per scene) and stops; no MP4.

story.json keys:
  tag, accent ("warn"|"brand"), logo, background (optional image path),
  lines:  [{"text": "<spoken line, as in the podcast script>", "hl": "<words to colour>"}...]
  scenes: [{"type": "hook|photo|stat|list|question|outro", "lines": [0, 1], ...scene fields}]
Scene fields: see SKILL.md (arnfar-news-video-design) or tools/news_video/story_example.json.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
LEAD = 0.1  # silence before the voice starts (s); keep tiny so the hook lands at frame 0
TAIL = 1.2   # hold on the outro after the voice ends (s)
# HQ standard (Lomon, 2026-10-31): every Arnfar video is uploaded as the 1080x1920 HQ master,
# never a size-capped web copy. H.264 High, CRF 16 capped at 12 Mbps, preset slower, 2 s GOP, 30 fps.
HQ_X264 = ["-c:v", "libx264", "-preset", "slower", "-profile:v", "high", "-crf", "16",
           "-maxrate", "12M", "-bufsize", "24M", "-g", "60", "-keyint_min", "30", "-sc_threshold", "40",
           "-x264-params", "aq-mode=3:aq-strength=0.9:deblock=-1,-1:psy-rd=1.0,0.15",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
HQ_MIN_KBPS = 3500  # QC floor for the master's video bitrate
# Optional supersampling (--ss 2): frames drawn at 2160x3840 and Lanczos-downscaled to 1080x1920.
# Slightly smoother text edges, about 1.5-2 h per 2:55 clip instead of about 25 min.
SUPERSAMPLE = 1  # Lomon 2026-10-31: default 1x + HQ encode; pass --ss 2 only for a clip he asks to supersample


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p.stderr + p.stdout


def audio_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def silences(path: Path, noise_db: int = -35, min_len: float = 0.18) -> list[tuple[float, float]]:
    log = run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", f"silencedetect=noise={noise_db}dB:d={min_len}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return list(zip(starts, ends))


def line_starts(lines: list[str], wav: Path) -> tuple[list[float], float]:
    """Start time of each line in the voice track (seconds, voice timeline)."""
    dur = audio_duration(wav)
    sil = silences(wav)
    voice_start = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    voice_end = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
    gaps = [(a, b) for a, b in sil if a > voice_start + 0.1 and b < voice_end - 0.1]
    weights = [max(len(re.sub(r"\s+", "", t)), 1) for t in lines]
    total = sum(weights)
    n, span = len(lines), voice_end - voice_start
    rate = span / total  # seconds per character, whole track
    if len(gaps) < n - 1:
        # not enough pauses: fall back to proportional split
        starts, cum = [voice_start], 0
        for w in weights[:-1]:
            cum += w
            starts.append(voice_start + span * cum / total)
        return starts, dur
    # Dynamic programming: pick n-1 pauses (in order) so every line's spoken
    # length is closest to its expected length (chars x average rate), with a
    # small bonus for longer pauses (sentence ends pause longer than commas).
    # pts[k] = (time where a line ends, time where the next begins)
    pts = [(voice_start, voice_start)] + [(a, b) for a, b in gaps] + [(voice_end, voice_end)]
    G = len(pts)
    INF = float("inf")

    def seg_cost(i: int, p: int, q: int) -> float:
        d = pts[q][0] - pts[p][1]
        e = weights[i] * rate
        return ((d - e) / e) ** 2

    best = [[INF] * G for _ in range(n)]
    back = [[-1] * G for _ in range(n)]
    for q in range(1, G - 1):
        best[0][q] = seg_cost(0, 0, q) - 0.3 * min(pts[q][1] - pts[q][0], 1.0)
    for i in range(1, n - 1):
        for q in range(i + 1, G - 1):
            bonus = 0.3 * min(pts[q][1] - pts[q][0], 1.0)
            for p in range(i, q):
                if best[i - 1][p] == INF:
                    continue
                c = best[i - 1][p] + seg_cost(i, p, q) - bonus
                if c < best[i][q]:
                    best[i][q], back[i][q] = c, p
    last = G - 1
    final, fp = INF, -1
    for p in range(n - 1, last):
        if best[n - 2][p] == INF:
            continue
        c = best[n - 2][p] + seg_cost(n - 1, p, last)
        if c < final:
            final, fp = c, p
    picks, q = [], fp
    for i in range(n - 2, -1, -1):
        picks.append(q)
        q = back[i][q]
    picks.reverse()
    starts = [voice_start] + [pts[k][1] - 0.05 for k in picks]
    return starts, dur


def auto_background(photo: Path, dst: Path) -> Path:
    """Topic background from the story's own photo: cover-fit, blur, Arnfar
    duotone (navy -> blue -> teal), darkened, vignette. Text-free by design."""
    from PIL import Image, ImageDraw, ImageFilter, ImageOps
    W, H = 1300, 2300  # oversize so the slow drift never shows an edge
    im = Image.open(photo).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(9))
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    # bright source areas (white product shots) must not wash out the frame
    g = g.point(lambda v: int(30 + v * 0.62))
    duo = ImageOps.colorize(g, black=(4, 10, 28), mid=(6, 70, 140), white=(30, 190, 150), midpoint=150)
    dark = Image.new("RGB", (W, H), (5, 12, 29))
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-W * 0.35, -H * 0.15, W * 1.35, H * 1.1), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    out = Image.composite(Image.blend(dark, duo, 0.62), dark, vig)
    out.save(dst, quality=90)
    return dst


def build_spec(story: dict, wav: Path) -> dict:
    texts = [ln["text"] for ln in story["lines"]]
    starts, dur = line_starts(texts, wav)
    spec = dict(story)
    spec["lines"] = [dict(ln, start=round(s + LEAD, 3)) for ln, s in zip(story["lines"], starts)]
    spec["duration"] = round(dur + LEAD + TAIL, 3)
    for k in ("logo", "background"):
        if spec.get(k):
            spec[k] = Path(spec[k]).resolve().as_uri()
    def photo_fit(path: str, given: str | None) -> str | None:
        # full-screen photos: small or very wide images would be blurry/cropped to nothing when
        # cover-filled to 9:16, so show them whole ("contain") over a blurred copy of themselves
        if given or not spec.get("fullphoto"):
            return given
        try:
            from PIL import Image
            with Image.open(path) as im:
                w, h = im.size
        except Exception:
            return None
        return "contain" if (w / max(h, 1) > 2.2 or h < 900) else None

    for sc in spec["scenes"]:
        if sc.get("photo"):
            sc["fit"] = photo_fit(sc["photo"], sc.get("fit"))
            sc["photo"] = Path(sc["photo"]).resolve().as_uri()
    for ln in spec["lines"]:
        if ln.get("photo"):
            ln["fit"] = photo_fit(ln["photo"], ln.get("fit"))
            ln["photo"] = Path(ln["photo"]).resolve().as_uri()
    covered = sorted(i for sc in spec["scenes"] for i in sc["lines"])
    if covered != list(range(len(texts))):
        sys.exit(f"scenes must cover every line exactly once, in order; got {covered}")
    return spec


def open_page(p, spec: dict, work: Path, scale: int = 1):
    page_dir = work / "page"
    page_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(HERE / "template.html", page_dir / "index.html")
    shutil.copytree(HERE / "fonts", page_dir / "fonts", dirs_exist_ok=True)
    browser = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=scale)
    page.add_init_script(f"window.SPEC = {json.dumps(spec, ensure_ascii=False)};")
    page.goto((page_dir / "index.html").as_uri())
    page.evaluate("window.READY")
    page.wait_for_timeout(300)
    return browser, page


def check_layout(spec: dict, work: Path) -> list[str]:
    """Seek to every line (and scene start) and collect safe-zone / clipping / subtitle-overlap issues."""
    times = sorted({round(ln["start"] + 1.2, 2) for ln in spec["lines"]} | {0.05})
    issues: list[str] = []
    with sync_playwright() as p:
        browser, page = open_page(p, spec, work)
        for t in times:
            for msg in page.evaluate(f"window.layoutCheck({t})"):
                issues.append(f"t={t:6.2f}s  {msg}")
        browser.close()
    return issues


def preview(spec: dict, out: Path, work: Path) -> Path:
    from PIL import Image
    shots = []
    with sync_playwright() as p:
        browser, page = open_page(p, spec, work)
        for sc in spec["scenes"]:
            idx = sc["lines"][-1]
            t = spec["lines"][idx]["start"] + 0.9
            page.evaluate(f"window.seek({t})")
            f = work / f"pv{len(shots)}.png"
            page.screenshot(path=str(f))
            shots.append(f)
        browser.close()
    w, h = 360, 640
    sheet = Image.new("RGB", (w * len(shots) + 10 * (len(shots) - 1), h), (20, 20, 20))
    for i, f in enumerate(shots):
        sheet.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (i * (w + 10), 0))
    dst = out.with_name(out.stem + "-sheet.jpg")
    sheet.save(dst, quality=90)
    return dst


def render(spec: dict, wav: Path, out: Path, fps: int, work: Path, music: str | None, ss: int = SUPERSAMPLE) -> None:
    frames = int(spec["duration"] * fps)
    silent = work / "video.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps),
                           "-c:v", "mjpeg", "-i", "-", *(["-vf", "scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int"] if ss > 1 else []),
                           *HQ_X264, "-r", str(fps), str(silent)], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        browser, page = open_page(p, spec, work, ss)
        for i in range(frames):
            page.evaluate(f"window.seek({i / fps})")
            ff.stdin.write(page.screenshot(type="jpeg", quality=100))
            if i % (fps * 10) == 0:
                print(f"frame {i}/{frames}", flush=True)
        browser.close()
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg video encode failed")
    mux(silent, wav, out, spec["duration"], music, work, spec)


def sfx_events(spec: dict) -> dict:
    """Sound-effect cue times from the scenes: impact on the hook, whoosh on every scene change,
    riser into every new chapter."""
    scenes, lines = spec["scenes"], spec["lines"]
    starts = [0.0] + [lines[sc["lines"][0]]["start"] for sc in scenes[1:]]
    ev = {"impact": [0.05], "whoosh": [], "riser": []}
    last_chap = None
    for i, sc in enumerate(scenes):
        chap = (sc.get("chapter") or "").split(" ")[0]
        if i > 0:
            ev["whoosh"].append(round(starts[i], 2))
            if chap and chap != last_chap and starts[i] > 2:
                ev["riser"].append(round(starts[i], 2))
        if chap:
            last_chap = chap
    return ev


def mux(video: Path, wav: Path, out: Path, duration: float, music: str | None, work: Path, spec: dict | None = None) -> None:
    """Voice (delayed by LEAD) + optional generated music bed, ducked under the voice."""
    delay = int(LEAD * 1000)
    if not music:
        run(["ffmpeg", "-y", "-hide_banner", "-i", str(video), "-i", str(wav),
             "-filter_complex", f"[1:a]adelay={delay}|{delay},apad,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
             "-movflags", "+faststart", str(out)])
        return
    bed = work / "music.wav"
    cmd = [sys.executable, str(HERE / "gen_music.py"), str(bed), f"{duration + 0.5:.2f}", "--mood", music]
    if spec is not None:
        evf = work / "events.json"
        evf.write_text(json.dumps(sfx_events(spec)), encoding="utf-8")
        cmd += ["--events", str(evf)]
    subprocess.run(cmd, check=True, capture_output=True)
    fc = (f"[1:a]adelay={delay}|{delay},aresample=48000,aformat=channel_layouts=stereo,apad,asplit=2[v1][v2];"
          f"[2:a]aresample=48000,volume={0.26 if music == 'hype' else 0.22}[m];"
          f"[m][v2]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
          f"[v1][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
    run(["ffmpeg", "-y", "-hide_banner", "-i", str(video), "-i", str(wav), "-i", str(bed),
         "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(out)])


def hq_report(src: Path) -> tuple[int, int, int, float]:
    """(width, height, video kbps, duration) of the HQ master, for QC."""
    o = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,bit_rate:format=duration",
             "-of", "default=nw=1", str(src)])
    kv = dict(l.split("=", 1) for l in o.splitlines() if "=" in l)
    return int(kv["width"]), int(kv["height"]), int(int(kv.get("bit_rate", "0") or 0) / 1000), float(kv["duration"])


def web_copy(src: Path) -> Path:
    """LEGACY, off by default (--web). Upload copy under ~9.5 MB for the 10 MB browser-extension
    upload cap. It looks soft (0.3 Mbps at 720p for a 2:55 clip); since 2026-10-31 Arnfar uploads
    the HQ master through the Windows file dialog instead. Only use when explicitly asked."""
    dst = src.with_name(src.stem + "-web.mp4")
    dur = audio_duration(src)
    akbps = 96
    budget_kbit = 9.2 * 8192  # ~9.2 MiB
    vkbps = int(budget_kbit / dur) - akbps
    for _ in range(4):
        vkbps = max(250, min(1400, vkbps))
        scale = [] if vkbps >= 650 else ["-vf", "scale=720:1280:flags=lanczos"]
        run(["ffmpeg", "-y", "-hide_banner", "-i", str(src), *scale, "-c:v", "libx264", "-preset", "slow",
             "-b:v", f"{vkbps}k", "-maxrate", f"{int(vkbps * 1.15)}k", "-bufsize", f"{2 * vkbps}k",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", f"{akbps}k", "-movflags", "+faststart", str(dst)])
        if dst.stat().st_size <= 9.7 * 1024 * 1024:
            break
        vkbps = int(vkbps * 0.85)
    return dst


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("wav")
    ap.add_argument("out")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--music", default="hype", help="background music mood: hype (default, energetic) | calm | upbeat | serious, or 'none'")
    ap.add_argument("--remux", action="store_true", help="keep the existing MP4 frames, rebuild audio only")
    ap.add_argument("--check", action="store_true", help="only run the safe-zone / overflow check (exit 1 on issues)")
    ap.add_argument("--ss", type=int, default=SUPERSAMPLE, help="supersampling factor: 1 (default, HQ encode) or 2 (draw 2160x3840 then downscale; 1.5-2 h per clip, only on request)")
    ap.add_argument("--web", action="store_true", help="LEGACY: also write a <=9.7 MB -web.mp4 (soft); not for normal uploads")
    a = ap.parse_args()
    music = None if a.music in ("none", "off", "") else a.music
    story_path = Path(a.story).resolve()
    story = json.loads(story_path.read_text(encoding="utf-8"))
    # relative asset paths in story.json are relative to the story file
    base = story_path.parent
    for k in ("logo", "background"):
        if story.get(k) and not Path(story[k]).is_absolute():
            story[k] = str(base / story[k])
    for sc in story["scenes"]:
        if sc.get("photo") and not Path(sc["photo"]).is_absolute():
            sc["photo"] = str(base / sc["photo"])
    for ln in story["lines"]:
        if ln.get("photo") and not Path(ln["photo"]).is_absolute():
            ln["photo"] = str(base / ln["photo"])
    wav, out = Path(a.wav).resolve(), Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if not story.get("background"):
        src = story.get("background_from") or next((sc["photo"] for sc in story["scenes"] if sc.get("photo")), None)
        if src:
            if not Path(src).is_absolute():
                src = str(base / src)
            story["background"] = str(auto_background(Path(src), out.with_name(out.stem + "-bg.jpg")))
    spec = build_spec(story, wav)
    (out.with_suffix(".timing.json")).write_text(json.dumps(
        [{"start": ln["start"], "text": ln["text"]} for ln in spec["lines"]], ensure_ascii=False, indent=1), encoding="utf-8")
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        if a.preview or a.check:
            issues = check_layout(spec, work)
            for msg in issues:
                print("LAYOUT", msg, file=sys.stderr)
            print(f"layout check: {len(issues)} issue(s)", file=sys.stderr)
            if a.check:
                sys.exit(1 if issues else 0)
            print(preview(spec, out, work))
            return
        if a.remux:
            # reuse the frames of an existing render; only rebuild the audio
            src = work / "prev.mp4"
            shutil.copy(out, src)
            mux(src, wav, out, spec["duration"], music, work, spec)
        else:
            render(spec, wav, out, a.fps, work, music, a.ss)
    w, h, kbps, dur = hq_report(out)
    ok = (w, h) == (1080, 1920) and kbps >= HQ_MIN_KBPS
    print(out)
    print(f"HQ master: {w}x{h}, {kbps} kbps video, {dur:.2f} s, {out.stat().st_size / 1e6:.1f} MB "
          f"-> {'OK, upload THIS file (HQ)' if ok else 'BELOW HQ STANDARD, do not upload'}")
    if a.web:
        web = web_copy(out)
        print(f"{web} ({web.stat().st_size / 1e6:.1f} MB, legacy soft copy, not for normal uploads)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Original, copyright-free background bed for Arnfar news videos.

Generated from code (no samples, no third-party audio), so it is safe for
Facebook, Instagram and TikTok. Calm "tech news" mood: soft detuned pad,
plucked arpeggio, light kick + shaker, 96 BPM, chord loop i-VI-III-VII.

Moods: calm, upbeat, serious, and "hype" (default since 2026-10-25, Lomon: the
music must be exciting and fun). Hype follows what short-form research recommends
for retention (120-140 BPM, "energetic/engaging"): 124 BPM four-on-the-floor kick,
clap on 2 and 4, off-beat open hats, 16th-note synth pluck, side-chained bass and
pad that "pump" with the kick, a riser + crash every 8 bars.

--events <json> adds sound effects synced to the video: {"impact": [t...],
"whoosh": [t...], "riser": [t...]} (seconds; a riser ENDS at t). render_video.py
writes it from the scene / chapter times.

usage: gen_music.py <out.wav> <seconds> [--mood hype|calm|upbeat|serious] [--seed N] [--events ev.json]
"""
from __future__ import annotations

import argparse
import json
import wave

import numpy as np
from scipy.signal import butter, lfilter

SR = 44100

MOODS = {
    # (bpm, root MIDI note, chord loop as semitone triads relative to root)
    "calm":    (96,  57, [(0, 3, 7), (-4, 0, 3), (3, 7, 10), (-2, 2, 5)]),   # Am F C G
    "upbeat":  (112, 60, [(0, 4, 7), (-3, 0, 4), (5, 9, 12), (7, 11, 14)]),  # C Am F G
    "serious": (84,  52, [(0, 3, 7), (-4, 0, 3), (-2, 2, 5), (-5, -1, 2)]),  # Em C D B-ish
    "hype":    (124, 57, [(0, 3, 7), (-4, 0, 3), (3, 7, 10), (-2, 2, 5)]),   # Am F C G (vi-IV-I-V feel)
}


def midi_hz(n: float) -> float:
    return 440.0 * 2 ** ((n - 69) / 12)


def one_pole_lp(x: np.ndarray, cutoff: float) -> np.ndarray:
    a = np.exp(-2 * np.pi * cutoff / SR)
    return lfilter([1 - a], [1, -a], x)


def bandpass(x: np.ndarray, lo: float, hi: float, order: int = 2) -> np.ndarray:
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], btype="band")
    return lfilter(b, a, x)


def highpass(x: np.ndarray, cut: float, order: int = 2) -> np.ndarray:
    b, a = butter(order, cut / (SR / 2), btype="high")
    return lfilter(b, a, x)


def saw(freq: float, t: np.ndarray, phase: float = 0.0) -> np.ndarray:
    return 2 * ((freq * t + phase) % 1.0) - 1


def render(seconds: float, mood: str, seed: int) -> np.ndarray:
    bpm, root, chords = MOODS[mood]
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    beat = 60.0 / bpm
    bar = beat * 4
    out = np.zeros(n)

    # pad: 3 detuned saws per chord note, low-passed, slow attack per bar
    pad = np.zeros(n)
    nbars = int(np.ceil(seconds / bar))
    for b in range(nbars):
        ch = chords[b % len(chords)]
        s, e = int(b * bar * SR), min(int((b + 1) * bar * SR), n)
        if s >= n:
            break
        tt = t[s:e] - t[s]
        env = np.minimum(tt / 0.6, 1.0) * np.minimum((bar - tt) / 0.4, 1.0)
        seg = np.zeros(e - s)
        for iv in ch:
            f = midi_hz(root + iv)
            for d in (-0.08, 0.0, 0.08):
                seg += saw(f * 2 ** (d / 12), tt, rng.random())
        pad[s:e] += seg * env / 9
    pad = one_pole_lp(pad, 900)
    out += 0.55 * pad

    # pluck arpeggio, 8th notes, two octaves up
    pl = np.zeros(n)
    step = beat / 2
    k = 0
    while k * step < seconds:
        s = int(k * step * SR)
        ch = chords[int(k * step // bar) % len(chords)]
        note = root + 12 + ch[[0, 1, 2, 1][k % 4]] + (12 if k % 8 == 6 else 0)
        L = min(int(0.35 * SR), n - s)
        tt = np.arange(L) / SR
        f = midi_hz(note)
        tone = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)
        pl[s:s + L] += tone * np.exp(-tt * 9) * 0.22
        k += 1
    out += pl

    # kick on 1 and 3, shaker on 8ths
    k = 0
    while k * beat < seconds:
        s = int(k * beat * SR)
        if k % 2 == 0:
            L = min(int(0.25 * SR), n - s)
            tt = np.arange(L) / SR
            f = 50 + 70 * np.exp(-tt * 30)
            out[s:s + L] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14) * 0.5
        for h in (0, 0.5):
            hs = int((k + h) * beat * SR)
            L = min(int(0.05 * SR), n - hs)
            if L > 0:
                tt = np.arange(L) / SR
                nz = rng.standard_normal(L)
                nz = nz - np.concatenate(([0], nz[:-1]))  # crude high-pass
                out[hs:hs + L] += nz * np.exp(-tt * 70) * (0.05 if h else 0.035)
        k += 1

    # fades + normalise to -3 dBFS peak
    fade_in, fade_out = int(1.0 * SR), int(2.0 * SR)
    out[:fade_in] *= np.linspace(0, 1, fade_in)
    out[-fade_out:] *= np.linspace(1, 0, fade_out)
    out /= max(np.max(np.abs(out)), 1e-6)
    return out * 0.7


def render_hype(seconds: float, seed: int) -> np.ndarray:
    bpm, root, chords = MOODS["hype"]
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    beat = 60.0 / bpm
    bar = beat * 4
    out = np.zeros(n)
    nbeats = int(np.ceil(seconds / beat)) + 1

    # side-chain envelope: dips right after every kick, recovers within ~0.25 beat
    ph = (t % beat) / beat
    duck = 0.35 + 0.65 * np.minimum(ph / 0.28, 1.0) ** 1.6

    # pad (supersaw, low-passed) and saw bass on the chord root, both pumped by the kick
    pad = np.zeros(n); bass = np.zeros(n)
    for b in range(int(np.ceil(seconds / bar))):
        ch = chords[b % len(chords)]
        s, e = int(b * bar * SR), min(int((b + 1) * bar * SR), n)
        if s >= n:
            break
        tt = t[s:e] - t[s]
        seg = np.zeros(e - s)
        for iv in ch:
            f = midi_hz(root + 12 + iv)
            for d in (-0.12, -0.04, 0.04, 0.12):
                seg += saw(f * 2 ** (d / 12), tt, rng.random())
        pad[s:e] += seg / 12
        fb = midi_hz(root - 12 + ch[0])
        # bass: 8th-note pulses (off-beat accent) for drive
        pulse = ((tt / (beat / 2)) % 1.0)
        benv = np.exp(-pulse * 3.0) * (0.8 + 0.2 * (np.floor(tt / (beat / 2)) % 2))
        bass[s:e] += (0.7 * saw(fb, tt) + 0.3 * np.sin(2 * np.pi * fb * tt)) * benv
    out += 0.30 * one_pole_lp(pad, 2200) * duck
    out += 0.42 * one_pole_lp(bass, 420) * duck

    # 16th-note pluck arpeggio, brighter and busier than calm
    pl = np.zeros(n)
    step = beat / 4
    pattern = [0, 2, 1, 2, 0, 2, 1, 3]
    k = 0
    while k * step < seconds:
        s = int(k * step * SR)
        ch = chords[int(k * step // bar) % len(chords)]
        idx = pattern[k % len(pattern)]
        note = root + 24 + (ch[idx] if idx < 3 else ch[0] + 12)
        L = min(int(0.18 * SR), n - s)
        tt = np.arange(L) / SR
        f = midi_hz(note)
        tone = saw(f, tt) * 0.5 + np.sin(2 * np.pi * f * tt)
        pl[s:s + L] += tone * np.exp(-tt * 18) * (0.16 if k % 4 == 0 else 0.11)
        k += 1
    out += one_pole_lp(pl, 5000)

    for k in range(nbeats):
        s = int(k * beat * SR)
        if s >= n:
            break
        # kick on every beat
        L = min(int(0.28 * SR), n - s)
        tt = np.arange(L) / SR
        f = 45 + 110 * np.exp(-tt * 35)
        out[s:s + L] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 11) * 0.75
        # clap on 2 and 4
        if k % 2 == 1:
            L = min(int(0.18 * SR), n - s)
            nz = bandpass(rng.standard_normal(L), 900, 3500)
            tt = np.arange(L) / SR
            env = np.exp(-tt * 25) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * tt) > 0.7))
            out[s:s + L] += nz * env * 0.32
        # open hat on the off-beat, closed hats on 16ths
        for h, amp, dec in ((0.5, 0.12, 22), (0.25, 0.04, 90), (0.75, 0.04, 90)):
            hs = int((k + h) * beat * SR)
            L = min(int(0.12 * SR), n - hs)
            if L > 0:
                tt = np.arange(L) / SR
                out[hs:hs + L] += highpass(rng.standard_normal(L), 7000) * np.exp(-tt * dec) * amp

    # riser into every 8th bar + crash on the downbeat
    for b8 in range(8, int(seconds / bar) + 1, 8):
        end = int(b8 * bar * SR)
        L = int(2 * bar * SR)
        s = max(end - L, 0)
        if end >= n:
            break
        tt = np.arange(end - s) / SR
        x = tt / max(tt[-1], 1e-6)
        nz = highpass(rng.standard_normal(end - s), 800)  # bright noise sweep
        out[s:end] += nz * (x ** 2.2) * 0.10
        L2 = min(int(1.6 * SR), n - end)
        tt2 = np.arange(L2) / SR
        out[end:end + L2] += highpass(rng.standard_normal(L2), 4000) * np.exp(-tt2 * 2.8) * 0.16

    fade_in, fade_out = int(0.4 * SR), int(2.0 * SR)
    out[:fade_in] *= np.linspace(0, 1, fade_in)
    out[-fade_out:] *= np.linspace(1, 0, fade_out)
    out /= max(np.max(np.abs(out)), 1e-6)
    return out * 0.75


def render_events(seconds: float, events: dict, seed: int) -> np.ndarray:
    """Sound effects synced to the video: impact (hook), whoosh (scene change), riser (into a chapter)."""
    rng = np.random.default_rng(seed + 99)
    n = int(seconds * SR)
    fx = np.zeros(n)
    for t0 in events.get("impact", []):
        s = int(t0 * SR)
        if s >= n:
            continue
        L = min(int(1.4 * SR), n - s)
        tt = np.arange(L) / SR
        f = 38 + 90 * np.exp(-tt * 9)
        boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.2)
        crack = highpass(rng.standard_normal(L), 3000) * np.exp(-tt * 30)
        fx[s:s + L] += boom * 0.9 + crack * 0.35
    for t0 in events.get("whoosh", []):
        L = int(0.55 * SR)
        s = int(t0 * SR) - L // 2
        if s < 0 or s + L > n:
            continue
        tt = np.arange(L) / SR
        x = tt / tt[-1]
        env = np.sin(np.pi * x) ** 2
        nz = rng.standard_normal(L)
        lo = bandpass(nz, 300, 1500); hi = bandpass(nz, 1500, 7000)
        sweep = lo * (1 - x) + hi * x
        fx[s:s + L] += sweep * env * 0.55
    for t0 in events.get("riser", []):
        end = int(t0 * SR)
        L = int(1.6 * SR)
        s = end - L
        if s < 0 or end > n:
            continue
        tt = np.arange(L) / SR
        x = tt / tt[-1]
        f = 220 * 2 ** (x * 2.5)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
        nz = highpass(rng.standard_normal(L), 2000)
        fx[s:end] += (tone * 0.18 + nz * 0.25) * x ** 2.5
    peak = np.max(np.abs(fx))
    return fx / peak * 0.8 if peak > 0 else fx


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("seconds", type=float)
    ap.add_argument("--mood", default="hype", choices=sorted(MOODS))
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--events", default=None, help="JSON file with impact/whoosh/riser times")
    a = ap.parse_args()
    x = render_hype(a.seconds, a.seed) if a.mood == "hype" else render(a.seconds, a.mood, a.seed)
    if a.events:
        ev = json.load(open(a.events, encoding="utf-8"))
        x = x + 0.55 * render_events(a.seconds, ev, a.seed)
        x /= max(np.max(np.abs(x)), 1e-6) / 0.8
    st = np.stack([x, np.roll(x, int(0.012 * SR))], axis=1)  # slight stereo width
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())
    print(a.out)


if __name__ == "__main__":
    main()

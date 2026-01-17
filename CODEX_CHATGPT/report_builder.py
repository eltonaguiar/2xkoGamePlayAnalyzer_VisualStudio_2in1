"""Report builders for HTML and lightweight PDF."""

import os
from pathlib import Path
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont


DEFAULT_COLORS = ("#1f77b4", "#d62728")  # blue, red
PLACEHOLDER_BG = "#0b0c10"


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def _color_block(color: str) -> str:
    return f"<span style='display:inline-block;width:12px;height:12px;background:{color};margin-right:8px;border-radius:3px;'></span>"


def generate_placeholder_portrait(path: str, name: str, color: str) -> str:
    """Create a simple color-backed portrait if no art is available."""
    ensure_dir(os.path.dirname(path))
    img = Image.new("RGB", (320, 380), color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = name
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.rectangle((10, 10, 310, 370), outline="#0b0c10", width=4)
    draw.text(((320 - tw) // 2, (380 - th) // 2), text, font=font, fill="#0b0c10")
    img.save(path)
    return path


def build_html_report(
    result: Dict,
    output_dir: str,
    video_path: str,
    player1: str,
    player2: str,
    color1: str,
    color2: str,
    start_pos1: str,
    start_pos2: str,
    img1_path: str,
    img2_path: str,
    fps: float,
    char1_img: str,
    char2_img: str,
    clip_paths: List[str],
) -> str:
    """Create an HTML report with embedded video tag and event tables."""
    ensure_dir(output_dir)
    video_uri = Path(video_path).absolute().as_uri()
    html_path = os.path.join(output_dir, "blitz_mirror_report.html")
    events: List[Dict] = result.get("events", [])
    mistakes: List[Dict] = result.get("mistakes", [])
    knowledge: Dict = result.get("knowledge", {})
    player_summary: Dict = result.get("player_summary", {})
    def rel_link(path_str: str) -> str:
        """Return path relative to output_dir for stable local links."""
        try:
            return Path(os.path.abspath(path_str)).relative_to(Path(output_dir).resolve()).as_posix()
        except Exception:
            return Path(path_str).as_posix()

    def render_mistake_row(m):
        player = m.get("player", 1)
        color = color1 if player == 1 else color2
        name = m.get("player_name", f"P{player}")
        ts = m.get("timestamp", "")
        full_ts = m.get("full_timestamp", ts)
        sec = m.get("seconds", None)
        sec_attr = f" data-sec='{sec}'" if sec is not None else ""
        punished = "Yes" if m.get("punished") else "No/Unknown"
        punish_info = f"{punished} ({m.get('punish_damage','~')} dmg)"
        return (
            f"<tr>"
            f"<td>{_color_block(color)}P{player}: {name} ({m.get('character','')})</td>"
            f"<td>R{m.get('round','?')} @ <a href='#' class='jump' data-ts='{ts}'{sec_attr} title='Exact time: {full_ts}'>{ts}</a></td>"
            f"<td>{m.get('title','')}</td>"
            f"<td>{m.get('detail','')}<br/><small>{m.get('range_note','')}</small></td>"
            f"<td>{m.get('damage_estimate','~')} dmg</td>"
            f"<td>{m.get('severity','')} ({m.get('impact','')})</td>"
            f"<td>{punish_info}<br/><small>{m.get('opponent_response','')}<br/>String: {m.get('opponent_string','')}</small></td>"
            f"<td>{'; '.join(m.get('recommendations', [])[:2])}</td>"
            f"</tr>"
        )

    def generate_loser_mistakes_html(mistakes, winners, p1, p2):
        loser = None
        ow = winners.get("overall_winner", 0)
        if ow == 1:
            loser = 2
        elif ow == 2:
            loser = 1
        if loser is None:
            return "<p>No clear loser (tie/unknown).</p>"
        loser_name = p1 if loser == 1 else p2
        loser_color = color1 if loser == 1 else color2
        filtered = [m for m in mistakes if m.get("player") == loser and m.get("severity") in ("critical", "major")]
        filtered = sorted(filtered, key=lambda x: -(x.get("punish_damage") or x.get("damage_estimate", 0)))[:5]
        if not filtered:
            return f"<p>No major mistakes detected for {loser_name} (P{loser}) with current heuristics.</p>"
        rows = []
        for m in filtered:
            ts = m.get("timestamp", "")
            rows.append(
                f"<tr>"
                f"<td>{_color_block(loser_color)}P{loser} {loser_name}</td>"
                f"<td><a href='#' class='jump' data-ts='{ts}' data-sec='{m.get('seconds','')}' title='Exact time: {m.get('full_timestamp', ts)}'>{ts}</a></td>"
                f"<td>{m.get('title','')}</td>"
                f"<td>{m.get('opponent_string','')}</td>"
                f"<td>{m.get('punish_damage','~')} dmg</td>"
                f"</tr>"
            )
        table = "<table><tr><th>Player</th><th>Time</th><th>Mistake</th><th>Opponent String</th><th>Est. Damage</th></tr>" + "".join(rows) + "</table>"
        return table

    def render_event_row(e):
        return (
            f"<tr>"
            f"<td>{e.get('timestamp','')}</td>"
            f"<td>{e.get('tag','')}</td>"
            f"<td>{e.get('intensity','')}</td>"
            f"<td>{e.get('motion','')}</td>"
            f"<td>{round(e.get('confidence',0)*100,1)}%</td>"
            f"</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>2XKO Blitz Mirror Analysis</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #0b0c10; color: #e6e6e6; }}
    h1, h2, h3 {{ color: #f5f5f5; }}
    .panel {{ background: #111722; border: 1px solid #233044; border-radius: 10px; padding: 16px; margin-bottom: 18px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #233044; padding: 8px; text-align: left; }}
    th {{ background: #182335; }}
    .tag {{ padding: 4px 8px; border-radius: 6px; background: #233044; font-size: 12px; }}
    .badge {{ padding: 4px 8px; border-radius: 6px; }}
    .p1 {{ background:{color1}; color:#0b0c10; }}
    .p2 {{ background:{color2}; color:#0b0c10; }}
    .chips span {{ display:inline-block; margin-right:8px; padding:4px 8px; border-radius:5px; background:#233044; }}
    a.jump {{ color:#5dade2; text-decoration:none; }}
    a.jump:hover {{ text-decoration:underline; }}
  </style>
</head>
<body>
  <h1>2XKO Blitzcrank Mirror (Juggernaut)</h1>
  <div class="panel">
    <h3>Video</h3>
    <video id="matchVideo" width="100%" controls src="{video_uri}">Your browser does not support video.</video>
    <p style="margin-top:8px;">{video_path}</p>
  </div>

  <div class="panel">
    <h3>Key Clips (critical/major)</h3>
    <ul style="font-size:15px;">
      {''.join(f"<li><a href='{rel_link(cp)}' target='_blank'>{Path(cp).name}</a></li>" for cp in clip_paths[:5]) if clip_paths else '<li>No clips exported for current thresholds.</li>'}
    </ul>
    <p style="font-size:12px;color:#9ea3aa;">Click to open top mistake clips in a new tab.</p>
  </div>

  <div class="panel">
    <h3>Players</h3>
    <div class="chips">
      <span class="badge p1">{_color_block(color1)}P1: {player1} - {start_pos1}</span>
      <span class="badge p2">{_color_block(color2)}P2: {player2} - {start_pos2}</span>
    </div>
    <div style="display:flex;gap:16px;margin-top:12px;flex-wrap:wrap;">
      <div style="flex:1;min-width:220px;text-align:center;">
        <img src="{Path(img1_path).absolute().as_uri()}" alt="{player1}" style="max-width:100%;border:1px solid #233044;border-radius:8px;"/>
        <div class="badge p1" style="display:inline-block;margin-top:6px;">Color: {color1}</div>
        <div style="margin-top:8px;"><img src="{Path(char1_img).absolute().as_uri()}" alt="Character P1" style="max-width:100%;border:1px solid #233044;border-radius:8px;"/></div>
      </div>
      <div style="flex:1;min-width:220px;text-align:center;">
        <img src="{Path(img2_path).absolute().as_uri()}" alt="{player2}" style="max-width:100%;border:1px solid #233044;border-radius:8px;"/>
        <div class="badge p2" style="display:inline-block;margin-top:6px;">Color: {color2}</div>
        <div style="margin-top:8px;"><img src="{Path(char2_img).absolute().as_uri()}" alt="Character P2" style="max-width:100%;border:1px solid #233044;border-radius:8px;"/></div>
      </div>
    </div>
  </div>

  <div class="panel">
    <h3>Key Mistakes (ranked by severity)</h3>
    <table>
      <tr><th>Player</th><th>Round/Time</th><th>Title</th><th>Detail + Range</th><th>Damage Est.</th><th>Severity</th><th>Punish</th><th>Recommendations</th></tr>
      {''.join(render_mistake_row(m) for m in mistakes)}
    </table>
  </div>

  <div class="panel">
    <h3>Event Timeline (sampled)</h3>
    <table>
      <tr><th>Time</th><th>Tag</th><th>Flash</th><th>Motion</th><th>Conf.</th></tr>
      {''.join(render_event_row(e) for e in events[:150])}
    </table>
  </div>

  <div class="panel">
    <h3>Player Tendencies</h3>
    <ul>
      <li>P1 ({player1}): {player_summary.get(1,{}).get('style','Unknown')} | spikes={player_summary.get(1,{}).get('events',0)} | big_commits={player_summary.get(1,{}).get('big_commits',0)}</li>
      <li>P2 ({player2}): {player_summary.get(2,{}).get('style','Unknown')} | spikes={player_summary.get(2,{}).get('events',0)} | big_commits={player_summary.get(2,{}).get('big_commits',0)}</li>
    </ul>
  </div>

  <div class="panel">
    <h3>Move Variety (heuristic counts)</h3>
    <table>
      <tr><th>Player</th><th>Move</th><th>Estimated Uses</th></tr>
      {''.join(f"<tr><td>P1 {player1}</td><td>{mv['move']}</td><td>{mv['uses']}</td></tr>" for mv in result.get('move_variety',{}).get(1,[]))}
      {''.join(f"<tr><td>P2 {player2}</td><td>{mv['move']}</td><td>{mv['uses']}</td></tr>" for mv in result.get('move_variety',{}).get(2,[]))}
    </table>
    <p style="font-size:12px;color:#9ea3aa;">Move IDs require telemetry; counts are heuristic based on activity spikes.</p>
  </div>

  <div class="panel">
    <h3>Mistakes by Round (categorized)</h3>
    <table>
      <tr><th>Round</th><th>Player</th><th>Time</th><th>Title</th><th>Severity</th><th>Punish?</th></tr>
      {''.join(f"<tr><td>{m.get('round','?')}</td><td>P{m.get('player','?')} {m.get('player_name','')}</td><td><a href='#' class='jump' data-ts='{m.get('timestamp','')}' data-sec='{m.get('seconds','')}' title='Exact time: {m.get('full_timestamp', m.get('timestamp',''))}'>{m.get('timestamp','')}</a></td><td>{m.get('title','')}</td><td>{m.get('severity','')}</td><td>{'Yes' if m.get('punished') else 'No/Unknown'}</td></tr>" for m in mistakes)}
    </table>
  </div>

  <div class="panel">
    <h3>Round Results (heuristic)</h3>
    <ul>
      {''.join(f"<li>Round {rnd}: Winner = {'P1 '+player1 if win==1 else 'P2 '+player2 if win==2 else 'Tie/Unknown'}</li>" for rnd, win in result.get('winners',{}).get('round_winners', {}).items())}
    </ul>
    <p><strong>Round Tally (heuristic):</strong> P1 {result.get('winners',{}).get('p1_rounds',0)} - P2 {result.get('winners',{}).get('p2_rounds',0)}</p>
    <p><strong>Overall (heuristic):</strong> { 'P1 '+player1 if result.get('winners',{}).get('overall_winner',0)==1 else 'P2 '+player2 if result.get('winners',{}).get('overall_winner',0)==2 else 'Tie/Unknown' }</p>
    <p style="font-size:12px;color:#9ea3aa;">Round winners are estimated from activity density (no HUD data).</p>
  </div>

  <div class="panel">
    <h3>Top Mistakes from the Losing Side</h3>
    {generate_loser_mistakes_html(mistakes, result.get('winners',{}), player1, player2)}
  </div>

  <div class="panel">
    <h3>Fast Reference</h3>
    <p><strong>Unsafe on block:</strong> {knowledge.get('unsafe_moves','')[:8]}</p>
    <p><strong>Safe pressure:</strong> {knowledge.get('safe_pressure','')}</p>
    <p><strong>Preferred punishes:</strong> {knowledge.get('preferred_punishes','')}</p>
    <p><strong>Juggernaut notes:</strong> {knowledge.get('juggernaut_notes','')}</p>
  </div>

  <div class="panel">
    <h3>Mistake Clips</h3>
    <ul>
      {''.join(f"<li><a href='{Path(cp).as_posix()}' target='_blank'>{Path(cp).name}</a></li>" for cp in clip_paths) if clip_paths else '<li>No clips exported for current thresholds.</li>'}
    </ul>
    <p style="font-size:12px;color:#9ea3aa;">Clips include critical/major mistakes; adjust clip length via --clip-pre/--clip-post.</p>
  </div>
  <div class="panel">
    <h3>Move Glossary (plain language)</h3>
    <ul>
      <li><strong>5L / 2L</strong>: fast light jab/low poke, safest check.</li>
      <li><strong>5S1 (Rocket Grab)</strong>: long tether that pulls on hit/block, + on block.</li>
      <li><strong>5S2 (Rocket Punch)</strong>: long-range strike, unsafe on block (-15).</li>
      <li><strong>2S2 (Garbage Collection)</strong>: close command grab; armored when empowered.</li>
      <li><strong>66H</strong>: running strike that low-crushes, hits OTG, -9 on block.</li>
      <li><strong>2H</strong>: main anti-air uppercut launcher, very unsafe on block.</li>
      <li><strong>Super1 (Helping Hand)</strong>: super that charges steam, ground bounce on hit.</li>
      <li><strong>Super2 (Static Field)</strong>: large AoE field super, very punishable on block.</li>
      <li><strong>Meter/Bar Spend</strong>: using supers/empowered specials; track steam usage.</li>
    </ul>
  </div>
  <script>
    const fps = {fps if fps else 30};
    function tsToSeconds(ts) {{
      // Accept MM:SS or MM:SS.t
      if (ts.includes('.')) {{
        const [mmss, tenths] = ts.split('.');
        const [mm, ss] = mmss.split(':').map(x => parseInt(x || '0', 10));
        return mm * 60 + ss + (parseInt(tenths || '0', 10) / 10);
      }}
      const parts = ts.split(':');
      if (parts.length < 2) return 0;
      const [mm, ss] = parts.map(p => parseInt(p || '0', 10));
      return mm * 60 + ss;
    }}
    function setupJumps() {{
      const video = document.getElementById('matchVideo');
      document.querySelectorAll('a.jump').forEach(el => {{
        el.addEventListener('click', (e) => {{
          e.preventDefault();
          if (!video) return;
          const secAttr = el.getAttribute('data-sec');
          const ts = el.getAttribute('data-ts') || '00:00';
          const target = secAttr && !Number.isNaN(parseFloat(secAttr)) ? parseFloat(secAttr) : tsToSeconds(ts);
          video.currentTime = target;
          video.play();
        }});
      }});
    }}
    document.addEventListener('DOMContentLoaded', setupJumps);
  </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path


def build_pdf_report(result: Dict, output_dir: str, player1: str, player2: str) -> str:
    """Create a simple PDF snapshot from text using Pillow (lightweight)."""
    ensure_dir(output_dir)
    pdf_path = os.path.join(output_dir, "blitz_mirror_report.pdf")
    mistakes: List[Dict] = result.get("mistakes", [])[:20]
    lines = ["2XKO Blitzcrank Mirror (Juggernaut)", f"P1: {player1} | P2: {player2}", ""]
    for m in mistakes:
        lines.append(
            f"R{m.get('round','?')} [{m.get('timestamp','')}] P{m.get('player',1)} {m.get('player_name','')}: {m.get('title','')} (sev: {m.get('severity','')}, punished: {'Yes' if m.get('punished') else 'No/Unknown'})"
        )
        recs = "; ".join(m.get("recommendations", [])[:2])
        if recs:
            lines.append(f"  -> {recs}")
        rng = m.get("range_note", "")
        dmg = m.get("damage_estimate", "~")
        opp = m.get("opponent_response", "")
        lines.append(f"  spacing: {rng} | est dmg: {dmg} | opp: {opp}")
    knowledge: Dict = result.get("knowledge", {})
    lines.append("")
    winners = result.get("winners", {})
    rw = winners.get("round_winners", {})
    ow = winners.get("overall_winner", 0)
    if rw:
        lines.append("Round Results (heuristic):")
        for rnd, win in rw.items():
            if win == 1:
                lines.append(f"  Round {rnd}: P1 {player1}")
            elif win == 2:
                lines.append(f"  Round {rnd}: P2 {player2}")
            else:
                lines.append(f"  Round {rnd}: Tie/Unknown")
    lines.append(f"Round tally (heuristic): P1 {winners.get('p1_rounds',0)} - P2 {winners.get('p2_rounds',0)}")
    if ow:
        lines.append(f"Overall (heuristic): {'P1 '+player1 if ow==1 else 'P2 '+player2}")
    lines.append(f"Unsafe: {knowledge.get('unsafe_moves','')[:6]}")
    lines.append(f"Safe pressure: {knowledge.get('safe_pressure','')}")
    lines.append(f"Punishes: {knowledge.get('preferred_punishes','')}")

    # Render text into an image and save as PDF
    font = ImageFont.load_default()
    padding = 20
    line_height = font.getbbox("Ag")[3] + 6
    width = 1200
    height = padding * 2 + line_height * max(12, len(lines))
    img = Image.new("RGB", (width, height), color="#0b0c10")
    draw = ImageDraw.Draw(img)
    y = padding
    for line in lines:
        draw.text((padding, y), line, font=font, fill="#e6e6e6")
        y += line_height
    img.save(pdf_path, "PDF", resolution=150.0)
    return pdf_path

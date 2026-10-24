#!/usr/bin/env python3
"""
Markdown -> formatted HTML converter (business-modern style)
Following doc-typeset SKILL.md + business-report prompt rules.
v2: fixed html-review issues (bare spacing -> CSS vars, added executive summary)
"""
import re, os, sys, html

MD_PATH = r"C:\Users\Su\Desktop\完美假日\output\merged\车记得_v2_合并方案.md"
OUT_HTML = r"C:\Users\Su\Desktop\完美假日\output\merged\v2-merge-20261010\stage2\formatted-车记得v2.html"

def read_md(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def esc(text):
    return html.escape(text, quote=False)

def inline_format(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

def parse_table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\|[\s\-:|]+\|?$', line):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return ''
    html_parts = ['<table>']
    html_parts.append('<thead><tr>')
    for cell in rows[0]:
        html_parts.append(f'<th>{inline_format(cell)}</th>')
    html_parts.append('</tr></thead>')
    html_parts.append('<tbody>')
    for row in rows[1:]:
        html_parts.append('<tr>')
        for cell in row:
            html_parts.append(f'<td>{inline_format(cell)}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody></table>')
    return ''.join(html_parts)

def parse_list(lines, ordered=False):
    tag = 'ol' if ordered else 'ul'
    items = []
    for line in lines:
        line = line.strip()
        m = re.match(r'^[-*]\s+(.*)' if not ordered else r'^\d+\.\s+(.*)', line)
        if m:
            items.append(m.group(1))
    if not items:
        return ''
    html_parts = [f'<{tag}>']
    for item in items:
        html_parts.append(f'<li>{inline_format(item)}</li>')
    html_parts.append(f'</{tag}>')
    return ''.join(html_parts)

def parse_blockquote(lines):
    content_lines = []
    for line in lines:
        line = re.sub(r'^>\s?', '', line)
        content_lines.append(line)
    content = '\n'.join(content_lines).strip()
    if not content:
        return ''
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    html_parts = []
    # Use CSS variables for spacing - no bare values
    html_parts.append('<div style="border-left:var(--border-heading-w) solid var(--color-primary);background:var(--color-surface);padding:var(--callout-pad);margin:var(--callout-margin);">')
    for para in paragraphs:
        para = para.replace('\n', '<br>')
        html_parts.append(f'<p style="margin:0 0 var(--callout-para-gap) 0;">&nbsp;&nbsp;{inline_format(para)}</p>')
    if html_parts and html_parts[-1].startswith('<p style="margin:0 0'):
        html_parts[-1] = html_parts[-1].replace('margin:0 0 var(--callout-para-gap) 0', 'margin:0')
    html_parts.append('</div>')
    return ''.join(html_parts)

def convert_md_to_html(md_text):
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    cover_title = ""
    cover_subtitle = ""

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('# ') and not stripped.startswith('## '):
            cover_title = stripped[2:].strip()
            i += 1
            while i < len(lines) and lines[i].strip().startswith('**') and lines[i].strip().endswith('**'):
                cover_subtitle = lines[i].strip().strip('*')
                i += 1
                break
            continue

        if stripped.startswith('## '):
            title = stripped[3:].strip()
            html_parts.append(f'<h2>{inline_format(title)}</h2>')
            i += 1
            continue

        if stripped.startswith('### ') and not stripped.startswith('#### '):
            title = stripped[4:].strip()
            html_parts.append(f'<h3>{inline_format(title)}</h3>')
            i += 1
            continue

        if stripped.startswith('#### '):
            title = stripped[5:].strip()
            html_parts.append(f'<h4>{inline_format(title)}</h4>')
            i += 1
            continue

        if re.match(r'^-{3,}$', stripped) or re.match(r'^\*{3,}$', stripped):
            html_parts.append('<hr style="border:none;border-top:var(--border-divider-w) solid var(--color-divider);margin:var(--hr-margin);">')
            i += 1
            continue

        if stripped.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|?$', lines[i+1].strip()):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(parse_table(table_lines))
            continue

        if stripped.startswith('>'):
            bq_lines = []
            while i < len(lines) and (lines[i].strip().startswith('>') or (lines[i].strip() == '' and i+1 < len(lines) and lines[i+1].strip().startswith('>'))):
                bq_lines.append(lines[i])
                i += 1
            html_parts.append(parse_blockquote(bq_lines))
            continue

        if re.match(r'^\d+\.\s+', stripped):
            list_lines = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i].strip()):
                list_lines.append(lines[i])
                i += 1
            html_parts.append(parse_list(list_lines, ordered=True))
            continue

        if re.match(r'^[-*]\s+', stripped):
            list_lines = []
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i].strip()):
                list_lines.append(lines[i])
                i += 1
            html_parts.append(parse_list(list_lines, ordered=False))
            continue

        if not stripped:
            i += 1
            continue

        para_lines = []
        while i < len(lines):
            l = lines[i].strip()
            if not l:
                break
            if l.startswith('#') or l.startswith('|') or l.startswith('>') or l.startswith('- ') or l.startswith('* '):
                break
            if re.match(r'^\d+\.\s+', l):
                break
            if re.match(r'^-{3,}$', l):
                break
            para_lines.append(lines[i])
            i += 1

        if para_lines:
            para_text = ' '.join(l.strip() for l in para_lines)
            html_parts.append(f'<p>{inline_format(para_text)}</p>')

    return cover_title, cover_subtitle, '\n'.join(html_parts)

def build_toc(md_text):
    toc_items = []
    for line in md_text.split('\n'):
        line = line.strip()
        if line.startswith('## ') and not line.startswith('### '):
            title = line[3:].strip()
            title = re.sub(r'\*\*(.+?)\*\*', r'\1', title)
            toc_items.append(title)
    items_html = []
    for idx, title in enumerate(toc_items, 1):
        items_html.append(f'<li>{esc(title)}</li>')
    return '\n'.join(items_html)

def build_executive_summary():
    """Build executive summary section with key highlights."""
    return '''<div class="executive-summary">
  <div class="summary-header">
    <h2>执行摘要</h2>
  </div>
  <div class="summary-body">
    <p>「车记得」是面向完美金鹰&middot;假日商圈的智慧停车解决方案，复用商场已有 CCTV 监控系统实现车牌自动识别与车位绑定，车主返程输入车牌号即可一键寻车。方案零新增硬件、零施工、零道闸改造，通过双轨设计（监控自动识别 + 二维码/拍照 AI 兜底）保证功能可用性。</p>
    <p>商圈年客流超 <strong>3000 万人次</strong>、会员规模突破 <strong>80 万人</strong>，跨场停车认知断层是真实痛点。方案涵盖监控识别、多模态 AI 视觉理解、生成式表达、对话式语义检索、行程级规划五大能力，决赛一天可在主办方真实车库做出可运行原型，赛后两周内单层试点实测。</p>
  </div>
</div>'''

def build_full_html(cover_title, cover_subtitle, body_html, toc_html):
    # Extract appendix
    appendix_match = re.search(r'(<hr[^>]*>)?\s*<h3>附[:：]数据来源</h3>(.*)$', body_html, re.DOTALL)
    appendix_html = ""
    main_html = body_html
    if appendix_match:
        appendix_html = '<h3>附：数据来源</h3>' + appendix_match.group(2).strip()
        main_html = body_html[:appendix_match.start()].rstrip()
        main_html = re.sub(r'(<hr[^>]*>\s*)$', '', main_html)

    exec_summary = build_executive_summary()

    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="docx-page-size" content="A4">
  <title>{esc(cover_title)}</title>
  <style>
  @page {{
    @bottom-center {{ content: counter(page); }}
  }}
  @page cover {{
    @bottom-center {{ content: none; }}
  }}
  section[role="cover"] {{ page: cover; }}

  :root {{
    /* Typography */
    --fs-h1: var(--typography-fontSize-h1, 20pt);
    --fs-h2: var(--typography-fontSize-h2, 16pt);
    --fs-h3: var(--typography-fontSize-h3, 14pt);
    --fs-body: var(--typography-fontSize-body, 11pt);
    --fs-small: var(--typography-fontSize-small, 10pt);
    --fs-tiny: var(--typography-fontSize-tiny, 9pt);
    --ff-heading: var(--typography-fontFamily-heading, "微软雅黑", sans-serif);
    --ff-body: var(--typography-fontFamily-body, "微软雅黑", sans-serif);
    --ff-mono: var(--typography-fontFamily-code, "Consolas", monospace);
    --lh-body: var(--typography-lineHeight-body, 1.6);
    --lh-compact: var(--typography-lineHeight-compact, 1.2);
    --fw-heading: var(--typography-fontWeight-heading, 600);
    --fw-body: var(--typography-fontWeight-body, 400);
    /* Color */
    --color-primary: #1565C0;
    --color-secondary: #0288D1;
    --color-accent: #00897B;
    --color-text: #212121;
    --color-textSecondary: #616161;
    --color-heading: #1A237E;
    --color-divider: #E0E0E0;
    --color-background: #FFFFFF;
    --color-surface: #F5F7FA;
    --color-emphasis: #C62828;
    /* Spacing - all via CSS variables, no bare values */
    --spacing-paragraph: 0.75em;
    --spacing-section: 2.5em;
    --spacing-block: 1em;
    --margin-page: 2.5cm;
    --page-content-width: 16cm;
    /* Component-specific spacing vars */
    --border-heading-w: 4px;
    --border-divider-w: 1px;
    --callout-pad: 12px 16px;
    --callout-margin: 0.75em 0;
    --callout-para-gap: 0.5em;
    --hr-margin: 1.5em 0;
    --table-cell-pad: 6px 10px;
    --code-pad: 1px 4px;
    --summary-border-w: 4px;
    --summary-pad: 1em 1.5em;
    --summary-margin: 1.5em 0;
    --cover-gap-title: 0.8em;
    --cover-gap-cat: 1.5em;
    --cover-gap-sub: 2em;
    --cover-gap-meta: 3em;
    --toc-pad-v: 1.5em;
    --toc-gap: 0.8em;
    --toc-item-gap: 0.4em;
    --h2-mt: 2em;
    --h2-mb: 0.8em;
    --h3-mt: 1.5em;
    --h3-mb: 0.6em;
    --h4-mt: 1em;
    --h4-mb: 0.5em;
    --table-margin: 1em 0;
    --list-margin: 0.5em 0 0.75em 1.5em;
    --list-item-gap: 0.3em;
    --appendix-pad: 2em 0 1em 0;
    --appendix-para-gap: 0.4em;
    --body-pad: 1em 0;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: var(--ff-body);
    font-size: var(--fs-body);
    line-height: var(--lh-body);
    color: var(--color-text);
    background: var(--color-background);
    max-width: var(--page-content-width);
    margin: 0 auto;
  }}

  /* Cover */
  .report-cover {{
    min-height: 50vh;
    padding: var(--margin-page);
    background: var(--color-surface);
    text-align: center;
  }}
  .cover-category {{
    font-size: var(--fs-h3);
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-primary);
    letter-spacing: 0.08em;
    margin-bottom: var(--cover-gap-cat);
    text-align: center;
  }}
  .cover-title {{
    font-size: var(--fs-h1);
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-primary);
    margin-bottom: var(--cover-gap-title);
    line-height: 1.4;
    text-align: center;
  }}
  .cover-subtitle {{
    font-size: var(--fs-h3);
    color: var(--color-textSecondary);
    margin-bottom: var(--cover-gap-sub);
    text-align: center;
    line-height: 1.6;
  }}
  .cover-meta {{
    font-size: var(--fs-small);
    color: var(--color-textSecondary);
    text-align: center;
    margin-top: var(--cover-gap-meta);
  }}
  .cover-meta p {{
    text-align: center;
    margin-bottom: var(--list-item-gap);
  }}

  /* TOC */
  .doc-toc {{
    padding: var(--toc-pad-v) 0;
    background: var(--color-background);
    border-bottom: var(--border-heading-w) solid var(--color-primary);
    margin-bottom: var(--cover-gap-sub);
  }}
  .toc-title {{
    font-size: var(--fs-h2);
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-heading);
    margin-bottom: var(--toc-gap);
  }}
  .toc-list, .toc-list ol, .toc-list ul {{
    list-style: none;
    list-style-type: none;
    padding-left: 0;
  }}
  .toc-list li {{
    margin-bottom: var(--toc-item-gap);
    text-indent: 0;
    font-size: var(--fs-body);
    line-height: 1.8;
  }}

  /* Executive Summary */
  .executive-summary {{
    margin: var(--summary-margin);
    padding: var(--summary-pad);
    border-left: var(--summary-border-w) solid var(--color-primary);
    background: var(--color-surface);
  }}
  .executive-summary h2 {{
    border-left: none;
    padding-left: 0;
    margin-top: 0;
    color: var(--color-primary);
  }}
  .executive-summary p {{
    margin-bottom: var(--spacing-paragraph);
  }}

  /* Body content */
  .report-body {{
    padding: var(--body-pad);
  }}
  .report-body h2 {{
    font-size: var(--fs-h2);
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-heading);
    border-left: var(--border-heading-w) solid var(--color-primary);
    padding-left: 12px;
    margin-top: var(--h2-mt);
    margin-bottom: var(--h2-mb);
    line-height: 1.4;
  }}
  .report-body h3 {{
    font-size: var(--fs-h3);
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-heading);
    margin-top: var(--h3-mt);
    margin-bottom: var(--h3-mb);
    line-height: 1.4;
  }}
  .report-body h4 {{
    font-size: var(--fs-body);
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-heading);
    margin-top: var(--h4-mt);
    margin-bottom: var(--h4-mb);
  }}
  .report-body p {{
    font-size: var(--fs-body);
    line-height: var(--lh-body);
    color: var(--color-text);
    margin-bottom: var(--spacing-paragraph);
    text-align: justify;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: var(--table-margin);
    font-size: var(--fs-small);
    line-height: var(--lh-compact);
  }}
  table th {{
    background: var(--color-surface);
    border: var(--border-divider-w) solid var(--color-divider);
    padding: var(--table-cell-pad);
    text-align: left;
    font-family: var(--ff-heading);
    font-weight: var(--fw-heading);
    color: var(--color-heading);
    font-size: var(--fs-small);
  }}
  table td {{
    border: var(--border-divider-w) solid var(--color-divider);
    padding: var(--table-cell-pad);
    font-size: var(--fs-small);
    color: var(--color-text);
    vertical-align: top;
  }}
  table tbody tr:nth-child(even) {{
    background: var(--color-surface);
  }}

  /* Lists */
  ul, ol {{
    margin: var(--list-margin);
  }}
  li {{
    margin-bottom: var(--list-item-gap);
    font-size: var(--fs-body);
    line-height: var(--lh-body);
    color: var(--color-text);
  }}

  /* Inline code */
  code {{
    font-family: var(--ff-mono);
    font-size: var(--fs-small);
    background: var(--color-surface);
    padding: var(--code-pad);
  }}

  /* Strong */
  strong {{
    font-weight: 700;
    color: var(--color-heading);
  }}

  /* Divider */
  hr {{
    border: none;
    border-top: var(--border-divider-w) solid var(--color-divider);
    margin: var(--hr-margin);
  }}

  /* Appendix */
  .appendix {{
    padding: var(--appendix-pad);
    border-top: var(--border-heading-w) solid var(--color-divider);
    margin-top: var(--h2-mt);
  }}
  .appendix h2 {{
    border-left: var(--border-heading-w) solid var(--color-textSecondary);
    color: var(--color-textSecondary);
  }}
  .appendix h3 {{
    color: var(--color-textSecondary);
  }}
  .appendix p {{
    font-size: var(--fs-small);
    color: var(--color-textSecondary);
    line-height: 1.5;
    margin-bottom: var(--appendix-para-gap);
  }}
  .appendix ul {{
    font-size: var(--fs-small);
    color: var(--color-textSecondary);
  }}
  .appendix li {{
    font-size: var(--fs-small);
    color: var(--color-textSecondary);
    margin-bottom: var(--list-item-gap);
  }}
  </style>
</head>
<body>
  <section role="cover" class="report-cover">
    <p class="cover-category">参赛项目方案</p>
    <h1 class="cover-title">{esc(cover_title)}</h1>
    <p class="cover-subtitle">{inline_format(cover_subtitle)}</p>
    <div class="cover-meta">
      <p>完美金鹰&middot;假日商圈 AI 大赛</p>
      <p>赛道二：商圈服务 &middot; 用户体验</p>
      <p>2026 年 10 月</p>
    </div>
  </section>

  <section role="body" class="report-body" data-page-restart="1">
    <nav class="doc-toc" aria-label="文档目录">
      <p class="toc-title">目录</p>
      <ol class="toc-list">
{toc_html}
      </ol>
    </nav>

{exec_summary}

    <main>
{main_html}
    </main>

    <div class="appendix">
{appendix_html if appendix_html else '<p>&nbsp;</p>'}
    </div>
  </section>
</body>
</html>'''
    return full_html

def main():
    md_text = read_md(MD_PATH)
    cover_title, cover_subtitle, body_html = convert_md_to_html(md_text)

    if not cover_subtitle:
        cover_subtitle = "参赛项目方案 · 完美金鹰·假日商圈 AI 大赛 · 赛道二：商圈服务 · 用户体验"

    toc_html = build_toc(md_text)
    full_html = build_full_html(cover_title, cover_subtitle, body_html, toc_html)

    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"HTML written: {OUT_HTML}")
    print(f"Size: {os.path.getsize(OUT_HTML)} bytes")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""security-design の入口に固有の構造を検査する。配置と manifest は harness-tools の validate-plugin-repository.py が判定するので、ここでは見ない。

基準資料: 各入口の SKILL.md、package の中の Markdown
入力: 絶対パスで渡された repository。frontmatter の YAML は mikefarah/yq v4 で読む
合格述語:
  1. 各入口の SKILL.md の frontmatter が閉じていて、description が空でない。SKILL.md に shell のコードブロックが無い
  2. package の Markdown に Gherkin（Feature:、Scenario:、```gherkin）が無い
  3. package の Markdown の相対リンクは、そのファイルと同じ入口（skills/<entry>/）の中の実在するファイルを指す。
     入口は自分のファイルだけで仕事を終えるので、兄弟の入口のファイルへリンクしない
失敗時の診断: 違反したファイルと理由
正例: この repository の配布物そのもの
反例: test-package.py の負例（description の欠落、shell のコードブロック、Gherkin、切れたリンク）
意味評価として残す範囲: 守るものの決め方、層ごとの脅威と対策の妥当性、利用者へ問う論点の選び方
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

PACKAGE = 'plugins/security-design'


def require(condition, path, message):
    if not condition:
        raise ValueError(f'{path}: {message}')


def yaml_value(text, path):
    result = subprocess.run(['yq', '-o=json', '.', '-'], input=text,
                            text=True, capture_output=True, check=False)
    require(result.returncode == 0, path, 'invalid YAML: ' + result.stderr.strip())
    return json.loads(result.stdout)


def validate(root):
    package = root / PACKAGE
    entries = sorted(p for p in (package / 'skills').iterdir() if p.is_dir())
    require(entries, package, 'no entry')
    for entry in entries:
        path = entry / 'SKILL.md'
        text = path.read_text()
        match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
        require(match is not None, path, 'frontmatter missing')
        metadata = yaml_value(match.group(1), path)
        require(isinstance(metadata, dict) and isinstance(metadata.get('description'), str) and bool(metadata['description']), path, 'description missing')
        require(not re.search(r'^```(?:bash|sh|shell)\b', text, re.M), path, 'shell block forbidden')
    for path in package.rglob('*.md'):
        text = path.read_text()
        require(not re.search(r'^\s*(?:Feature:|Scenario:|```gherkin)', text, re.M), path, 'Gherkin は配布物に置かない')
        parts = path.relative_to(package).parts
        home = package / parts[0] / parts[1] if parts[0] == 'skills' and len(parts) > 2 else package
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if '://' in link or link.startswith('#'):
                continue
            target = (path.parent / link.split('#', 1)[0]).resolve()
            require(target.is_relative_to(home.resolve()) and target.is_file(), path, f'link missing or outside entry: {link}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', type=Path)
    args = parser.parse_args()
    try:
        require(args.repository.is_absolute(), args.repository, 'absolute repository required')
        validate(args.repository)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'Package structure: passed ({args.repository})')
    return 0


if __name__ == '__main__':
    sys.exit(main())

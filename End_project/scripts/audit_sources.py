"""重新校验真实下载的四表，并比较 Kaggle 与固定提交镜像的 CSV 内容。"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from fetch_olist import FILES


def inspect(root):
    manifest = json.loads((root / 'source_manifest.json').read_text())
    if set(manifest['files']) != set(FILES) or manifest.get('errors'):
        raise ValueError(f'源清单不完整: {root}')
    result, content = {}, {}
    for role, name in FILES.items():
        data = (root / name).read_bytes()
        entry = manifest['files'][role]
        digest = hashlib.sha256(data).hexdigest()
        with (root / name).open(newline='', encoding='utf-8-sig') as stream:
            rows = list(csv.DictReader(stream))
        if digest != entry['sha256'] or len(rows) != entry['rows'] or len(data) != entry['bytes']:
            raise ValueError(f'源文件哈希、行数或字节数不一致: {name}')
        content[role] = Counter(hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest() for row in rows)
        result[role] = {'filename': name, 'rows': len(rows), 'bytes': len(data),
                        'sha256': digest, 'transport': entry['transport'],
                        'requested_url': entry['requested_url']}
    return result, content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary', type=Path, required=True)
    parser.add_argument('--mirror', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    primary, first = inspect(args.primary)
    mirror, second = inspect(args.mirror)
    comparison = {role: {'byte_identical': primary[role]['sha256'] == mirror[role]['sha256'],
                         'csv_rows_identical_ignoring_order': first[role] == second[role],
                         'primary_only_rows': sum((first[role] - second[role]).values()),
                         'mirror_only_rows': sum((second[role] - first[role]).values())} for role in FILES}
    result = {'audited_at_utc': datetime.now(timezone.utc).isoformat(),
              'primary': primary, 'mirror': mirror, 'comparison': comparison,
              'status': 'passed', 'meaning': '校验本地载荷与下载清单；内容比较不推断未知上游版本号。'}
    if args.output.exists():
        parser.error('审计文件已存在，请指定新文件名')
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

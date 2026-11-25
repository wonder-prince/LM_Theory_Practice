"""仅用标准库获取公开 Olist 文件，或导入用户指定的可追溯 CSV。"""
import argparse
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

FILES = {
    'orders': 'olist_orders_dataset.csv',
    'items': 'olist_order_items_dataset.csv',
    'payments': 'olist_order_payments_dataset.csv',
    'customers': 'olist_customers_dataset.csv',
}
PAGE = 'https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce'
LICENSE = 'CC BY-NC-SA 4.0'
MAX_BYTES = 40 * 1024 * 1024
MIRROR_COMMIT = '21baca68a891817e8370b832273ba62d05a3d719'
MIRROR_BASE = f'https://raw.githubusercontent.com/cstuer/olist-ecommerce-analysis/{MIRROR_COMMIT}/raw'
MIRROR_BLOBS = {
    'orders': '13bbde9cd290f98fb3de3c6c1eb4d4a6f63dafa4',
    'items': 'dbdec13793b96ea5c00441f70d129d471c29bfda',
    'payments': 'b6c294a50fc1470abf2b8b09a33698c46eb6190d',
    'customers': '1e7c3f923dede48035a8637dd28c357e154e5e75',
}
# 避免macOS系统代理自动旁路检查的潜在阻塞；保留代理发现，旁路遵守no_proxy环境配置。
urllib.request.proxy_bypass = urllib.request.proxy_bypass_environment


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'datasets/raw')
    parser.add_argument('--mirror', action='store_true', help='显式使用固定提交的公开镜像，并验证Git blob哈希')
    parser.add_argument('--timeout', type=float, default=120, help='单次连接或读取超时秒数')
    parser.add_argument('--import-dir', type=Path)
    parser.add_argument('--source-url', help='导入时必须提供真实下载地址或镜像仓库地址')
    args = parser.parse_args()
    if args.import_dir and not args.source_url:
        parser.error('--import-dir 必须配合 --source-url')
    if args.import_dir and args.mirror:
        parser.error('--import-dir与--mirror不能同时使用')
    args.output.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output / 'source_manifest.json'
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest = {'dataset_page': PAGE, 'license': LICENSE, 'license_verified_date': '2026-11-24',
                'schema_version': 'olist-public-files-v1', 'upstream_kaggle_version': 'unverified',
                'files': {}, 'errors': [], 'previous_errors': old.get('previous_errors', []) + old.get('errors', [])}
    for role, name in FILES.items():
        dest = args.output / name
        entry = old.get('files', {}).get(role)
        if not args.import_dir and dest.exists() and entry and sha(dest.read_bytes()) == entry['sha256']:
            manifest['files'][role] = entry
            continue
        url = args.source_url if args.import_dir else (f'{MIRROR_BASE}/{name}' if args.mirror else f'https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce/{name}')
        try:
            if args.import_dir:
                data = (args.import_dir / name).read_bytes()
                final_url = url
                transport = 'imported_mirror_or_local'
                archive_hash = None
            else:
                request = urllib.request.Request(url, headers={'User-Agent': 'OlistAcademicDataPreparation/1.0', 'Accept-Encoding': 'gzip'})
                with urllib.request.urlopen(request, timeout=args.timeout) as response:
                    final_url = response.url
                    chunks, size = [], 0
                    while True:
                        chunk = response.read(256 * 1024)
                        if not chunk:
                            break
                        chunks.append(chunk)
                        size += len(chunk)
                        if size > MAX_BYTES:
                            raise ValueError('单文件响应超过40MiB上限')
                        if size % (1024 * 1024) == 0:
                            print(f'{name}: 已传输{size // (1024 * 1024)} MiB', flush=True)
                    data = b''.join(chunks)
                    archive_hash = sha(data)
                    if response.headers.get('Content-Encoding') == 'gzip':
                        with gzip.GzipFile(fileobj=io.BytesIO(data)) as compressed:
                            data = compressed.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise ValueError('解压后文件超过40MiB上限')
                if zipfile.is_zipfile(io.BytesIO(data)):
                    with zipfile.ZipFile(io.BytesIO(data)) as archive:
                        matches = [n for n in archive.namelist() if Path(n).name == name]
                        if len(matches) != 1 or archive.getinfo(matches[0]).file_size > MAX_BYTES:
                            raise ValueError('压缩包成员不符合预期')
                        data = archive.read(matches[0])
                transport = 'github_commit_pinned_mirror' if args.mirror else 'kaggle_public_api'
            git_blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
            if args.mirror and git_blob != MIRROR_BLOBS[role]:
                raise ValueError('镜像Git blob SHA-1不匹配')
            text = data.decode('utf-8-sig')
            rows = list(csv.DictReader(io.StringIO(text)))
            if not rows or ('order_id' if role != 'customers' else 'customer_unique_id') not in rows[0]:
                raise ValueError('返回内容不是预期CSV')
            if dest.exists() and dest.read_bytes() != data:
                raise ValueError('目标文件已存在且不同；请指定新的 --output，不覆盖现有数据')
            if not dest.exists():
                dest.write_bytes(data)
            manifest['files'][role] = {'filename': name, 'requested_url': url, 'resolved_url': final_url,
                'transport': transport, 'sha256': sha(data), 'download_payload_sha256': archive_hash,
                'git_blob_sha1': git_blob, 'mirror_commit': MIRROR_COMMIT if args.mirror else None,
                'bytes': len(data), 'rows': len(rows),
                'acquired_at_utc': datetime.now(timezone.utc).isoformat()}
            print(json.dumps({'file': name, 'rows': len(rows), 'sha256': sha(data)}, ensure_ascii=False))
        except Exception as exc:
            manifest['errors'].append({'file': name, 'url': url, 'error': str(exc)})
            print(f'{name}: {exc}')
    attempts = args.output / 'download_attempts.json'
    if attempts.exists():
        manifest['prior_attempts'] = {'filename': attempts.name, 'sha256': sha(attempts.read_bytes())}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    if manifest['errors']:
        raise SystemExit('部分下载失败，已记录source_manifest；可使用带来源地址的导入路径。')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
from __future__ import annotations
import csv
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / 'metadata' / 'cores.json'
EXTERNAL = ROOT / 'external_files.csv'
EXPERIMENTAL_ROOT = '_Experimental'
VALID_STATUSES = {'experimental','developing','candidate','graduated'}
VALID_AI = {'No AI assistance','AI-assisted development','Substantially AI-generated','Other'}
VALID_PLATFORMS = {'arcade','console','computer','other','utility'}
VALID_SOURCES = {'repository','external'}
VALID_ROLES = {'rbf','mra','mgl','cfg','txt'}
SUPPORTED_SUFFIXES = {'.rbf','.mra','.mgl','.cfg','.txt'}
SHA256_RE = re.compile(r'^[0-9a-fA-F]{64}$')

def fail(message: str) -> None:
    print(f'ERROR: {message}', file=sys.stderr)
    raise SystemExit(1)

def valid_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {'http','https'} and bool(parsed.netloc)

def validate_relative_path(path: str) -> Path:
    if not isinstance(path, str) or not path:
        fail('artifact path must be a non-empty string')
    p = Path(path)
    if p.is_absolute(): fail(f"invalid absolute path '{path}'")
    if '..' in p.parts or '.' in p.parts: fail(f"invalid path '{path}'")
    if '\\' in path: fail(f"path must use '/' separators: '{path}'")
    return p

def artifacts_for(core: dict) -> list[dict]:
    artifacts = core.get('artifacts')
    if not isinstance(artifacts, list) or not artifacts:
        fail(f"{core.get('slug','<unnamed>')}: 'artifacts' must be a non-empty list")
    out=[]
    for i,a in enumerate(artifacts,1):
        if not isinstance(a,dict): fail(f"{core.get('slug','<unnamed>')}: artifact {i} must be an object")
        for k in ('asset','path','role','source'):
            if not a.get(k): fail(f"{core.get('slug','<unnamed>')}: artifact {i} missing '{k}'")
        s=str(a['source']).lower(); r=str(a['role']).lower()
        if s not in VALID_SOURCES: fail(f"{core.get('slug','<unnamed>')}: invalid artifact source '{a['source']}'")
        if r not in VALID_ROLES: fail(f"{core.get('slug','<unnamed>')}: invalid artifact role '{a['role']}'")
        out.append(a)
    return out

def validate_artifact_path(core:dict,a:dict)->None:
    slug=core['slug']; platform=core['platform']; role=a['role'].lower(); path=a['path']; p=validate_relative_path(path)
    if p.suffix.lower() not in SUPPORTED_SUFFIXES: fail(f"{slug}: unsupported artifact path '{path}'")
    if platform=='arcade':
        if not (p.parts[0]=='_Arcade' or p.parts[0].startswith('_Arcade_')):
            fail(f"{slug}: Arcade artifacts must be under _Arcade or _Arcade_*; got '{path}'")
        root=p.parts[0]
        if role=='mra':
            if len(p.parts)!=2: fail(f"{slug}: Arcade MRA must be directly under {root}/; got '{path}'")
        elif role=='rbf':
            if len(p.parts)!=3 or p.parts[1].lower()!='cores': fail(f"{slug}: Arcade RBF must be under {root}/cores/; got '{path}'")
    else:
        if not path.startswith(EXPERIMENTAL_ROOT+'/_'):
            fail(f"{slug}: non-Arcade artifact must start with _Experimental/_ProjectName/; got '{path}'")
        if len(p.parts)<3 or not p.parts[1].startswith('_'):
            fail(f"{slug}: invalid Experimental project path '{path}'")

def validate_integrity_fields(slug,a):
    s=a.get('sha256')
    if s is not None and (not isinstance(s,str) or not SHA256_RE.fullmatch(s)): fail(f"{slug}: invalid SHA-256 for artifact '{a['path']}'")
    n=a.get('size_bytes')
    if n is not None and (not isinstance(n,int) or n<=0): fail(f"{slug}: invalid size_bytes for artifact '{a['path']}'")

def sha256_file(path:Path)->tuple[str,int]:
    h=hashlib.sha256(); size=0
    with path.open('rb') as f:
        while True:
            c=f.read(1024*1024)
            if not c: break
            h.update(c); size+=len(c)
    return h.hexdigest(),size

def sha256_url(url:str)->tuple[str,int]:
    req=urllib.request.Request(url,headers={'User-Agent':'MiSTer-Experimental-validator/1.0'})
    h=hashlib.sha256(); size=0
    try:
        with urllib.request.urlopen(req,timeout=60) as r:
            while True:
                c=r.read(1024*1024)
                if not c: break
                h.update(c); size+=len(c)
    except (urllib.error.URLError,TimeoutError) as e: fail(f"could not download '{url}': {e}")
    return h.hexdigest(),size

def validate_local_mra(slug,a):
    path=ROOT/validate_relative_path(a['path'])
    try: tree=ET.parse(path)
    except (ET.ParseError,OSError) as e: fail(f"{slug}: unable to parse repository MRA '{a['path']}': {e}")
    rbf=tree.getroot().find('rbf')
    if rbf is None or not (rbf.text or '').strip(): fail(f"{slug}: MRA '{a['path']}' does not contain a non-empty <rbf> element")

if not METADATA.is_file(): fail('metadata/cores.json not found')
try: metadata=json.loads(METADATA.read_text(encoding='utf-8'))
except json.JSONDecodeError as e: fail(f'metadata/cores.json is invalid JSON: {e}')
cores=metadata.get('cores')
if not isinstance(cores,list): fail("metadata/cores.json must contain a 'cores' array")

metadata_by_path={}; slugs=set()
for core in cores:
    if not isinstance(core,dict): fail("each item in metadata/cores.json 'cores' must be an object")
    required={'slug','name','status','release','source_repository','release_url','author','license','ai_assistance','platform','artifacts'}
    for k in required:
        if not core.get(k): fail(f"{core.get('name','<unnamed>')}: missing '{k}'")
    slug=core['slug']
    if slug in slugs: fail(f'duplicate slug: {slug}')
    slugs.add(slug)
    if core['status'] not in VALID_STATUSES: fail(f"{slug}: invalid status '{core['status']}'")
    if core['ai_assistance'] not in VALID_AI: fail(f"{slug}: invalid ai_assistance '{core['ai_assistance']}'")
    if core['platform'] not in VALID_PLATFORMS: fail(f"{slug}: invalid platform '{core['platform']}'")
    if not valid_url(core['source_repository']): fail(f"{slug}: invalid source_repository URL")
    if not valid_url(core['release_url']): fail(f"{slug}: invalid release_url URL")
    arts=artifacts_for(core); roles=set(); roots=set()
    for a in arts:
        validate_integrity_fields(slug,a); validate_artifact_path(core,a)
        path=a['path']; roles.add(a['role'].lower())
        if path in metadata_by_path: fail(f'duplicate metadata path: {path}')
        metadata_by_path[path]=core
        if core['platform']=='arcade': roots.add(Path(path).parts[0])
        if a['source'].lower()=='repository' and a['role'].lower()=='mra': validate_local_mra(slug,a)
    if core['platform']=='arcade':
        if 'mra' not in roles: fail(f"{slug}: Arcade submissions must declare at least one MRA artifact")
        if 'rbf' not in roles: fail(f"{slug}: Arcade submissions must declare at least one RBF artifact")
        if len(roots)!=1: fail(f"{slug}: all Arcade artifacts must share one _Arcade* root")

external_by_path={}
if not EXTERNAL.is_file(): fail('external_files.csv not found')
with EXTERNAL.open(newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f,skipinitialspace=True)
    if not reader.fieldnames: fail('external_files.csv has no header')
    if 'Path in MiSTer' not in reader.fieldnames: fail("external_files.csv is missing 'Path in MiSTer' column")
    if 'URL' not in reader.fieldnames: fail("external_files.csv is missing 'URL' column")
    for line_no,row in enumerate(reader,2):
        path=(row.get('Path in MiSTer') or '').strip(); url=(row.get('URL') or '').strip()
        if not path: fail(f'external_files.csv line {line_no}: empty path')
        if not url: fail(f'external_files.csv line {line_no}: empty URL')
        validate_relative_path(path)
        if Path(path).suffix.lower() not in SUPPORTED_SUFFIXES: fail(f"external_files.csv line {line_no}: unsupported artifact path '{path}'")
        if not valid_url(url): fail(f"external_files.csv line {line_no}: invalid URL '{url}'")
        if path in external_by_path: fail(f"external_files.csv line {line_no}: duplicate path '{path}'")
        external_by_path[path]={'url':url,'line':line_no}

metadata_paths=set(metadata_by_path); external_paths=set(external_by_path)
for path,core in metadata_by_path.items():
    a=next(a for a in artifacts_for(core) if a['path']==path); source=a['source'].lower()
    if source=='external' and path not in external_paths: fail(f'metadata external artifact has no external_files.csv entry: {path}')
    if source=='repository' and path in external_paths: fail(f'repository artifact must not appear in external_files.csv: {path}')
for path in sorted(external_paths-metadata_paths): fail(f'external_files.csv entry has no metadata entry: {path}')

install_roots={Path(p).parts[0] for p in metadata_paths}; payloads=set()
for root in sorted(install_roots):
    rp=ROOT/root
    if not rp.exists(): continue
    for p in rp.rglob('*'):
        if p.is_file(): payloads.add(p.relative_to(ROOT).as_posix())
for path in sorted(payloads-metadata_paths):
    fail(f'undeclared installed artifact: {path}\nEvery repository payload under a declared install root must be declared in metadata/cores.json.')

count=0
for path,core in metadata_by_path.items():
    a=next(a for a in artifacts_for(core) if a['path']==path); source=a['source'].lower()
    print(f"Checking artifact: {core['name']} [{a['role']}; {source}]")
    print(f'  Path: {path}')
    sha_decl=a.get('sha256'); size_decl=a.get('size_bytes')
    if source=='repository':
        local=ROOT/validate_relative_path(path)
        if a['role'].lower()=='mra': validate_local_mra(core['slug'],a)
        actual_sha,actual_size=sha256_file(local)
    else:
        entry=external_by_path.get(path)
        if entry is None: fail(f"{core['slug']}: external artifact missing CSV entry: {path}")
        print(f"  URL: {entry['url']}")
        actual_sha,actual_size=sha256_url(entry['url'])
    if sha_decl and actual_sha.lower()!=sha_decl.lower(): fail(f"{core['slug']}: SHA-256 mismatch for {path}\n  expected: {sha_decl}\n  actual:   {actual_sha}")
    if size_decl is not None and actual_size!=size_decl: fail(f"{core['slug']}: artifact size mismatch for {path}\n  expected: {size_decl}\n  actual:   {actual_size}")
    print(f'  SHA-256: {actual_sha}'); print(f'  Size:    {actual_size} bytes'); count+=1

print(f'Validation OK: {len(cores)} project(s), {count} artifact(s)')

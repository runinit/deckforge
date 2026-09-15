#!/usr/bin/env python3
"""Fetch selected source checkouts. Never install dependencies or execute their code."""
import argparse, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--only',nargs='+',required=True);a=p.parse_args()
project=Path(__file__).resolve().parents[1];root=a.root.expanduser().resolve()
if root==project or project in root.parents:p.exit(1,'Checkouts must be outside the public project\n')
config=json.loads((project/'config/upstreams.json').read_text());known={x['id']:x for x in config['upstreams']}
unknown=set(a.only)-known.keys()
if unknown:p.exit(1,f'Unknown ids: {sorted(unknown)}\n')
root.mkdir(parents=True,exist_ok=True);lockfile=root/'upstreams.lock.json'
lock=json.loads(lockfile.read_text()) if lockfile.exists() else {'checkouts':{}}
for name in a.only:
    spec=known[name];dest=root/name;url=f'https://github.com/{spec["repo"]}.git'
    if dest.exists():p.exit(1,f'{dest} exists. No existing checkout will be changed. Select only not-yet-fetched ids.\n')
    try:
        subprocess.run(['git','clone','--no-checkout','--depth','1',url,str(dest)],check=True,timeout=180)
        rev=spec['commit']
        if rev:subprocess.run(['git','-C',str(dest),'fetch','--depth','1','origin',rev],check=True,timeout=180)
        else:rev=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
        subprocess.run(['git','-C',str(dest),'checkout','--detach',rev],check=True,timeout=60)
        actual=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
        if actual!=rev:raise RuntimeError('Commit mismatch')
        lock['checkouts'][name]={'repository':spec['repo'],'commit':actual,'auditPinned':spec['commit'] is not None,'path':str(dest)}
        lockfile.write_text(json.dumps(lock,indent=2)+'\n')
    except (subprocess.CalledProcessError,subprocess.TimeoutExpired,RuntimeError) as e:
        p.exit(1,f'Checkout failed: {e}. Partial directory retained for inspection; nothing was installed.\n')
print(lockfile)

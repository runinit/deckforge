#!/usr/bin/env python3
"""Structural acceptance for OUR trusted smoke fixture, not a general upload sandbox."""
import argparse, hashlib, json, posixpath, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

def inspect(file: Path) -> dict:
    ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/package/2006/relationships'}
    errors=[]
    with zipfile.ZipFile(file) as z:
        infos=z.infolist()
        if len(infos)>5000 or sum(i.file_size for i in infos)>100_000_000: raise ValueError('Archive exceeds fixture limits')
        if any(i.file_size>20_000_000 for i in infos): raise ValueError('Archive member exceeds fixture limits')
        names=set(z.namelist())
        if any(n.startswith('/') or '..' in n.split('/') for n in names): raise ValueError('Unsafe archive member')
        slides=sorted(n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n))
        count={'slides':len(slides),'text_boxes':0,'native_shapes':0,'native_tables':0,'native_charts':0,'pictures':0,'notes':0,'embedded_workbooks':0}
        for name in sorted(names):
            if name.endswith(('.xml','.rels')):
                raw=z.read(name)
                if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():raise ValueError('DTD/entity not allowed')
                try: xml=ET.fromstring(raw)
                except ET.ParseError as exc:errors.append(f'{name}: malformed XML: {exc}');continue
                if name in slides:
                    count['text_boxes']+=sum(1 for e in xml.findall('.//p:sp',ns) if e.find('p:txBody',ns) is not None)
                    count['native_shapes']+=len(xml.findall('.//p:sp',ns))
                    count['native_tables']+=len(xml.findall('.//a:tbl',ns))
                    count['pictures']+=len(xml.findall('.//p:pic',ns))
                    if not any(t.text for t in xml.findall('.//a:t',ns)):errors.append(f'{name}: no native text')
                if re.fullmatch(r'ppt/charts/chart\d+\.xml',name):count['native_charts']+=1
                if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',name):count['notes']+=1
                if name.endswith('.rels'):
                    base='' if name=='_rels/.rels' else posixpath.dirname(posixpath.dirname(name))
                    for rel in xml:
                        if rel.attrib.get('TargetMode')=='External':errors.append(f'{name}: external relationship unexpected in fixture');continue
                        target=rel.attrib.get('Target','')
                        resolved=posixpath.normpath(posixpath.join(base,target)).lstrip('/')
                        if resolved not in names: errors.append(f'{name}: missing target {target}')
            if name.startswith('ppt/embeddings/') and name.endswith('.xlsx'):count['embedded_workbooks']+=1
            if name.lower().endswith('vbaproject.bin'):errors.append('Macros unexpected')
        if count['slides']!=6:errors.append('Smoke fixture must have exactly six slides')
        if count['notes']!=count['slides']:errors.append('Each fixture slide needs notes')
        for key in ['native_tables','native_charts','embedded_workbooks']:
            if count[key]<1:errors.append(f'Missing {key}')
        if count['pictures']!=0:errors.append('Fixture should contain no raster/SVG image pictures')
    return {'status':'structural-smoke-pass' if not errors else 'fail','sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'counts':count,'errors':errors,'not_checked':['Visual appearance','Text fitting','PowerPoint open/edit/save','True connector anchors','Native chart Edit Data operation']}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('pptx',type=Path);args=parser.parse_args()
    try: result=inspect(args.pptx)
    except (OSError,ValueError,zipfile.BadZipFile) as e:parser.exit(1,f'{e}\n')
    print(json.dumps(result,indent=2));sys.exit(bool(result['errors']))

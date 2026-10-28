# Viết lại BÌNH LUẬN GHIM theo từng cách phối: Cách N – Áo / Quần-Váy / Giày + link aff.
import csv,glob,os,re,sys,shutil
V=sys.argv[1]; K=V+'/KENH-03-thoi-trang'; T=K+'/3-THANH-PHAM'
aff={}
for r in csv.DictReader(open(K+'/5-LINK-AFFILIATE/KHO-SP-KENH03-2210.csv',encoding='utf-8-sig')): aff[r['itemid']]=r['link_aff']
for r in csv.DictReader(open(V+'/_HE-THONG/LINK-AFF-DA-DOI.csv',encoding='utf-8-sig')): aff.setdefault(r['itemid'],r['link_aff'])
BAD={'52903924770','48852922203'}
order=['k03-lo-2210','k03-lo-2','k03-lo-3','k03-lo-4','k03-lo-5','k03-lo-6','k03-lo-7','k03-lo-8','k03-lo-3-sua','k03-lo-8-sua']
links={}
for o in order:
    for f in glob.glob(f'{V}/_CHO-DUYET/{o}/**/links.csv',recursive=True):
        links[os.path.basename(os.path.dirname(f))[:3]]=f
def kind(name,mon):
    n=name.lower()
    if mon=='giay' or re.search(r'giày|giay|sneaker|boot|bốt|sandal|dép|loafer|búp bê|mary|oxford|sục',n): return (3,'👟 Giày')
    if re.search(r'chân váy|váy|skirt',n) and 'cardigan' not in n: return (2,'👗 Chân váy' if 'chân váy' in n or 'váy' in n else '👗 Váy')
    if re.search(r'đầm',n): return (2,'👗 Đầm')
    if re.search(r'quần|jean|kaki|short',n) and not re.search(r'^áo',n): return (2,'👖 Quần')
    if re.search(r'set|bộ',n): return (1,'🧥 Set')
    if re.search(r'khăn',n): return (4,'🧣 Khăn')
    if re.search(r'khoác|dạ|măng tô|mangto|blazer|cardigan|cadigan|bomber|phao|hoodie|gile|da mềm',n): return (0,'🧥 Áo khoác')
    return (1,'👚 Áo')
def setno(s):
    s=str(s).strip().lower()
    if s in('chinh','0'): return 0
    m=re.search(r'\d+',s); return int(m.group()) if m else None
done=[]
for folder in sorted(glob.glob(T+'/0*-5-cach-phoi')):
    num=os.path.basename(folder)[:3]
    if num not in links: continue
    rows=list(csv.DictReader(open(links[num],encoding='utf-8-sig')))
    hero=None; sets={}
    for r in rows:
        i=(r.get('itemid') or '').strip(); sn=setno(r.get('set',''))
        la=(r.get('link_aff') or '').strip()
        url=aff.get(i) if i else (la if la.startswith('https://s.shopee.vn/') else None)
        if (i and i in BAD) or sn is None or not url: continue
        item=(kind(r.get('ten_sp',''),r.get('mon','')),url)
        if sn==0 or r.get('mon')=='chinh': hero=item
        else: sets.setdefault(sn,[]).append(item)
    if not hero or not sets: print('skip',num); continue
    L=['Link từng cách phối trong video đây nha 👇','']
    for sn in sorted(sets):
        items=[hero]+sets[sn]; seen=set(); items2=[]
        for it in sorted(items,key=lambda x:x[0][0]):
            if it[1] in seen: continue
            seen.add(it[1]); items2.append(it)
        L.append(f'✨ Cách {sn}:')
        for (k,lab),url in items2: L.append(f'{lab}: {url}')
        L.append('')
    L.append('(Link affiliate – mình nhận hoa hồng nhỏ khi bạn mua, giá không đổi ❤️)')
    p=folder+'/noi-dung-dang.txt'; t=open(p,encoding='utf-8').read()
    lines=t.split('\n'); s=e=None
    for idx,l in enumerate(lines):
        if s is None and 'BÌNH LUẬN GHIM' in l: s=idx; continue
        if s is not None and idx>s and (re.match(r'^===',l.strip()) or re.match(r'^[A-ZÀ-Ỹ0-9 #/]+:$',l.strip())):
            e=idx; break
    if s is None: print('nohdr',num); continue
    e=e if e is not None else len(lines)
    new=lines[:s+1]+L+['']+lines[e:]
    if not os.path.exists(folder+'/noi-dung-dang-cu.txt'): shutil.copy(p,folder+'/noi-dung-dang-cu.txt')
    open(p,'w',encoding='utf-8').write('\n'.join(new)); done.append(num)
print('done',len(done),done[0],done[-1])

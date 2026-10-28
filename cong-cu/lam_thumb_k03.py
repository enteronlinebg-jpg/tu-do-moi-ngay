import sys,os,glob,json,subprocess,re
from PIL import Image,ImageDraw,ImageFont
V=sys.argv[1]; only=sys.argv[2:] 
K=V+'/KENH-03-thoi-trang'; T=K+'/3-THANH-PHAM'; FONT=V+'/_HE-THONG/cong-cu-dung/BeVietnamPro-ExtraBold.ttf'
OVR={'036':'Măng tô dạ dáng dài','041':'Set nỉ thu đông','038':'Áo dạ blazer tweed','030':'Blazer công sở','031':'Cardigan SEOULIFE','034':'Jean ống rộng retro'}
def hero(num):
    if num in OVR: return OVR[num]
    fs=glob.glob(f'{K}/2-DANG-LAM/k03-{num}-*-loi-doc.json')
    if not fs: return None
    t=json.load(open(fs[0],encoding='utf-8'))['segments'][0][2]
    t=re.sub(r'^(Một|Mot)\s+(chiếc|cái|bộ|set)\s+','',t.strip(),flags=re.I)
    return t.split(',')[0].split('!')[0].strip()
def fit(d,text,maxw,start):
    s=start
    while s>40:
        f=ImageFont.truetype(FONT,s)
        if d.textlength(text,font=f)<=maxw: return f
        s-=4
    return ImageFont.truetype(FONT,40)
def wrap(d,text,maxw,size):
    words=text.split(); lines=['']
    f=ImageFont.truetype(FONT,size)
    for w in words:
        t=(lines[-1]+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: lines[-1]=t
        else: lines.append(w)
    return lines,f
for folder in sorted(glob.glob(T+'/0*-5-cach-phoi')):
    num=os.path.basename(folder)[:3]
    if only and num not in only: continue
    mp4=[m for m in glob.glob(folder+'/*.mp4') if not m.endswith('-cu.mp4')]
    name=hero(num)
    if not mp4 or not name: print('skip',num); continue
    fr='/tmp/fr_'+num+'.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss','5.5','-i',mp4[0],'-frames:v','1',fr])
    src=Image.open(fr).convert('RGB')
    bg=src.getpixel((540,1900))
    out=Image.new('RGB',(1080,1920),bg)
    body=src.crop((0,280,1080,1880)); sc=0.8
    body=body.resize((int(1080*sc),int(1600*sc)),Image.LANCZOS)
    out.paste(body,((1080-body.width)//2,630))
    d=ImageDraw.Draw(out)
    nm=name.upper(); lines,f2=wrap(d,nm,840,90)
    while len(lines)>2: lines,f2=wrap(d,nm,840,f2.size-6)
    if len(lines)==2: lines,f2=wrap(d,nm,840,min(f2.size,76))
    if len(lines)==2:
        w=nm.split(); best=None
        for k in range(1,len(w)):
            a,b=' '.join(w[:k]),' '.join(w[k:]); m=max(d.textlength(a,font=f2),d.textlength(b,font=f2))
            if m<=840 and (best is None or m<best[0]): best=(m,[a,b])
        if best: lines=best[1]
    lh=f2.size+14; top=290; h=40+58+18+lh*len(lines)+30
    d.rounded_rectangle((80,top,1000,top+h),radius=36,fill=(43,33,28))
    f1=ImageFont.truetype(FONT,54)
    d.text((540,top+40+27),'5 CÁCH PHỐI',font=f1,fill=(232,214,196),anchor='mm')
    y=top+40+58+18+lh//2
    for i,l in enumerate(lines):
        d.text((540,y+i*lh),l,font=f2,fill=(255,255,255),anchor='mm')
    tp=folder+'/thumbnail.jpg'
    if os.path.exists(tp) and not os.path.exists(folder+'/thumbnail-cu.jpg'): os.rename(tp,folder+'/thumbnail-cu.jpg')
    out.save(tp,quality=92); print(num,nm,len(lines))

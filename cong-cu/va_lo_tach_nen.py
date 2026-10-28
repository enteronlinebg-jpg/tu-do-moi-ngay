# Thay ảnh sản phẩm bị thủng (do tách nền) bằng bản dựng lại sạch, bám theo vị trí từng khung.
# python3 va_lo_tach_nen.py vao.mp4 ra.mp4 t0 t1 x0 y0 x1 y1 t_mau [cao_cap_quan(px, mặc định 28)]
import sys,subprocess,numpy as np,cv2
from scipy import ndimage
src,dst=sys.argv[1],sys.argv[2]; t0,t1=float(sys.argv[3]),float(sys.argv[4]); x0,y0,x1,y1=map(int,sys.argv[5:9]); tm=float(sys.argv[9])
WB=int(sys.argv[10]) if len(sys.argv)>10 else 28
W,H,FPS=1080,1920,30
def grab(t):
    b=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',src,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(H,W,3)
def objmask(r,bg):
    m=np.abs(r-bg).sum(2)>36
    lab,k=ndimage.label(ndimage.binary_closing(m,iterations=3))
    if k==0: return None,None
    big=np.argmax(ndimage.sum(m,lab,range(1,k+1)))+1
    mm=(lab==big)&m
    ys,xs=np.where(lab==big); return mm,(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
reg=grab(tm)[y0:y1,x0:x1].astype(np.float32)
bg=np.median(np.concatenate([reg[:4].reshape(-1,3),reg[-4:].reshape(-1,3)]),0)
m,(bx0,by0,bx1,by1)=objmask(reg,bg)
A=reg[by0:by1,bx0:bx1].copy(); mA=m[by0:by1,bx0:bx1]
h,w=mA.shape
pts=np.column_stack(np.where(mA)[::-1]).astype(np.int32)
hull=np.zeros((h,w),np.uint8); cv2.fillConvexPoly(hull,cv2.convexHull(pts),1); hull=hull.astype(bool)
cov=np.array([ (mA[y]&hull[y]).sum()/max(hull[y].sum(),1) for y in range(h)])
lo=int(h*0.6); yref=lo+int(np.argmax(cov[lo:h-6]))
xs=np.where(hull[yref])[0]; refrow=A[max(yref-1,0):yref+2, xs[0]:xs[-1]+1].mean(0)
C=A.copy()
for y in range(WB,yref):
    xs=np.where(hull[y])[0]
    if len(xs)<2: continue
    C[y,xs[0]:xs[-1]+1]=cv2.resize(refrow[None],(xs[-1]-xs[0]+1,1),interpolation=cv2.INTER_LINEAR)[0]
# giữ mép ngoài mềm
alpha=cv2.GaussianBlur(hull.astype(np.float32),(3,3),0)
full_mean=A[mA].mean(0)
print('box',bx0,by0,bx1,by1,'yref',yref,'cov',round(cov[yref],3))
dec=subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',src,
  '-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-shortest',dst],stdin=subprocess.PIPE)
n=0; fixed=0
while True:
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    f=np.frombuffer(buf,np.uint8).reshape(H,W,3).copy(); t=n/FPS
    if t0<=t<=t1:
        r=f[y0:y1,x0:x1].astype(np.float32)
        mm,bb=objmask(r,bg)
        if bb is not None and (bb[2]-bb[0])>w*0.5:
            cw,ch=bb[2]-bb[0],bb[3]-bb[1]
            Cs=cv2.resize(C,(cw,ch)) if (cw,ch)!=(w,h) else C
            As=cv2.resize(alpha,(cw,ch)) if (cw,ch)!=(w,h) else alpha
            cur=r[bb[1]:bb[3],bb[0]:bb[2]][mm[bb[1]:bb[3],bb[0]:bb[2]]].mean(0)
            a=float(np.clip(((cur-bg)@(full_mean-bg))/max((full_mean-bg)@(full_mean-bg),1),0,1))
            sub=r[bb[1]:bb[3],bb[0]:bb[2]]
            k=(As*a)[...,None]
            sub[:]=sub*(1-k)+(bg*(1-a)+Cs*a)*k + sub*0  # đè bản sạch
            f[y0:y1,x0:x1]=np.clip(r,0,255).astype(np.uint8); fixed+=1
    enc.stdin.write(f.tobytes()); n+=1
enc.stdin.close(); enc.wait(); print('frames',n,'fixed',fixed)

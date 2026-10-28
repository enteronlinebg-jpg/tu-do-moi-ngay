import numpy as np, os
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage
S=new_session('isnet-general-use')
R='/mnt/user-data/uploads/VAS/KENH-03-thoi-trang/2-DANG-LAM/lookbook-002-tai-nguyen/'
def rb(name):
    im=Image.open(R+name).convert('RGB')
    return remove(im,session=S,post_process_mask=True)
def trim(im,pad=6):
    a=np.array(im)[:,:,3]; ys,xs=np.where(a>20)
    return im.crop((max(xs.min()-pad,0),max(ys.min()-pad,0),min(xs.max()+pad,im.width),min(ys.max()+pad,im.height)))
for n in ['jacket','m1_jeans','m2_skirt','m3_cargo','m4_maxi','m5_shorts']:
    trim(rb(n+'.jpg')).save(f'cut/{n}.png')
# split grids into components
for g in ['bottoms','shoes']:
    im=rb(g+'.jpg'); a=np.array(im)[:,:,3]>40
    lab,n=ndimage.label(ndimage.binary_dilation(a,iterations=12))
    objs=ndimage.find_objects(lab)
    comps=[]
    for i,sl in enumerate(objs):
        h=sl[0].stop-sl[0].start; w=sl[1].stop-sl[1].start
        if h*w<8000: continue
        sub=im.crop((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop))
        mask=(lab[sl]==i+1)
        arr=np.array(sub); arr[:,:,3]=arr[:,:,3]*mask
        comps.append(((sl[0].start+sl[0].stop)/2,(sl[1].start+sl[1].stop)/2,Image.fromarray(arr)))
    comps.sort(key=lambda c:(round(c[0]/250),c[1]))
    for k,(cy,cx,c) in enumerate(comps): trim(c).save(f'cut/{g}_{k}.png'); print(g,k,int(cy),int(cx),c.size)

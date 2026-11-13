from pathlib import Path
import hashlib,json
from PIL import Image,ImageOps
R=Path(__file__).resolve().parent
SRC=R/'covers/Eli首帧封面-v4.png'
EXPECTED='6165d25ce794d0de9de7d47f5d8ca472a05dba53671dee392740f4bf996e0493'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SRC)==EXPECTED
OUT=R/'covers/适配-v4';OUT.mkdir(exist_ok=True)
source=Image.open(SRC).convert('RGB')
results=[]
for label,size in [('3比4',(1080,1440)),('4比3',(1440,1080)),('16比9',(1920,1080))]:
    dest=OUT/f'Eli首帧封面-v4-{label}.png';assert not dest.exists()
    # 36 px safety around the available canvas; preserve whole source foreground.
    fitted=ImageOps.contain(source,(size[0]-72,size[1]-72),Image.Resampling.LANCZOS)
    x=(size[0]-fitted.width)//2;y=(size[1]-fitted.height)//2
    canvas=Image.new('RGB',size,(246,239,250));canvas.paste(fitted,(x,y));canvas.save(dest)
    exported=Image.open(dest).convert('RGB')
    assert exported.size==size
    assert exported.crop((x,y,x+fitted.width,y+fitted.height)).tobytes()==fitted.tobytes()
    preview=OUT/f'Eli首帧封面-v4-{label}-预览.jpg'
    ImageOps.contain(canvas,(800,800),Image.Resampling.LANCZOS).save(preview,quality=92)
    results.append(dict(path=str(dest),preview=str(preview),width=size[0],height=size[1],bytes=dest.stat().st_size,sha256=sha(dest),source_box=[0,0,source.width,source.height],fitted_size=list(fitted.size),placement=[x,y,x+fitted.width,y+fitted.height],padding_color=[246,239,250],preserved_entire_source=True,foreground_equals_expected_resample=True,cropped=False,stretched=False,redrawn=False))
assert sha(SRC)==EXPECTED
(R/'evidence/比例适配-v4-原始核验.json').write_text(json.dumps(dict(source=str(SRC),source_sha256=EXPECTED,method='Pillow ImageOps.contain LANCZOS；整图等比缩小，整数尺寸取整，不裁切；淡紫纯色留边与36px安全余量',outputs=results),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False))

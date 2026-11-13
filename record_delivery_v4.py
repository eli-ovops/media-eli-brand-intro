from pathlib import Path
import json,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,d):(R/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
d=json.loads((R/'evidence/输入冻结.json').read_text())
for k in ['source','frozen']:assert sha(d[k])==d[k+'_sha256']
p=R/'covers/Eli首帧封面-v4.png';im=Image.open(p)
qa=dict(version='v4',viewed=[str(p),str(R/'covers/Eli首帧封面-v4-预览.jpg')],method='实际view_image原PNG及手机预览，与已查看v3.1比较',text=['把 AI 用起来','实用方法 · 项目经验 · 踩坑分享','我是 Eli','AI｜Agent｜FDE'],text_visually_correct=True,face_round_glasses_black_jacket_pose_visually_preserved=True,layout_brush_paper_three_theme_cards_preserved=True,purple_palette_and_light_background=True,text_does_not_cover_face=True,pixel_identity_unchanged='UNKNOWN; image_gen编辑并非像素锁定',crop_3_4='沿用原构图，中心裁切仍会切字；本轮留后续适配，未宣称通过',user_acceptance='PENDING')
save('evidence/封面QA-v4.json',qa)
receipt=dict(content_id=R.name,date=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),status='V4_ACTUAL_PNG_DELIVERED_PENDING_PMO_USER_REVIEW',owner_thread_id='01a11a6f-49ef-7653-934a-4312979fd4e7',task=str(R/'封面紫色修订-v4任务.md'),human_instruction='想保持紫色的色调；图呢',method='built-in image_gen',generation_count=1,edit_target=str(R/'covers/Eli首帧封面-v3.1.png'),edit_target_sha256=sha(R/'covers/Eli首帧封面-v3.1.png'),prompt=str(R/'covers/prompt-v4.txt'),raw_generated='/Users/USER/.codex/generated_images/01a11a6f-49ef-7653-934a-4312979fd4e7/exec-88c2f862-d910-45fa-90c0-80e752394bb1.png',cover=str(p),cover_sha256=sha(p),cover_bytes=p.stat().st_size,dimensions=list(im.size),preview=str(R/'covers/Eli首帧封面-v4-预览.jpg'),qa=str(R/'evidence/封面QA-v4.json'),input_and_frozen_sha_verified_unchanged=True,source_video_sha256=d['source_sha256'],rules=['ROUTING-2026-09-30-v3','HANDOFF-2026-10-10-v2','BLOCKERS-2026-09-23-v1'],target_model='gpt-6.1-sol',target_effort='medium',actual_model='UNKNOWN',actual_effort='UNKNOWN',actual_speed='UNKNOWN',boundary=dict(changed_video=False,copied_input_again=False,modified_old_images_or_receipts=False,uploaded_or_published=False,dispatched_other_threads=False,modified_shared_state=False,installed_or_paid=False,deleted=False),remaining=['用户选定封面','3:4比例与实际平台遮挡由后续阶段适配'],temporary_records='v4原PNG/预览/提示词/QA/回执/脚本全部保留用于审图；无新视频或自动化',failures=[])
save('回执-v4.json',receipt)
files=[dict(path=str(f),bytes=f.stat().st_size,sha256=sha(f),source='本内容冻结输入、版本封面、静态QA或制作记录',purpose='保留用于审图/发布适配/来源验证') for f in sorted(R.rglob('*')) if f.is_file() and f.name!='文件记录-v4.json']
save('文件记录-v4.json',dict(content_id=R.name,version='v4',total_bytes=sum(x['bytes'] for x in files),files=files))
print(json.dumps(dict(cover=str(p),sha256=sha(p),bytes=p.stat().st_size,input_unchanged=True),ensure_ascii=False))

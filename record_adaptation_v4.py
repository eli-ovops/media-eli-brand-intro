from pathlib import Path
import json,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=json.loads((R/'evidence/比例适配-v4-原始核验.json').read_text())
assert sha(raw['source'])==raw['source_sha256']
for o in raw['outputs']:assert sha(o['path'])==o['sha256']
inp=json.loads((R/'evidence/输入冻结.json').read_text())
for k in ['source','frozen']:assert sha(inp[k])==inp[k+'_sha256']
receipt=dict(content_id=R.name,date=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),status='ADAPTED_PNGS_DELIVERED_PENDING_PMO_PLATFORM_REVIEW',owner_thread_id='01a11a6f-49ef-7653-934a-4312979fd4e7',task=str(R/'封面比例适配任务-v4.md'),requirements_read=str(R/'flow/06/封面适配需求-04.md'),blocker_screenshot_actually_viewed=str(R/'flow/06/抖音-3比4裁切阻断.jpg'),input=raw['source'],input_sha256=raw['source_sha256'],outputs=raw['outputs'],method=raw['method'],visual_check=dict(actually_viewed=[o['path'] for o in raw['outputs']],all_four_text_groups_face_and_glasses_visible=True,no_crop_or_overlap=True,wide_padding='4:3/16:9保留居中纵向原图和淡紫左右宽留边，任务已明确接受',limit='本轮为本地PNG原件验证，平台原生编辑器仍由06验收；等比重采样保留整图内容，不冒称所有原分辨率像素数值不变'),rule_versions=['ROUTING-2026-09-30-v3','HANDOFF-2026-10-10-v2','BLOCKERS-2026-09-23-v1'],target_model='gpt-6.1-sol',target_effort='medium',actual_model='UNKNOWN',actual_effort='UNKNOWN',actual_speed='UNKNOWN',boundary=dict(original_cover_sha_unchanged=True,video_sha_unchanged=True,redrawn=False,uploaded_or_published=False,dispatched_other_threads=False,shared_state_modified=False,installed_or_paid=False,deleted=False),temporary_files='3张PNG、3张JPG预览、适配源码、原始核验及回执保留供PMO与06复用，无新增视频',failures=[])
(R/'比例适配回执-v4.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
paths=[R/'adapt_cover_v4.py',R/'record_adaptation_v4.py',R/'evidence/比例适配-v4-原始核验.json',R/'比例适配回执-v4.json',R/'README.md',*sorted((R/'covers/适配-v4').iterdir())]
files=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),source='本条批准v4机械等比适配或本轮记录',purpose='发布封面适配、实际审阅及恢复；保留') for p in paths if p.is_file()]
(R/'比例适配文件记录-v4.json').write_text(json.dumps(dict(content_id=R.name,total_bytes=sum(f['bytes'] for f in files),files=files),ensure_ascii=False,indent=2)+'\n')
print('3 PNG SHA verified; original cover and both video copies unchanged')

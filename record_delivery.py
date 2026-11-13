import hashlib,json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,d): (ROOT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
inputs=json.loads((ROOT/'evidence/输入冻结.json').read_text())
for k in ['source','frozen']:
    assert sha(Path(inputs[k]))==inputs[k+'_sha256']
cover=ROOT/'covers/Eli首帧封面-v2.png'
im=Image.open(cover);assert im.size==(941,1672)
receipt=dict(content_id=ROOT.name,date=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),status='DELIVERED_PENDING_USER_AND_PMO_REVIEW',owner_thread_id='01a11a6f-49ef-7653-934a-4312979fd4e7',authorization_task='/Volumes/EXTERNAL/自媒体/流程协作/04-剪辑与视觉制作/Eli形象短片封面任务-20261010.md',input_freeze=inputs,input_spec=json.loads((ROOT/'evidence/输入规格-avprobe.json').read_text()),cover=dict(path=str(cover),sha256=sha(cover),bytes=cover.stat().st_size,width=im.width,height=im.height,aspect='near9:16',aspect_relative_error_percent=round(abs(im.width/im.height/(9/16)-1)*100,5),preview=str(ROOT/'covers/Eli首帧封面-v2-预览.jpg'),text=['我是 Eli','把 AI 用进真实任务','AI｜Agent｜FDE'],method='built-in image_gen',prompts=[str(ROOT/'covers/prompt-v1.txt'),str(ROOT/'covers/prompt-v2.txt')]),generation_history=[dict(version='v1',raw='/Users/USER/.codex/generated_images/01a11a6f-49ef-7653-934a-4312979fd4e7/exec-f49c9974-96f2-46f3-9b27-27558689ac8f.png',saved=str(ROOT/'covers/Eli首帧封面-v1.png'),reason_superseded='中心3:4裁切会切近头发与辅助文字，保留历史'),dict(version='v2',raw='/Users/USER/.codex/generated_images/01a11a6f-49ef-7653-934a-4312979fd4e7/exec-7c454647-d8bc-4bd3-9a3f-9a3f84bde1eb.png',saved=str(cover),change='仅一次针对性裁切位置修正')],visual_qa=dict(owner='04',method='实际view_image查看参考帧和最终PNG、手机预览、中心3:4裁切图',viewed_source_seconds=[3,5],also_viewed=['既有sheet-01.jpg','既有12.5秒结尾原尺寸.jpg'],actual_final_viewed=[str(cover),str(ROOT/'covers/Eli首帧封面-v2-预览.jpg'),str(ROOT/'evidence/居中3比4裁切检查-v2.png')],text_visual_match=True,face_and_round_glasses_visible=True,no_text_over_face=True,crop=dict(box=[1,210,940,1462],size=[939,1252],important_content_visible=True),limit='基于指定视频形象AI重绘；本人身份相似度最终待用户，实际平台遮挡/裁切待06。未连续播放听看视频，不把采样升级为全片验收'),routing=dict(read_rules=['ROUTING-2026-09-30-v3','HANDOFF-2026-10-10-v2','BLOCKERS-2026-09-23-v1','IDEA-GATE-2026-09-30-v1'],target_model='gpt-6.1-sol',target_effort='medium',actual_model='UNKNOWN',actual_effort='UNKNOWN',actual_speed='UNKNOWN'),read_files=['/Volumes/EXTERNAL/自媒体/AGENTS.md','/Users/USER/.codex/AGENTS.details.md','/Users/USER/.codex/LOCAL_BLOCKERS.md','/Users/USER/.codex/skills/.system/imagegen/SKILL.md','/Volumes/EXTERNAL/自媒体/流程协作/README.md','/Volumes/EXTERNAL/自媒体/流程协作/流程状态.json','/Volumes/EXTERNAL/自媒体/流程协作/会话登记.json','/Volumes/EXTERNAL/自媒体/审片/eli形象短片修订-20261010/检查结论.md'],boundaries=dict(transcoded_video=False,inserted_cover_into_video=False,changed_music=False,uploaded_or_published=False,modified_old_interview=False,modified_shared_state=False,dispatched_other_threads=False,installed_or_paid=False,deleted=False),next_step='用户审封面，PMO审原件后依序派05/06；04不自行PASS，输入视频继续保留',processes_or_automations='不适用；本轮工具均返回结束，无新增自动化',failures=[],temporary_records_status='参考帧、QA裁切图、预览和提示词保留，用于审阅/恢复/适配')
save('回执.json',receipt)
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name=='文件记录.json':continue
    if p.parent.name=='sources':origin='用户指定输入原样复制';purpose='冻结发布准备输入，保留'
    elif p.name.startswith('参考帧'):origin='指定视频FFmpeg3/5秒抽帧';purpose='封面身份/风格参考'
    elif p.name.startswith('居中'):origin='本轮PNG的QA裁切';purpose='静态构图检查，非平台交付'
    elif p.suffix=='.png' and p.parent.name=='covers':origin='内置imagegen';purpose='主封面v2或历史v1'
    elif p.suffix=='.jpg':origin='PNG忠实缩小预览';purpose='手机尺寸审阅'
    else:origin='本轮制作记录';purpose='提示词、来源校验或交接证据'
    files.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),mtime=datetime.fromtimestamp(p.stat().st_mtime,ZoneInfo('Asia/Shanghai')).isoformat(),source=origin,purpose=purpose,cleanup='保留；本轮未发布、未删除'))
save('文件记录.json',dict(content_id=ROOT.name,total_bytes=sum(f['bytes'] for f in files),files=files,raw_generated_files_preserved=[v['raw'] for v in receipt['generation_history']]))
print(json.dumps(dict(cover_sha256=sha(cover),total_bytes=sum(f['bytes'] for f in files),file_count=len(files),input_sha_verified=True),ensure_ascii=False))

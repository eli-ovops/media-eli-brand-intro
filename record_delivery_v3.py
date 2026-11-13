import hashlib,json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,d):(ROOT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
inputs=json.loads((ROOT/'evidence/输入冻结.json').read_text())
for k in ['source','frozen']:assert sha(inputs[k])==inputs[k+'_sha256']
refs=[dict(path='/Volumes/EXTERNAL/自媒体/first-video-life-guide-20261008/qa/cover-v6/poster-frame14.png',role='风格辅助：巨型字体、蓝橙反差、立体主题场景'),dict(path='/Volumes/EXTERNAL/自媒体/sun-shao-interview-20261009/covers/邵艾伦×孙宇晨-没资源怎么抓住AI机会-海报-v3.png',role='主风格：米白纸纹、深蓝橙笔刷、人物合成与插画路径'),dict(path=str(ROOT/'evidence/参考帧-03.000.png'),role='本条视频3秒帧：唯一人物身份、黑外套、圆框眼镜')]
for r in refs:r['sha256']=sha(r['path']);r['actually_viewed']=True
cover=ROOT/'covers/Eli首帧封面-v3.1.png';im=Image.open(cover)
qa=dict(content_id=ROOT.name,version='v3.1',cover=str(cover),dimensions=list(im.size),sha256=sha(cover),method='实际查看原PNG、540px宽手机预览、中心3:4裁切PNG',viewed=[str(cover),str(ROOT/'covers/Eli首帧封面-v3.1-预览.jpg'),str(ROOT/'evidence/居中3比4裁切检查-v3.1.png')],reference_images=refs,full_portrait_qa=dict(title='把 AI 用起来',subtitle='实用方法 · 项目经验 · 踩坑分享',identity='我是 Eli',identity_line='AI｜Agent｜FDE',visual_text_correct=True,unrequested_decorative_words_removed=True,one_person=True,face_and_round_glasses_visible=True,text_does_not_cover_face=True,theme_cards=['工具操作界面','项目流程','问题→修复'],claims='纯频道主题示意，无收益/客户/真实项目成果'),crop_qa=dict(box=[1,210,940,1462],size=[939,1252],passed=False,issue='标题顶部和底部身份文案被截；不宜直接中心3:4裁切',next='06经PMO释放后在真实编辑器优先完整图等比适配；若平台强制填满3:4，需要另做布局适配'),limitations=['AI重绘非原帧像素不变；本人身份相似度最终由用户审阅','不是所有比例与所有平台按钮遮区均已通过','本轮只生成1张新设计并完成1次针对性修复，未无限追加生成'])
save('evidence/封面QA-v3.json',qa)
receipt=dict(content_id=ROOT.name,date=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),status='STYLE_CANDIDATE_DELIVERED_WITH_CROP_GAP_PENDING_PMO_REVIEW',owner_thread_id='01a11a6f-49ef-7653-934a-4312979fd4e7',task=str(ROOT/'封面风格修订-v3任务.md'),human_correction='封面没那种味道啊，需要结合前两次的那种封面风格',v2_status='USER_REJECTED_NOT_PUBLICATION_CANDIDATE',current_version='v3.1',cover=str(cover),cover_sha256=sha(cover),cover_bytes=cover.stat().st_size,qa=str(ROOT/'evidence/封面QA-v3.json'),references=refs,method='built-in image_gen',generation_count=1,targeted_repair_count=1,prompts=[str(ROOT/'covers/prompt-v3.txt'),str(ROOT/'covers/prompt-v3.1.txt')],raw_outputs=['/Users/USER/.codex/generated_images/01a11a6f-49ef-7653-934a-4312979fd4e7/exec-0eba9e6a-4418-4484-8620-127263aa1737.png','/Users/USER/.codex/generated_images/01a11a6f-49ef-7653-934a-4312979fd4e7/exec-eb50526f-f687-42f8-8f82-2fa68523aea9.png'],input_sha256=inputs['source_sha256'],input_and_frozen_video_unchanged=True,input_copied_again=False,read_rule_versions=['ROUTING-2026-09-30-v3','HANDOFF-2026-10-10-v2','BLOCKERS-2026-09-23-v1'],target_model='gpt-6.1-sol',target_effort='medium',actual_model='UNKNOWN',actual_effort='UNKNOWN',actual_speed='UNKNOWN',unfinished=['主封面待PMO审图和用户选定','中心3:4裁切未通过，需要完整图适配或后续单独布局修订'],boundary=dict(changed_video=False,uploaded_or_published=False,dispatched_05_or_06=False,modified_shared_state=False,modified_reference_covers_or_interview_cleanup=False,installed_or_paid=False,deleted=False),temporary_records='新PNG、手机预览、QA裁切图、提示词、脚本与回执全部保留供审图/后续适配；无新视频/自动化',tool_failures=[])
save('回执-v3.json',receipt)
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name=='文件记录-v3.json':continue
    files.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),mtime=datetime.fromtimestamp(p.stat().st_mtime,ZoneInfo('Asia/Shanghai')).isoformat(),source='本条冻结输入/原封面历史或v3内置imagegen/静态QA与记录',purpose='审图、来源校验和后续适配',cleanup='保留，未删除'))
save('文件记录-v3.json',dict(content_id=ROOT.name,version='v3.1',total_bytes=sum(f['bytes'] for f in files),files=files))
print(json.dumps(dict(sha=sha(cover),total_bytes=sum(f['bytes'] for f in files),input_unchanged=True,crop_passed=False),ensure_ascii=False))

"""Persistent sparse LK frontend benchmark; no mapping or pose certification."""
import json
import sys
import time
from pathlib import Path
import cv2
import numpy as np

run=Path(sys.argv[1]);out=run/'lightweight_frontend';out.mkdir(exist_ok=True)
cal=json.loads(Path('artifacts/m3c-calibration-20261007/calibration_result.json').read_text())
K=np.array(cal['camera_matrix']);K[:2,:]*=.5;d=np.array(cal['distortion_coefficients'])
K[0,2]-=.25;K[1,2]-=.25  # OpenCV resize pixel-center convention
cap=cv2.VideoCapture(str(run/'record.h264'))
max_frames=int(sys.argv[2]) if len(sys.argv)>2 else 0
pts=None;old=None;anchor=None;key_index=0;next_id=0;ids=np.empty(0,dtype=int)
records=[];keyframes=[];times=[];decode_times=[];start=time.perf_counter();i=0
while True:
    if max_frames and i>=max_frames:break
    tick=time.perf_counter();ok,frame=cap.read();decode_times.append((time.perf_counter()-tick)*1000)
    if not ok:break
    tick=time.perf_counter()
    gray=cv2.cvtColor(cv2.resize(frame,(672,380),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY)
    incoming=0 if pts is None else len(pts);retained=0;median_flow=0
    if old is not None and incoming:
        nxt,status,err=cv2.calcOpticalFlowPyrLK(old,gray,pts,None,winSize=(15,15),maxLevel=2)
        back,bs,_=cv2.calcOpticalFlowPyrLK(gray,old,nxt,None,winSize=(15,15),maxLevel=2)
        good=(status.ravel()==1)&(bs.ravel()==1)&(np.linalg.norm((pts-back).reshape(-1,2),axis=1)<.75)&(err.ravel()<30)
        xy=nxt.reshape(-1,2);good&=(xy[:,0]>=8)&(xy[:,0]<664)&(xy[:,1]>=8)&(xy[:,1]<372)
        retained=int(good.sum())
        if retained:median_flow=float(np.median(np.linalg.norm((nxt-pts).reshape(-1,2)[good],axis=1)))
        pts=nxt[good];ids=ids[good]
    replenished=0
    if pts is None or len(pts)<180 or i%30==0:
        mask=np.full(gray.shape,255,np.uint8);mask[:8,:]=0;mask[-8:,:]=0;mask[:,:8]=0;mask[:,-8:]=0
        if pts is not None:
            for p in pts.reshape(-1,2):cv2.circle(mask,tuple(np.int32(p)),10,0,-1)
        extra=cv2.goodFeaturesToTrack(gray,maxCorners=max(1,400-(0 if pts is None else len(pts))),qualityLevel=.015,minDistance=10,mask=mask,blockSize=7)
        if extra is not None and (pts is None or len(pts)<400):
            extra=extra[:400-(0 if pts is None else len(pts))];replenished=len(extra)
            pts=extra if pts is None else np.concatenate([pts,extra]);ids=np.concatenate([ids,np.arange(next_id,next_id+replenished)]);next_id+=replenished
    if pts is None:pts=np.empty((0,1,2),np.float32)
    # Undistort point coordinates only, preserving native-camera calibration.
    und=cv2.undistortPoints(pts,K,d,P=K).reshape(-1,2) if len(pts) else np.empty((0,2))
    current={int(identity):p for identity,p in zip(ids,und)}
    common=[] if anchor is None else [j for j in current if j in anchor]
    parallax=float(np.median([np.linalg.norm(current[j]-anchor[j]) for j in common])) if common else 0
    choose=anchor is None or (i-key_index>=18 and (parallax>=8 or len(common)<80 or i-key_index>=90))
    if choose:
        keyframes.append({'frame_index':i,'seconds_nominal':i/180,'common_tracks':len(common),'median_displacement_halfres_px':parallax,'points':len(pts),'reason':'initial' if anchor is None else 'motion_or_track_loss_or_timeout'})
        anchor=current;key_index=i
    elapsed=(time.perf_counter()-tick)*1000;times.append(elapsed)
    records.append({'frame_index':i,'tracked_incoming':incoming,'retained':retained,'retention':None if not incoming else retained/incoming,'active_tracks':len(pts),'replenished':replenished,'median_flow_halfres_px':median_flow,'keyframe':choose,'processing_ms':elapsed})
    old=gray;i+=1
cap.release()
elapsed=time.perf_counter()-start
ret=np.array([r['retention'] for r in records if r['retention'] is not None])
report={'decoded_frames':i,'geometry':[672,380],'coordinate_note':'Half-resolution tracking, point-only undistortion with appropriately scaled K; source video and original calibration unchanged.','elapsed_seconds':elapsed,'end_to_end_fps':i/elapsed,'processing_ms_median':float(np.median(times)),'processing_ms_p95':float(np.percentile(times,95)),'processing_fps_mean':1000/float(np.mean(times)),'decode_ms_median':float(np.median(decode_times)),'retention_median':float(np.median(ret)),'retention_p10':float(np.percentile(ret,10)),'retention_min':float(ret.min()),'active_tracks_median':float(np.median([r['active_tracks'] for r in records])),'keyframes':keyframes,'records':records,'limitations':'Windows-host offline frontend benchmark, no board realtime claim, map, estimated poses or metric scale. Keyframe displacement includes rotation, not verified triangulation parallax.'}
report['frame_limit']=max_frames
report['platform']=__import__('platform').platform()
report['limitations']='Offline frontend benchmark on the recorded platform, not realtime SLAM. No map, estimated poses or metric scale. Keyframe displacement includes rotation, not verified triangulation parallax. Bounded frame sample when frame_limit is nonzero.'
(out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('records','keyframes')},indent=2));print('keyframes='+str(len(keyframes)))

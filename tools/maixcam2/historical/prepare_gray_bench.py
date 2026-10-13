"""Make bounded gray benchmark inputs with installed Python OpenCV."""
import cv2
import time
import json
from pathlib import Path
source='/root/os04a10-tests/os04a10-20261007-005702-52804b/record.h264'
out=Path('/root/slam-bench-20261007')
cap=cv2.VideoCapture(source)
start=time.perf_counter();count=0
with (out/'gray336.raw').open('wb') as a,(out/'gray672.raw').open('wb') as b:
    for i in range(360):
        ok,frame=cap.read()
        if not ok:break
        for w,h,f in [(336,190,a),(672,380,b)]:
            gray=cv2.cvtColor(cv2.resize(frame,(w,h),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2GRAY)
            f.write(gray.tobytes())
        count+=1
cap.release()
print(json.dumps({'prepared_frames':count,'wall_seconds':time.perf_counter()-start}))
assert count==360

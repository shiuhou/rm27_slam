"""Portable bounded wrapper of the historical resize/BGR-to-gray preparation.

This prepares an offline decoded prefix, not camera timestamps or a VIO dataset.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

import cv2


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def prepare(source, output, frames):
    if type(frames) is not int or not 1 <= frames <= 3600:
        raise ValueError('frames must be an integer in [1, 3600]')
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    output.mkdir(parents=True, exist_ok=False)
    marker = output / 'INCOMPLETE'
    marker.write_text('Partial decoded prefix only; do not use as a complete input.\n', encoding='utf-8')
    capture = cv2.VideoCapture(str(source))
    count = 0
    started = time.perf_counter()
    try:
        with (output / 'gray336.raw').open('xb') as small, (output / 'gray672.raw').open('xb') as large:
            for _ in range(frames):
                ok, frame = capture.read()
                if not ok:
                    break
                for width, height, stream in ((336, 190, small), (672, 380, large)):
                    gray = cv2.cvtColor(cv2.resize(frame, (width, height),
                                       interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
                    stream.write(gray.tobytes())
                count += 1
    finally:
        capture.release()
    if count != frames:
        raise ValueError(f'decoded {count} frames; requested {frames}; incomplete prefix retained')
    result = dict(schema_version=1, status='COMPLETE_REQUESTED_PREFIX', source_name=source.name,
                  source_sha256=sha256(source), requested_frames=frames, prepared_frames=count,
                  preparation_wall_seconds=time.perf_counter() - started, opencv_version=cv2.__version__,
                  pixel_pipeline='OpenCV INTER_AREA resize, then BGR2GRAY, uint8 row-major',
                  timestamp_evidence='NONE: decoded order only; no exposure clock or synchronization',
                  scope='Offline frontend input preparation; not SLAM/VIO qualification', outputs={})
    for width, height in ((336, 190), (672, 380)):
        name = f'gray{width}.raw'
        path = output / name
        result['outputs'][name] = dict(width=width, height=height, frames=count,
                                      bytes=path.stat().st_size, sha256=sha256(path))
    (output / 'preparation.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    marker.unlink()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='existing video file; no camera/device access')
    parser.add_argument('--output', type=Path, required=True, help='new directory; refuses existing paths')
    parser.add_argument('--frames', type=int, default=360, help='decoded prefix size, 1..3600 (default 360)')
    args = parser.parse_args()
    print(json.dumps(prepare(args.input, args.output, args.frames), indent=2, allow_nan=False))


if __name__ == '__main__':
    main()

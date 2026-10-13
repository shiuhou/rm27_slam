"""Synthetic video tests only; no camera, board, SLAM or performance PASS."""
import hashlib
from pathlib import Path
import subprocess
import sys

import cv2
import numpy as np
import pytest


def video(path, count=3):
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'MJPG'), 30, (128, 96))
    assert writer.isOpened(), 'MJPG fixture encoder unavailable'
    try:
        for i in range(count):
            frame = np.full((96, 128, 3), 30 + i * 40, dtype=np.uint8)
            cv2.circle(frame, (30 + i * 10, 45), 12, (210, 90, 150), -1)
            writer.write(frame)
    finally:
        writer.release()
    return path


def prepare(*args):
    from tools.maixcam2.prepare_gray import prepare
    return prepare(*args)


def test_outputs_match_existing_resize_and_gray_algorithm(tmp_path):
    source = video(tmp_path / 'synthetic.avi')
    output = tmp_path / 'gray'
    result = prepare(source, output, 3)
    assert result['status'] == 'COMPLETE_REQUESTED_PREFIX'
    assert result['prepared_frames'] == 3
    assert result['source_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
    cap = cv2.VideoCapture(str(source))
    decoded = []
    try:
        for _ in range(3):
            ok, frame = cap.read()
            assert ok
            decoded.append(frame)
    finally:
        cap.release()
    for width, height in ((336, 190), (672, 380)):
        raw = (output / f'gray{width}.raw').read_bytes()
        expected = b''.join(cv2.cvtColor(cv2.resize(frame, (width, height),
                             interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).tobytes()
                            for frame in decoded)
        assert raw == expected
        assert len(raw) == width * height * 3
        assert result['outputs'][f'gray{width}.raw']['sha256'] == hashlib.sha256(raw).hexdigest()
    assert not (output / 'INCOMPLETE').exists()
    assert (output / 'preparation.json').is_file()


def test_existing_output_is_never_overwritten(tmp_path):
    source = video(tmp_path / 'synthetic.avi')
    output = tmp_path / 'existing'
    output.mkdir()
    (output / 'keep').write_bytes(b'untouched')
    with pytest.raises(FileExistsError):
        prepare(source, output, 3)
    assert list(output.iterdir()) == [output / 'keep']
    assert (output / 'keep').read_bytes() == b'untouched'


def test_short_input_leaves_marked_prefix_not_success(tmp_path):
    source = video(tmp_path / 'short.avi', 2)
    output = tmp_path / 'incomplete'
    with pytest.raises(ValueError, match='2.*3'):
        prepare(source, output, 3)
    assert (output / 'INCOMPLETE').exists()
    assert not (output / 'preparation.json').exists()
    assert (output / 'gray336.raw').stat().st_size == 336 * 190 * 2


@pytest.mark.parametrize('count', [0, -1, 3601, True, 1.5])
def test_frame_limit_is_positive_bounded_integer(tmp_path, count):
    source = video(tmp_path / 'synthetic.avi')
    output = tmp_path / 'not-created'
    with pytest.raises(ValueError):
        prepare(source, output, count)
    assert not output.exists()


def test_missing_source_does_not_create_outputs(tmp_path):
    with pytest.raises(FileNotFoundError):
        prepare(tmp_path / 'absent.avi', tmp_path / 'not-created', 3)
    assert not (tmp_path / 'not-created').exists()


def test_cli_help_needs_no_private_paths_or_hardware():
    script = Path(__file__).resolve().parents[1] / 'tools/maixcam2/prepare_gray.py'
    result = subprocess.run([sys.executable, str(script), '--help'], capture_output=True, text=True)
    assert result.returncode == 0
    assert '--input' in result.stdout and '--output' in result.stdout

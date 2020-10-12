from subprocess import Popen, PIPE
from threading import Timer

SUPPORTED_TYPES = [
    "epub",
]


def convert_to_pdf(input_fp, output_fp):
    p = Popen(["ebook-convert", str(input_fp), str(output_fp)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    timer = Timer(60, p.kill)
    try:
        timer.start()
        output, err = p.communicate()
    finally:
        timer.cancel()
    if output is None:
        output = b""
    if err is None:
        err = b"Killed by timer"
    rc = p.returncode
    return output, err, rc

from subprocess import Popen, PIPE

SUPPORTED_TYPES = [
    "epub",
]


def convert_to_pdf(input_fp, output_fp):
    p = Popen(["ebook-convert", str(input_fp), str(output_fp)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    return output, err, rc

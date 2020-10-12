import subprocess

SUPPORTED_TYPES = [
    "epub",
]


def convert_to_pdf(input_fp, output_fp):
    subprocess.call(["ebook-convert", str(input_fp), str(output_fp)])


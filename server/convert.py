from subprocess import STDOUT, check_output

SUPPORTED_TYPES = [
    "epub",
]


def convert_to_pdf(input_fp, output_fp):
    output = check_output(f"ebook-convert {input_fp} {output_fp}", stderr=STDOUT, timeout=60)
    return output

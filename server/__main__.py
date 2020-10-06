from . import prepare_workdir, new_tmp_dir, compress_pdf, get_path
from sanic import Sanic, response
import concurrent.futures
import functools
import aiofiles
import asyncio
import logging
import secrets
import shutil
import os

app = Sanic(name="mautils")


@app.route("/api/compress/pdf", methods=['POST'])
async def api_compress_pdf(request):
    # For now assume it's one file
    assert len(request.files) == 1
    for i, (_, file_container) in enumerate(request.files.items()):
        assert len(file_container) == 1
        file_obj = file_container[0]
        try:
            tmp_dir = new_tmp_dir()
            tmp_fp = tmp_dir / f"tmp-{i}.pdf"
            result_fp = tmp_dir / file_obj.name

            if not file_obj.name.endswith(".pdf") or not file_obj.type == "application/pdf":
                return response.json({"status": 400, "message": "Wrong file (or format). Only '.pdf' can be compressed here"}, status=400)

            async with aiofiles.open(tmp_fp, "wb") as tmp:
                await tmp.write(file_obj.body)

            logging.info(f"Started optimising {file_obj.name}..")
            init_size = tmp_fp.stat().st_size

            loop = asyncio.get_event_loop()
            with concurrent.futures.ProcessPoolExecutor() as pool:
                await loop.run_in_executor(
                    pool,
                    functools.partial(
                        # We have to pass strings, not Path obj (using .cpp internally)
                        compress_pdf, str(tmp_fp), str(result_fp)
                    )
                )

            size = "{0:.0%}".format(1 - (result_fp.stat().st_size / init_size))
            logging.info(f"Finished optimising {file_obj.name}. Compressed by {size}!")

            return await response.file(result_fp)

        except Exception as e:
            logging.exception(e)
            return response.json({"status": 500, "message": str(e)}, status=500)

        finally:
            # Remove tmp dir after processing
            shutil.rmtree(tmp_dir)

    return response.json({"status": 400, "message": "No file recieved"}, status=400)


if __name__ == "__main__":
    formatter = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    date_format = "%d-%b-%y %H:%M:%S"

    logging.basicConfig(
        format=formatter,
        datefmt=date_format,
        level=logging.INFO
    )

    prepare_workdir()
    app.run(host="0.0.0.0", port=8080, debug=False, access_log=False, workers=1)

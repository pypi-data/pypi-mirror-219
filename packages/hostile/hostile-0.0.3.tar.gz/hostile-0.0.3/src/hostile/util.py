import concurrent.futures
import subprocess
import tarfile

from functools import partial
from pathlib import Path

import httpx

from tqdm import tqdm


def run(cmd: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, shell=True, cwd=cwd, check=True, text=True, capture_output=True
    )


def run_bash(cmd: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Needed because /bin/sh does not support process substitution used for tee"""
    return subprocess.run(
        ["/bin/bash", "-c", cmd], cwd=cwd, check=True, text=True, capture_output=True
    )


def run_bash_parallel(
    cmds: dict[str, str], cwd: Path | None = None, description: str = "Processing tasks"
) -> dict[str, subprocess.CompletedProcess]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as x:
        futures = {
            x.submit(partial(run_bash, cwd=cwd), cmd): k for k, cmd in cmds.items()
        }
        results = {}
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc=description,
            disable=len(cmds) == 1,
        ):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as e:
                print(f"Exception occurred during executing command:")
                print(f"{cmds[key]}")
                print(f"stderr:")
                print(f"{e.stderr}")
        return results


def fastq_path_to_stem(fastq_path: Path) -> str:
    fastq_path = Path(fastq_path)
    return fastq_path.name.removesuffix(fastq_path.suffixes[-1]).removesuffix(
        fastq_path.suffixes[-2]
    )


def parse_count_file(path: Path) -> int:
    # logging.info(f"{path=}")
    try:
        with open(path, "r") as fh:
            print()
            count = int(fh.read().strip())
    except ValueError:  # file is empty and count is zero
        count = 0
    return count


def untar_file(input_path, output_path):
    with tarfile.open(input_path) as fh:
        fh.extractall(path=output_path)


def download(url: str, path: Path) -> None:
    with open(path, "wb") as fh:
        with httpx.stream("GET", url) as response:
            total = int(response.headers["Content-Length"])
            with tqdm(
                total=total, unit_scale=True, unit_divisor=1024, unit="B"
            ) as progress:
                num_bytes_downloaded = response.num_bytes_downloaded
                for chunk in response.iter_bytes():
                    fh.write(chunk)
                    progress.update(
                        response.num_bytes_downloaded - num_bytes_downloaded
                    )
                    num_bytes_downloaded = response.num_bytes_downloaded

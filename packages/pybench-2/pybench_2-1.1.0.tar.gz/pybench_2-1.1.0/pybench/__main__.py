import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import List, Type

from loguru import logger
from yada import Parser1

from pybench.base import BenchSetup
from pybench.helper import exec

ROOT_DIR = Path(__file__).parent.parent


@dataclass
class BenchArgs:
    benchname: str
    rerun: bool = False
    output_dir: Path = field(default=ROOT_DIR / "data")


def main():
    args = Parser1(BenchArgs).parse_args()

    try:
        m = import_module(f"pybench.{args.benchname}")
    except ModuleNotFoundError:
        m = import_module(f"{args.benchname}")

    cwd = args.output_dir / args.benchname
    cwd.mkdir(exist_ok=True, parents=True)
    benchfiles: List[Path] = []

    (SetupArgs,) = [
        cls
        for name in dir(m)
        if isinstance((cls := getattr(m, name)), type)
        and issubclass(cls, BenchSetup)
        and cls is not BenchSetup
    ]  # should only have one bench per file

    for benchargs in SetupArgs.iter_configs({}):
        logger.info(
            "Benchmark {}: run method {}",
            benchargs.get_bench_name(),
            benchargs.get_method_name(),
        )

        benchfile = (
            cwd / benchargs.get_bench_name() / f"{benchargs.get_method_name()}.json"
        )
        benchfile.parent.mkdir(exist_ok=True)
        benchfiles.append(benchfile)
        if benchfile.exists():
            if args.rerun:
                benchfile.unlink()
            else:
                logger.info("Skipping existing benchmark")
                continue

        exec(
            [
                "python",
                "-m",
                "pyperf",
                "timeit",
                "--copy-env",
                "--name",
                benchargs.get_bench_name(),
                "-s",
                benchargs.get_setup(),
                "-o",
                benchfile.name,
                benchargs.get_statement(),
            ],
            cwd=benchfile.parent,
            capture_stdout=False,
        )

    # group by by benchmark
    methods: dict[str, list[Path]] = defaultdict(list)
    for benchargs in SetupArgs.iter_configs({}):
        benchfile = (
            cwd / benchargs.get_bench_name() / f"{benchargs.get_method_name()}.json"
        )
        methods[benchargs.get_method_name()].append(benchfile)

    cmpfiles = []
    for method, benchfiles in methods.items():
        outfile = cwd / f"{benchfiles[0].stem}.json"
        if outfile.exists():
            outfile.unlink()
        if len(benchfiles) == 1:
            exec(["cp", benchfiles[0], outfile])
        elif len(benchfiles) == 2:
            exec(
                [
                    "python",
                    "-m",
                    "pyperf",
                    "convert",
                    "--add",
                    benchfiles[0],
                    benchfiles[1],
                    "-o",
                    outfile,
                ]
            )
        else:
            tmpfile = cwd / f"{benchfiles[0].stem}.tmp.json"
            exec(["cp", benchfiles[0], tmpfile])
            for benchfile in benchfiles[1:]:
                exec(
                    [
                        "python",
                        "-m",
                        "pyperf",
                        "convert",
                        "--add",
                        benchfile,
                        tmpfile,
                        "-o",
                        outfile,
                    ]
                )
                shutil.move(outfile, tmpfile)
            shutil.move(tmpfile, outfile)

        cmpfiles.append(outfile)

    exec(
        [
            "python",
            "-m",
            "pyperf",
            "compare_to",
            "--table",
        ]
        + [f.name for f in cmpfiles],
        cwd=cwd,
        capture_stdout=False,
    )


if __name__ == "__main__":
    main()

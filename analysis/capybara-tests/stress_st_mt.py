#!/usr/bin/env python3
import argparse
import os
import pathlib
import subprocess
import sys


DEFAULT_COLLECTIONS = [
    "ReconstructedHcalFarForwardZDCNeutrals",
    "ReconstructedLFHCALNeutrals",
]


def run(cmd, log, env):
    print(" ".join(map(str, cmd)))
    log.parent.mkdir(parents=True, exist_ok=True)

    with open(log, "w") as f:
        subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True,
            env=env,
        )


def capybara_compare(st_file, mt_file, collection, report_subdir, env):
    report_subdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "capybara",
        "bara",
        "-m",
        collection,
        str(st_file.resolve()),
        str(mt_file.resolve()),
    ]

    p = subprocess.run(
        cmd,
        cwd=report_subdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )

    return p.returncode, p.stdout.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Stress-test EICrecon single-thread vs multi-thread reproducibility."
    )

    parser.add_argument("input", type=pathlib.Path, help="Input EDM4hep ROOT file")
    parser.add_argument(
        "-n",
        "--runs",
        type=int,
        default=20,
        help="Number of MT runs",
    )
    parser.add_argument(
        "-j",
        "--threads",
        type=int,
        default=4,
        help="Number of MT threads",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=pathlib.Path,
        default=pathlib.Path("stress_st_vs_mt"),
        help="Output directory",
    )
    parser.add_argument(
        "--tmpdir",
        type=pathlib.Path,
        default=None,
        help="Optional TMPDIR to use during reconstruction",
    )
    parser.add_argument(
        "-m",
        "--collection",
        action="append",
        dest="collections",
        default=None,
        help="Collection to compare. Can be passed multiple times.",
    )

    args = parser.parse_args()

    if not args.input.exists():
        sys.exit(f"Input file not found: {args.input}")

    if args.runs < 1:
        sys.exit("--runs must be >= 1")

    if args.threads < 1:
        sys.exit("--threads must be >= 1")

    collections = args.collections or DEFAULT_COLLECTIONS

    st_dir = args.outdir / "single"
    mt_dir = args.outdir / "multi"
    report_dir = args.outdir / "reports"

    for d in [st_dir, mt_dir, report_dir]:
        d.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()

    if args.tmpdir is not None:
        args.tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = str(args.tmpdir.resolve())

    st_file = st_dir / "rec_ST.root"

    print("Running ST reference once...")
    run(
        [
            "eicrecon",
            "-Pnthreads=1",
            f"-Ppodio:output_file={st_file}",
            str(args.input),
        ],
        args.outdir / "log_ST.txt",
        env,
    )

    for i in range(args.runs):
        print(f"\n=== MT run {i + 1} / {args.runs} ===")

        mt_file = mt_dir / f"rec_MT_{i:03d}.root"

        run(
            [
                "eicrecon",
                f"-Pnthreads={args.threads}",
                f"-Ppodio:output_file={mt_file}",
                str(args.input),
            ],
            args.outdir / f"log_MT_{i:03d}.txt",
            env,
        )

        for coll in collections:
            rep = report_dir / f"run_{i:03d}_{coll}"
            retcode, out = capybara_compare(st_file, mt_file, coll, rep, env)

            if retcode != 0:
                failure_file = args.outdir / "first_failure.txt"

                with open(failure_file, "w") as f:
                    f.write(f"run = {i}\n")
                    f.write(f"collection = {coll}\n")
                    f.write(f"ST = {st_file}\n")
                    f.write(f"MT = {mt_file}\n\n")
                    f.write(out)

                print(f"\nDIFFERENCE FOUND in run {i}, collection {coll}")
                print(out[:4000])
                print(f"\nSaved first failure info to: {failure_file}")
                sys.exit(1)

    print("\nNo ST/MT differences found.")
    print(f"Tested {args.runs} MT runs against one ST reference.")


if __name__ == "__main__":
    main()
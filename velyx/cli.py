import argparse
import json
import os

from velyx.intent.resolver import resolve_intent


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--service")
    parser.add_argument("--env")
    parser.add_argument("--catalog")
    parser.add_argument("--outdir", default="out")

    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    intent = resolve_intent(
        args.service,
        args.env,
        args.catalog
    )

    with open(f"{args.outdir}/intent.json", "w") as f:
        json.dump(intent, f, indent=2)

    print("intent snapshot generated")


if __name__ == "__main__":
    main()
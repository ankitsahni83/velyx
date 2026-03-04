import argparse
import json
import os

from velyx.intent.resolver import resolve_intent
from velyx.iac.terraform_parser import load_tfplan
from velyx.iac.posture_extractor import extract_posture
from velyx.reconcile.infra_reconciler import reconcile_intent_vs_infra
from velyx.report.render_md import render_summary_md


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--service")
    parser.add_argument("--env")
    parser.add_argument("--catalog")
    parser.add_argument("--outdir", default="out")
    parser.add_argument("--tfplan")

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


    if args.tfplan:

        tfplan = load_tfplan(args.tfplan)

        posture = extract_posture(
            tfplan,
            args.service,
            args.env
        )

        with open(f"{args.outdir}/infra_posture.json", "w") as f:
            json.dump(posture, f, indent=2)

        print("infra posture generated")

    
    if args.tfplan:
        report = reconcile_intent_vs_infra(intent, posture)

        with open(f"{args.outdir}/report.json", "w") as f:
            json.dump(report, f, indent=2)

        with open(f"{args.outdir}/summary.md", "w") as f:
            f.write(render_summary_md(report))

        print("report generated")


if __name__ == "__main__":
    main()
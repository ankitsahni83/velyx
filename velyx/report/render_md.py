def render_summary_md(report: dict) -> str:
    lines = []
    lines.append(f"# Velyx Report – {report.get('service_id')} ({report.get('env')})")
    lines.append("")
    lines.append(f"**Overall:** {report.get('overall')}")
    lines.append("")
    lines.append("## Findings")
    findings = report.get("findings", [])

    if not findings:
        lines.append("- No issues detected.")
        return "\n".join(lines)

    for f in findings:
        lines.append(f"- **{f['severity']}**: {f['expectation']}")
        lines.append(f"  - Observed: `{f['observed']}`")
        lines.append(f"  - Recommendation: {f['recommendation']}")
        if f.get("evidence"):
            lines.append(f"  - Evidence: {', '.join(f['evidence'])}")
        lines.append("")

    return "\n".join(lines)
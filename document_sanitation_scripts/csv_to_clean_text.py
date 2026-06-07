import csv
import re
from pathlib import Path


def normalize_text(text: str) -> str:
    """Normalize whitespace and remove surrounding whitespace."""
    return re.sub(r"\s+", " ", text or "").strip()


def sanitize_csv_file(csv_path: Path, output_path: Path) -> None:
    """Convert a CSV file into a cleaned text file with headers prefixed."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        rows = [row for row in reader]

    if not rows:
        return

    headers = [normalize_text(cell) for cell in rows[0]]
    lines = []

    for row_index, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue

        for col_index, value in enumerate(row):
            header = headers[col_index] if col_index < len(headers) else f"Column {col_index + 1}"
            cleaned_value = normalize_text(value)
            if cleaned_value:
                lines.append(f"{header} {cleaned_value}")
            else:
                lines.append(header)

        lines.append("")  # separate rows with a blank line

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    workspace_root = Path(__file__).resolve().parent.parent
    input_dir = workspace_root / "raw_documentation_inputs"
    output_dir = workspace_root / "documents"

    import argparse

    parser = argparse.ArgumentParser(
        description="Convert each CSV in raw_documentation_inputs into a cleaned text file."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=input_dir,
        help="Directory containing CSV input files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=output_dir,
        help="Directory to write cleaned text files.",
    )
    args = parser.parse_args()

    csv_files = sorted(args.input_dir.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"No CSV files found in {args.input_dir}")

    for csv_file in csv_files:
        output_file = args.output_dir / f"{csv_file.stem}.txt"
        sanitize_csv_file(csv_file, output_file)
        print(f"Wrote cleaned text file: {output_file}")

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ensure_package():
    package_path = ROOT / "src"
    package_path.mkdir(exist_ok=True)
    init_file = package_path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("# Package initialization for banking churn analysis\n", encoding="utf-8")


if __name__ == "__main__":
    ensure_package()

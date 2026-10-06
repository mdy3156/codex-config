"""Run with python3: outputs belong to the working project, not the skill install."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    (root / ".git").mkdir()  # An empty sandbox placeholder is not a repository.
    installed = root / "installed-skill"
    source = Path(__file__).resolve().parents[1]
    shutil.copytree(source / "assets", installed / "assets")
    (installed / "scripts").mkdir()
    script = installed / "scripts" / "new_notebook.py"
    shutil.copy2(source / "scripts" / "new_notebook.py", script)
    for repository in (False, True):
        project = root / ("repo" if repository else "plain")
        working = project / "nested"
        working.mkdir(parents=True)
        if repository:
            (project / ".git").mkdir()
            (project / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
        output_root = project if repository else working
        command = [sys.executable, str(script), "--title", "Output location"]
        subprocess.run(command, cwd=working, check=True, capture_output=True)
        output = output_root / "output/jupyter-notebook/output-location.ipynb"
        assert output.exists(), f"Notebook missing from working project: {output}"
        notebook = json.loads(output.read_text())
        assert notebook["nbformat"] == 4
        cell_ids = [cell.get("id") for cell in notebook["cells"]]
        assert all(cell_ids) and len(set(cell_ids)) == len(cell_ids)
        assert notebook["cells"][0]["source"][0] == "# Experiment: Output location\n"
        original = output.read_bytes()
        rerun = subprocess.run(command, cwd=working, capture_output=True)
        assert rerun.returncode != 0 and output.read_bytes() == original
        explicit = working / "explicit.ipynb"
        subprocess.run(command + ["--kind", "tutorial", "--out", str(explicit)],
                       cwd=working, check=True, capture_output=True)
        assert "# Tutorial:" in json.loads(explicit.read_text())["cells"][0]["source"][0]
        tutorial_ids = [cell.get("id") for cell in json.loads(explicit.read_text())["cells"]]
        assert all(tutorial_ids) and len(set(tutorial_ids)) == len(tutorial_ids)
    assert not (installed / "output").exists()
print("Notebook output-location and overwrite checks passed.")

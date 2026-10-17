import json
import subprocess
import sys
import tempfile
import os

PY = sys.executable
SCRIPT = "invoice.py"


def run(*args):
    return subprocess.run([PY, SCRIPT, *args], capture_output=True, text=True)


def write_json(data):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, f)
    f.close()
    return f.name


def test_example_json_from_repo():
    r = run("example.json")
    assert r.returncode == 0, r.stderr
    assert "Acme Corp" in r.stdout
    assert "INV-0001" in r.stdout


def test_subtotal_and_total_math():
    path = write_json({
        "invoice_number": "INV-0002", "from": "A", "to": "B",
        "items": [{"description": "x", "qty": 2, "rate": 50}],
    })
    r = run(path)
    os.unlink(path)
    assert r.returncode == 0, r.stderr
    assert "$100.00" in r.stdout  # subtotal == total, qty*rate


def test_tax_applied_when_present():
    path = write_json({
        "invoice_number": "INV-0003", "from": "A", "to": "B", "tax_rate": 10,
        "items": [{"description": "x", "qty": 1, "rate": 100}],
    })
    r = run(path)
    os.unlink(path)
    assert "Tax (10%): $10.00" in r.stdout
    assert "Total: $110.00" in r.stdout


def test_tax_row_omitted_when_zero():
    path = write_json({
        "invoice_number": "INV-0004", "from": "A", "to": "B", "tax_rate": 0,
        "items": [{"description": "x", "qty": 1, "rate": 100}],
    })
    r = run(path)
    os.unlink(path)
    assert "Tax (" not in r.stdout


def test_description_is_html_escaped():
    path = write_json({
        "invoice_number": "INV-0005", "from": "A", "to": "B",
        "items": [{"description": "<script>alert(1)</script>", "qty": 1, "rate": 10}],
    })
    r = run(path)
    os.unlink(path)
    assert "<script>" not in r.stdout
    assert "&lt;script&gt;" in r.stdout


def test_string_qty_is_html_escaped():
    # qty/rate come straight from untrusted JSON -- a non-numeric qty must
    # not be interpolated raw into the HTML (regression: it used to be).
    path = write_json({
        "invoice_number": "INV-0006", "from": "A", "to": "B",
        "items": [{"description": "x", "qty": "<img src=x onerror=alert(1)>", "rate": 1}],
    })
    r = run(path)
    os.unlink(path)
    assert r.returncode != 0 or "<img src=x" not in r.stdout


def test_output_file_written():
    path = write_json({
        "invoice_number": "INV-0007", "from": "A", "to": "B",
        "items": [{"description": "x", "qty": 1, "rate": 10}],
    })
    out_path = path + ".html"
    r = run(path, "-o", out_path)
    assert r.returncode == 0, r.stderr
    assert os.path.exists(out_path)
    content = open(out_path).read()
    assert "INV-0007" in content
    os.unlink(path)
    os.unlink(out_path)


def test_notes_omitted_when_absent():
    path = write_json({
        "invoice_number": "INV-0008", "from": "A", "to": "B",
        "items": [{"description": "x", "qty": 1, "rate": 10}],
    })
    r = run(path)
    os.unlink(path)
    assert "class='meta'>" not in r.stdout.split("Date:")[1]


if __name__ == "__main__":
    failures = 0
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {t.__name__}: {e}")
    if failures:
        print(f"{failures} failure(s)")
        sys.exit(1)
    print(f"All {len(tests)} tests passed")

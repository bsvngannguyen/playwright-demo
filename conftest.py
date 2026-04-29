import time
import os
import pytest

results = []
start_time = time.time()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        status = "PASSED" if rep.passed else "FAILED"
        error_msg = ""

        if rep.failed:
            error_msg = str(rep.longrepr)

        results.append({
            "name": item.name,
            "status": status,
            "error": error_msg
        })


def pytest_sessionfinish(session, exitstatus):
    report_path = "FULL_TEST_REPORT.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        # ====== CODE ======
        f.write("========== TEST CODE SOURCE ==========\n\n")
        # Lấy danh sách các file test duy nhất đã chạy trong session
        test_files = {str(item.fspath) for item in session.items}
        for test_file in test_files:
            f.write(f"--- File: {os.path.basename(test_file)} ---\n")
            with open(test_file, "r", encoding="utf-8") as code_file:
                f.write(code_file.read())
            f.write("\n" + "="*40 + "\n")

        # ====== RESULT ======
        f.write("\n\n========== TEST EXECUTION RESULT ==========\n")
        f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {round(time.time() - start_time, 2)}s\n")
        f.write("_" * 60 + "\n")

        for res in results:
            line = f"[{res['status']}] {res['name']}"
            f.write(line + "\n")
            if res["error"]:
                f.write(f"  Error: {res['error']}\n")

    print(f"\n✅ Full report created: {os.path.abspath(report_path)}")
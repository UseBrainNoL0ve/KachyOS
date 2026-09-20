from __future__ import annotations

import threading

from .assistant import ask_ollama
from .audit import collect_audit
from .lab import collect_runtimes, discover_labs
from .operations import read_operations
from .status import collect_status
from .telemetry import collect_telemetry, render_telemetry
from .telemetry_history import load_snapshots, render_history, save_snapshot
from .tool_manager import build_install_plan, inspect_candidates, render_plan
from .tools import catalog, check_tools, summarize_tools
from .updates import collect_updates

APP_STYLE = """
QWidget { background: #080b10; color: #d7e0ea; font-family: JetBrains Mono, monospace; }
QMainWindow { background: #080b10; }
QLabel#Title { color: #7dff9b; font-size: 30px; font-weight: 800; letter-spacing: 2px; }
QLabel#Subtitle { color: #718096; padding-left: 12px; }
QLabel#StatusDot { color: #7dff9b; font-weight: 800; }
QFrame#Card { background: #0d1219; border: 1px solid #1d2a36; border-radius: 10px; }
QLabel#CardValue { color: #7dff9b; font-size: 25px; font-weight: 800; }
QLabel#CardCaption { color: #66778a; font-size: 11px; }
QTextEdit#Panel, QListWidget { background: #0a0f15; border: 1px solid #1b2834; border-radius: 8px; }
QLineEdit, QComboBox { background: #0b1118; color: #d7e0ea; border: 1px solid #223344; padding: 9px; border-radius: 7px; }
QLineEdit:focus { border: 1px solid #7dff9b; }
QPushButton { background: #101923; color: #b9c7d5; border: 1px solid #263746; padding: 9px 16px; border-radius: 7px; }
QPushButton:hover { background: #14212c; border-color: #7dff9b; color: #7dff9b; }
QPushButton:disabled { color: #4d5b68; }
QTabWidget::pane { border: 1px solid #1b2834; border-radius: 8px; }
QTabBar::tab { background: #0b1118; color: #718096; padding: 10px 16px; margin-right: 2px; }
QTabBar::tab:selected { color: #7dff9b; border-bottom: 2px solid #7dff9b; }
QListWidget::item { padding: 7px; border-radius: 5px; }
QListWidget::item:selected { background: #11231a; color: #7dff9b; }
QLabel#Section { color: #5f7182; font-size: 10px; font-weight: 800; letter-spacing: 2px; }
QLabel#Signal { color: #7dff9b; font-weight: 700; }
QTextEdit#Console { background: #06090d; border: 1px solid #17232e; color: #91a4b5; font-size: 11px; }
"""


def dashboard_snapshot() -> dict[str, object]:
    """Collect one read-only snapshot for GUI consumers."""
    tools = check_tools()
    return {
        "status": collect_status(),
        "audit": collect_audit(),
        "tools": tools,
        "tool_summary": summarize_tools(tools),
        "updates": collect_updates(),
        "runtimes": collect_runtimes(),
        "labs": discover_labs(),
    }


def launch_gui() -> int:
    try:
        from PySide6.QtCore import QObject, QThread, QTimer, Qt, Signal
        from PySide6.QtWidgets import (
            QApplication, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
            QListWidget, QListWidgetItem, QMainWindow, QPushButton, QSplitter,
            QTabWidget, QTextEdit, QVBoxLayout, QWidget,
        )
    except ImportError:
        print("GUI dependency missing: install PySide6, then run 'kachysec gui'.")
        return 2

    class AssistantWorker(QObject):
        finished = Signal(str)
        failed = Signal(str)

        def __init__(self, question: str, model: str) -> None:
            super().__init__()
            self.question = question
            self.model = model

        def run(self) -> None:
            try:
                response = ask_ollama(self.question, model=self.model)
            except Exception as exc:
                self.failed.emit(str(exc))
            else:
                self.finished.emit(response.text)

    app = QApplication.instance() or QApplication([])
    app.setApplicationName("KachySec")
    app.setStyle("Fusion")

    window = QMainWindow()
    window.setWindowTitle("KachySec — Security Workstation")
    window.resize(1280, 820)

    root = QWidget()
    root_layout = QVBoxLayout(root)
    root_layout.setContentsMargins(22, 18, 22, 18)
    root_layout.setSpacing(12)

    header = QHBoxLayout()
    title = QLabel("KachySec")
    title.setObjectName("Title")
    subtitle = QLabel("SECURITY WORKSTATION // CONTROL PLANE")
    subtitle.setObjectName("Subtitle")
    header.addWidget(title)
    header.addWidget(subtitle)
    header.addStretch()
    status_dot = QLabel("● LOCAL // ONLINE")
    status_dot.setObjectName("StatusDot")
    header.addWidget(status_dot)
    refresh_button = QPushButton("⟳ REFRESH")
    header.addWidget(refresh_button)
    root_layout.addLayout(header)

    cards = QHBoxLayout()
    card_values: dict[str, QLabel] = {}
    for key, label in (("tools", "Tools"), ("updates", "Updates"), ("audit", "Audit"), ("runtime", "Runtimes")):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        value = QLabel("—")
        value.setObjectName("CardValue")
        caption = QLabel(label)
        caption.setObjectName("CardCaption")
        layout.addWidget(value)
        layout.addWidget(caption)
        cards.addWidget(card)
        card_values[key] = value
    root_layout.addLayout(cards)

    tabs = QTabWidget()
    overview_page = QWidget()
    overview_layout = QVBoxLayout(overview_page)
    section = QLabel("LIVE OPERATIONS // SECURITY CONTROL")
    section.setObjectName("Section")
    overview_layout.addWidget(section)
    signal = QLabel("● TELEMETRY LINK  ·  LOCAL HOST  ·  READ-ONLY")
    signal.setObjectName("Signal")
    overview_layout.addWidget(signal)
    overview = QTextEdit()
    overview.setReadOnly(True)
    overview.setObjectName("Panel")
    overview_layout.addWidget(overview, 1)
    console = QTextEdit()
    console.setReadOnly(True)
    console.setObjectName("Console")
    console.setMaximumHeight(120)
    overview_layout.addWidget(console)
    tabs.addTab(overview_page, "◈  COMMAND")

    assistant_page = QWidget()
    assistant_layout = QVBoxLayout(assistant_page)
    assistant_help = QLabel(
        "Local cybersecurity copilot. It receives a read-only KachySec snapshot and answers without executing commands."
    )
    assistant_help.setWordWrap(True)
    assistant_layout.addWidget(assistant_help)

    assistant_output = QTextEdit()
    assistant_output.setReadOnly(True)
    assistant_output.setObjectName("Panel")
    assistant_output.setPlaceholderText("Assistant responses will appear here.")
    assistant_layout.addWidget(assistant_output, 1)

    assistant_row = QHBoxLayout()
    assistant_input = QLineEdit()
    assistant_input.setPlaceholderText("Ask about an audit warning, tool, lab, recon plan, or security concept…")
    assistant_model = QLineEdit("qwen2.5:7b")
    assistant_model.setMaximumWidth(150)
    assistant_send = QPushButton("▶ RUN QUERY")
    assistant_row.addWidget(assistant_input, 1)
    assistant_row.addWidget(assistant_model)
    assistant_row.addWidget(assistant_send)
    assistant_layout.addLayout(assistant_row)
    tabs.addTab(assistant_page, "⌁  COPILOT")

    tools_page = QWidget()
    tools_layout = QVBoxLayout(tools_page)
    toolbar = QHBoxLayout()
    search = QLineEdit()
    search.setPlaceholderText("Search tools by name, category, purpose, or binary…")
    category = QComboBox()
    category.addItem("All categories")
    toolbar.addWidget(search, 1)
    toolbar.addWidget(category)
    tools_layout.addLayout(toolbar)

    splitter = QSplitter(Qt.Orientation.Horizontal)
    tool_list = QListWidget()
    detail = QTextEdit()
    detail.setReadOnly(True)
    detail.setObjectName("Panel")
    splitter.addWidget(tool_list)
    splitter.addWidget(detail)
    splitter.setSizes([620, 560])
    tools_layout.addWidget(splitter, 1)

    plan_button = QPushButton("⚙ BUILD INSTALL PLAN")
    plan_button.setToolTip("Preview a pacman installation plan. No package changes are made.")
    tools_layout.addWidget(plan_button)
    tabs.addTab(tools_page, "▣  TOOLKIT")

    audit_page = QTextEdit()
    audit_page.setReadOnly(True)
    audit_page.setObjectName("Panel")
    tabs.addTab(audit_page, "◉  AUDIT")

    updates_page = QTextEdit()
    updates_page.setReadOnly(True)
    updates_page.setObjectName("Panel")
    tabs.addTab(updates_page, "↻  UPDATES")

    labs_page = QTextEdit()
    labs_page.setReadOnly(True)
    labs_page.setObjectName("Panel")
    tabs.addTab(labs_page, "⌬  LABS")

    telemetry_page = QTextEdit()
    telemetry_page.setReadOnly(True)
    telemetry_page.setObjectName("Panel")
    tabs.addTab(telemetry_page, "⌁  TELEMETRY")

    history_page = QTextEdit()
    history_page.setReadOnly(True)
    history_page.setObjectName("Panel")
    tabs.addTab(history_page, "▤  HISTORY")

    root_layout.addWidget(tabs, 1)
    window.setCentralWidget(root)

    snapshot: dict[str, object] = {}
    visible_tools: list[dict[str, object]] = []
    active_threads: list[QThread] = []

    def render_tool_detail() -> None:
        row = tool_list.currentRow()
        if row < 0 or row >= len(visible_tools):
            detail.setPlainText("Select a tool to inspect its metadata and package candidates.")
            return
        item = visible_tools[row]
        spec = next(spec for spec in catalog() if spec.name == item["name"])
        package_lines = []
        for candidate in inspect_candidates(spec):
            state = "installed" if candidate.installed else ("available" if candidate.available else "not found")
            package_lines.append(f"• {candidate.package} — {state}")
        verification = " ".join(str(x) for x in spec.verification)
        detail.setPlainText(
            f"{item['name']}\n{'=' * len(str(item['name']))}\n\n"
            f"Category: {item['category']}\nBinary: {item['binary']}\n"
            f"Scope: {item['scope']}\nInstalled: {'yes' if item['installed'] else 'no'}\n\n"
            f"Purpose\n{item['purpose']}\n\nPackage candidates\n"
            + ("\n".join(package_lines) if package_lines else "No package metadata.")
            + f"\n\nVerification\n{verification}\n\n"
            "No installation is performed from this view."
        )

    def filter_tools() -> None:
        query = search.text().strip().lower()
        selected_category = category.currentText()
        tool_list.clear()
        visible_tools.clear()
        for item in snapshot.get("tools", []):
            if selected_category != "All categories" and item["category"] != selected_category:
                continue
            haystack = " ".join(str(item[field]) for field in ("name", "category", "purpose", "binary")).lower()
            if query and query not in haystack:
                continue
            visible_tools.append(item)
            marker = "●" if item["installed"] else "○"
            tool_list.addItem(QListWidgetItem(f"{marker}  {item['name']}  ·  {item['category']}"))
        render_tool_detail()

    def render() -> None:
        nonlocal snapshot
        snapshot = dashboard_snapshot()
        summary = snapshot["tool_summary"]
        card_values["tools"].setText(f"{summary['installed']} / {summary['total']}")
        card_values["updates"].setText(str(len(snapshot["updates"])))
        audit = snapshot["audit"]
        passed = sum(1 for item in audit if item.status == "PASS")
        warnings = sum(1 for item in audit if item.status == "WARN")
        card_values["audit"].setText(f"{passed} / {warnings}")
        card_values["runtime"].setText(str(sum(1 for item in snapshot["runtimes"] if item.installed)))

        overview.setPlainText(
            "KACHYSEC // SECURITY OPERATIONS CENTER\n"
            "════════════════════════════════════════════════════════════\n\n"
            "HOST  ·  CACHYOS\n"
            f"TOOLS       {summary['installed']:>3} / {summary['total']:<3} online in catalog\n"
            f"AUDIT       {passed:>3} PASS   {warnings:>3} WARN\n"
            f"UPDATES     {len(snapshot['updates']):>3} pending\n"
            f"LABS        {sum(1 for item in snapshot['runtimes'] if item.installed):>3} runtimes available\n\n"
            "OPERATOR PIPELINE\n"
            "01 DISCOVER    02 INSPECT    03 COPILOT    04 PLAN\n"
            "05 AUTHORIZE   06 EXECUTE    07 VERIFY     08 EVIDENCE\n\n"
            "SECURITY BOUNDARY\n"
            "Discovery and planning are read-only. State-changing or network-active work remains explicit, scoped, and operator-controlled."
        )
        console.setPlainText(
            "[KACHYSEC] local control plane initialized\n"
            f"[TOOLS] catalog={summary['total']} installed={summary['installed']}\n"
            f"[AUDIT] pass={passed} warn={warnings}\n"
            f"[UPDATES] pending={len(snapshot['updates'])}\n"
            "[COPILOT] advisory mode / command execution disabled\n"
            "[EVIDENCE] local telemetry + operation history available"
        )

        current = category.currentText()
        category.blockSignals(True)
        category.clear()
        category.addItem("All categories")
        for name in sorted({str(item["category"]) for item in snapshot["tools"]}):
            category.addItem(name)
        if current in [category.itemText(i) for i in range(category.count())]:
            category.setCurrentText(current)
        category.blockSignals(False)
        filter_tools()

        audit_lines = ["READ-ONLY SECURITY AUDIT", ""]
        for item in audit:
            audit_lines.append(f"[{item.status}] {item.name} — {item.summary}")
            if item.evidence:
                audit_lines.append(f"  Evidence: {item.evidence.splitlines()[0]}")
            if item.remediation:
                audit_lines.append(f"  Review: {item.remediation}")
        audit_page.setPlainText("\n".join(audit_lines))

        updates = snapshot["updates"]
        update_lines = ["PACKAGE UPDATES", ""]
        update_lines.extend(f"{item.name}: {item.current} → {item.available}" for item in updates)
        if not updates:
            update_lines.append("No pending package updates reported by pacman.")
        update_lines.extend(("", "Read-only: no packages were modified."))
        updates_page.setPlainText("\n".join(update_lines))

        runtime_lines = ["LAB RUNTIMES", ""]
        for item in snapshot["runtimes"]:
            marker = "[+]" if item.installed else "[-]"
            runtime_lines.append(f"{marker} {item.name} — {item.version or 'not installed'}")
        runtime_lines.extend(("", "LOCAL LAB DEFINITIONS", ""))
        labs = snapshot["labs"]
        runtime_lines.extend(f"• {lab.name} [{lab.kind}] — {lab.description}" for lab in labs)
        if not labs:
            runtime_lines.append("• No local lab definitions discovered.")
        runtime_lines.extend(("", "No lab lifecycle action was executed."))
        labs_page.setPlainText("\n".join(runtime_lines))

        telemetry_snapshot = collect_telemetry()
        save_snapshot(telemetry_snapshot)
        telemetry_page.setPlainText(
            render_telemetry(telemetry_snapshot) + "\n\n" + render_history(load_snapshots(12))
        )

        records = read_operations()
        history_lines = ["LOCAL OPERATION HISTORY", ""]
        if not records:
            history_lines.append("No recorded operations yet.")
        for record in reversed(records[-50:]):
            history_lines.append(f"[{record.get('returncode')}] {record.get('operation')} — {record.get('started_at')}")
            history_lines.append("  " + " ".join(str(x) for x in record.get("command", [])))
            output = str(record.get("output", ""))
            if output:
                history_lines.append("  " + output.splitlines()[0])
        history_lines.append("")
        history_lines.append("History is read from local JSONL state and is never committed automatically.")
        history_page.setPlainText("\n".join(history_lines))

    def ask_assistant() -> None:
        question = assistant_input.text().strip()
        model = assistant_model.text().strip() or "qwen2.5:7b"
        if not question:
            return
        assistant_input.clear()
        assistant_output.append(f"\nYOU\n{question}\n")
        assistant_output.append("ASSISTANT\nWorking with the current KachySec snapshot…")
        assistant_send.setEnabled(False)

        thread = QThread(window)
        worker = AssistantWorker(question, model)
        worker.moveToThread(thread)

        def success(text: str) -> None:
            assistant_output.append(text)

        def failure(message: str) -> None:
            assistant_output.append(f"Assistant error: {message}")

        def cleanup() -> None:
            assistant_send.setEnabled(True)
            if thread in active_threads:
                active_threads.remove(thread)
            worker.deleteLater()
            thread.deleteLater()

        worker.finished.connect(success)
        worker.failed.connect(failure)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        thread.finished.connect(cleanup)
        active_threads.append(thread)
        thread.started.connect(worker.run)
        thread.start()

    refresh_button.clicked.connect(render)
    assistant_send.clicked.connect(ask_assistant)
    assistant_input.returnPressed.connect(ask_assistant)
    search.textChanged.connect(lambda _text: filter_tools())
    category.currentTextChanged.connect(lambda _text: filter_tools())
    tool_list.currentRowChanged.connect(lambda _row: render_tool_detail())
    plan_button.clicked.connect(lambda: detail.setPlainText(render_plan(build_install_plan(list(catalog())))))

    timer = QTimer(window)
    timer.setInterval(10_000)
    timer.timeout.connect(render)
    timer.start()

    window.setStyleSheet(APP_STYLE)

    render()
    window.show()
    return app.exec()

from __future__ import annotations

from .audit import collect_audit
from .status import collect_status
from .tools import check_tools, summarize_tools
from .updates import collect_updates


def dashboard_snapshot() -> dict[str, object]:
    """Collect one read-only snapshot for GUI consumers."""
    tools = check_tools()
    return {
        "status": collect_status(),
        "audit": collect_audit(),
        "tools": tools,
        "tool_summary": summarize_tools(tools),
        "updates": collect_updates(),
    }


def launch_gui() -> int:
    try:
        from PySide6.QtCore import QTimer, Qt
        from PySide6.QtWidgets import (
            QApplication,
            QFrame,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QListWidget,
            QListWidgetItem,
            QMainWindow,
            QPushButton,
            QTabWidget,
            QVBoxLayout,
            QWidget,
        )
    except ImportError:
        print("GUI dependency missing: install PySide6, then run 'kachysec gui'.")
        return 2

    app = QApplication.instance() or QApplication([])
    app.setApplicationName("KachySec")
    app.setStyle("Fusion")

    window = QMainWindow()
    window.setWindowTitle("KachySec — Security Workstation")
    window.resize(1180, 760)

    root = QWidget()
    root_layout = QVBoxLayout(root)
    root_layout.setContentsMargins(24, 20, 24, 20)
    root_layout.setSpacing(14)

    header = QHBoxLayout()
    title = QLabel("KachySec")
    title.setObjectName("Title")
    subtitle = QLabel("CachyOS security workstation control plane")
    subtitle.setObjectName("Subtitle")
    header.addWidget(title)
    header.addWidget(subtitle)
    header.addStretch()
    refresh_button = QPushButton("Refresh")
    header.addWidget(refresh_button)
    root_layout.addLayout(header)

    cards = QHBoxLayout()
    card_values: dict[str, QLabel] = {}
    for key, label in (
        ("tools", "Tools"),
        ("updates", "Updates"),
        ("audit", "Audit"),
        ("runtime", "Runtime"),
    ):
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
    overview = QLabel(
        "Read-only dashboard. Refreshing this view never installs packages, "
        "changes services, or performs network probing."
    )
    overview.setWordWrap(True)
    overview.setAlignment(Qt.AlignmentFlag.AlignTop)
    overview.setObjectName("Panel")
    tabs.addTab(overview, "Overview")

    tools_page = QWidget()
    tools_layout = QVBoxLayout(tools_page)
    search = QLineEdit()
    search.setPlaceholderText("Filter tools by name, category, or purpose…")
    tool_list = QListWidget()
    tools_layout.addWidget(search)
    tools_layout.addWidget(tool_list)
    tabs.addTab(tools_page, "Tools")

    audit_page = QLabel()
    audit_page.setWordWrap(True)
    audit_page.setAlignment(Qt.AlignmentFlag.AlignTop)
    audit_page.setObjectName("Panel")
    tabs.addTab(audit_page, "Audit")

    updates_page = QLabel()
    updates_page.setWordWrap(True)
    updates_page.setAlignment(Qt.AlignmentFlag.AlignTop)
    updates_page.setObjectName("Panel")
    tabs.addTab(updates_page, "Updates")

    root_layout.addWidget(tabs)
    window.setCentralWidget(root)

    snapshot: dict[str, object] = {}

    def render() -> None:
        nonlocal snapshot
        snapshot = dashboard_snapshot()

        summary = snapshot["tool_summary"]
        card_values["tools"].setText(
            f"{summary['installed']} / {summary['total']}"
        )
        updates = snapshot["updates"]
        card_values["updates"].setText(str(len(updates)))
        audit = snapshot["audit"]
        passed = sum(1 for item in audit if item.status == "PASS")
        warnings = sum(1 for item in audit if item.status == "WARN")
        card_values["audit"].setText(f"{passed} / {warnings}")
        status = snapshot["status"]
        runtime_count = sum(1 for value in status.get("runtimes", {}).values() if value)
        card_values["runtime"].setText(str(runtime_count))

        tool_list.clear()
        query = search.text().strip().lower()
        for item in snapshot["tools"]:
            haystack = " ".join(
                str(item[field]) for field in ("name", "category", "purpose")
            ).lower()
            if query and query not in haystack:
                continue
            marker = "●" if item["installed"] else "○"
            QListWidgetItem(
                f"{marker}  {item['name']}   ·   {item['category']}   —   {item['purpose']}",
                tool_list,
            )

        audit_lines = ["READ-ONLY SECURITY AUDIT", ""]
        for item in audit:
            audit_lines.append(f"{item.status:<5} {item.name} — {item.summary}")
            if item.evidence:
                audit_lines.append(f"      {item.evidence}")
        audit_page.setText("\n".join(audit_lines))

        update_lines = ["PACKAGE UPDATES", ""]
        if updates:
            update_lines.extend(
                f"{item.name}: {item.current} → {item.available}"
                for item in updates
            )
        else:
            update_lines.append("No pending package updates reported by pacman.")
        update_lines.append("")
        update_lines.append("Read-only: no packages were modified.")
        updates_page.setText("\n".join(update_lines))

    refresh_button.clicked.connect(render)
    search.textChanged.connect(lambda _text: render())
    timer = QTimer(window)
    timer.setInterval(10_000)
    timer.timeout.connect(render)
    timer.start()

    window.setStyleSheet(
        """
        QMainWindow { background: palette(window); }
        QLabel#Title { font-size: 30px; font-weight: 700; }
        QLabel#Subtitle { padding-left: 12px; color: palette(mid); }
        QFrame#Card { border: 1px solid palette(mid); border-radius: 12px; }
        QLabel#CardValue { font-size: 26px; font-weight: 700; }
        QLabel#CardCaption { color: palette(mid); }
        QLabel#Panel { padding: 18px; }
        QLineEdit { padding: 10px; border-radius: 8px; }
        QListWidget { padding: 8px; border-radius: 8px; }
        QPushButton { padding: 9px 16px; border-radius: 8px; }
        """
    )

    render()
    window.show()
    return app.exec()

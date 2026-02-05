from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


DEFAULT_DATA_PATH = Path("data/protocols/protocols_seed.fr-CH.json")


def _resolve_data_path(path: Path) -> Path:
    if path.exists():
        return path
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        bundled = Path(sys._MEIPASS) / "data" / "protocols" / path.name
        if bundled.exists():
            return bundled
    return path


@dataclass
class Protocol:
    protocol_id: str
    title: str
    red_flags: list[str]
    checklist: list[str]


@dataclass
class ProtocolCatalog:
    locale: str
    updated_at: str
    disclaimer: str
    protocols: list[Protocol]
    sources: list[dict[str, str]]


class ProtocolRepository:
    @staticmethod
    def load(path: Path) -> ProtocolCatalog:
        payload = json.loads(path.read_text(encoding="utf-8"))

        meta = payload.get("meta", {})
        protocols_raw = payload.get("protocols", [])
        protocols = [
            Protocol(
                protocol_id=item["id"],
                title=item["title"],
                red_flags=list(item.get("red_flags", [])),
                checklist=list(item.get("checklist", [])),
            )
            for item in protocols_raw
        ]

        return ProtocolCatalog(
            locale=meta.get("locale", "fr-CH"),
            updated_at=meta.get("updated_at", ""),
            disclaimer=meta.get("disclaimer", ""),
            protocols=protocols,
            sources=list(payload.get("sources", [])),
        )


class ProtocolApp(ttk.Frame):
    def __init__(self, master: tk.Tk, catalog: ProtocolCatalog):
        super().__init__(master, padding=12)
        self.catalog = catalog
        self.protocol_map = {p.title: p for p in catalog.protocols}

        self.master.title("Protocoles de soins - Permanence")
        self.master.geometry("980x620")
        self.master.minsize(860, 560)

        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        self._build_header()
        self._build_left_panel()
        self._build_detail_panel()
        self._build_footer()

        if catalog.protocols:
            first = catalog.protocols[0].title
            self.protocol_listbox.set(first)
            self.render_protocol(first)

    def _build_header(self) -> None:
        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Protocoles de soins (assistantes médicales)",
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            header,
            text=f"Locale: {self.catalog.locale}  |  Mise à jour: {self.catalog.updated_at}",
        ).grid(row=1, column=0, sticky="w")

    def _build_left_panel(self) -> None:
        left = ttk.Labelframe(self, text="Protocoles", padding=8)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._refresh_list())

        ttk.Entry(left, textvariable=self.search_var).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.protocol_listbox = tk.StringVar(value=[p.title for p in self.catalog.protocols])
        self.listbox = tk.Listbox(left, listvariable=self.protocol_listbox, exportselection=False)
        self.listbox.grid(row=1, column=0, sticky="nsew")
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _build_detail_panel(self) -> None:
        right = ttk.Labelframe(self, text="Détails", padding=8)
        right.grid(row=1, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(3, weight=1)

        self.title_label = ttk.Label(right, font=("Segoe UI", 12, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.red_flags_text = tk.Text(right, wrap="word", height=8)
        self.red_flags_text.grid(row=1, column=0, sticky="ew", pady=(8, 8))

        self.checklist_text = tk.Text(right, wrap="word", height=8)
        self.checklist_text.grid(row=2, column=0, sticky="ew")

        self.sources_text = tk.Text(right, wrap="word")
        self.sources_text.grid(row=3, column=0, sticky="nsew", pady=(8, 0))

    def _build_footer(self) -> None:
        footer = ttk.Frame(self)
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        footer.columnconfigure(0, weight=1)

        ttk.Label(
            footer,
            text=f"⚠️ {self.catalog.disclaimer}",
            foreground="#8a6d3b",
        ).grid(row=0, column=0, sticky="w")

        ttk.Button(footer, text="À propos", command=self._show_about).grid(row=0, column=1, sticky="e")

    def _refresh_list(self) -> None:
        query = self.search_var.get().strip().lower()
        titles = [p.title for p in self.catalog.protocols if query in p.title.lower()]
        self.protocol_listbox.set(titles)
        if titles:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.render_protocol(titles[0])

    def _on_select(self, _event: object) -> None:
        selected = self.listbox.curselection()
        if not selected:
            return
        title = self.listbox.get(selected[0])
        self.render_protocol(title)

    def render_protocol(self, title: str) -> None:
        protocol = self.protocol_map.get(title)
        if not protocol:
            return

        self.title_label.configure(text=protocol.title)
        self._set_text(
            self.red_flags_text,
            "Drapeaux rouges\n" + "\n".join(f"• {item}" for item in protocol.red_flags),
        )
        self._set_text(
            self.checklist_text,
            "Checklist\n" + "\n".join(f"• {item}" for item in protocol.checklist),
        )

        source_lines = ["Sources de référence"]
        for src in self.catalog.sources:
            source_lines.append(
                f"• {src.get('name', '')} ({src.get('version', '')})\n  {src.get('url', '')}"
            )
        self._set_text(self.sources_text, "\n".join(source_lines))

    @staticmethod
    def _set_text(widget: tk.Text, content: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, content)
        widget.configure(state="disabled")

    def _show_about(self) -> None:
        messagebox.showinfo(
            "À propos",
            "Application de protocoles de soins\n"
            "Usage interne en permanence. Validation médicale locale obligatoire.",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Application protocoles de soins")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Chemin vers le fichier JSON des protocoles",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Valide le fichier JSON sans lancer l'interface",
    )
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    catalog = ProtocolRepository.load(_resolve_data_path(args.data))

    if args.check:
        print(f"OK: {len(catalog.protocols)} protocoles chargés depuis {args.data}")
        return 0

    root = tk.Tk()
    ProtocolApp(root, catalog)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

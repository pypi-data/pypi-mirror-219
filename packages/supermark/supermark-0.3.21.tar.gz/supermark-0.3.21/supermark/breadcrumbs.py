from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .build_html import HTMLBuilder

import yaml
from yaml.scanner import ScannerError

from .report import Report
from .utils import get_relative_path


class Page:
    def __init__(
        self, path: Path, d: Dict[str, str], children: Optional[List["Page"]] = None
    ):
        self.page = d["page"]
        self.page_path = path / Path(self.page)
        self.title = d["title"] if "title" in d else d["page"]
        # TODO handle that these are not set
        self.children = children
        self.parent = None
        if self.children:
            for child in self.children:
                child.parent = self

    def __str__(self):
        return self.title


class Breadcrumbs:
    def __init__(self, report: Report, path: Path):
        self.pages: Dict[Path, Page] = {}
        self.report = report
        self.path = path
        with open(path) as f:
            try:
                temp: Any = yaml.safe_load(f)
                self.roots = self.parse_breadcrumbs(temp, path.parent)
            except ScannerError as e:
                self.report.warning(str(e), path)

    def parse_breadcrumbs(self, l: List[Any], path: Path) -> List[Any]:
        """[{page}, [children]]"""
        tchildren = []
        for i in range(len(l)):
            item = l[i]
            if isinstance(item, dict):
                if i < len(l) - 1 and isinstance(l[i + 1], list):
                    children = self.parse_breadcrumbs(l[i + 1], path)
                else:
                    children = None
                page = Page(path, item, children=children)
                tchildren.append(page)
                page_path = path / Path(item["page"])
                if not page_path.exists():
                    self.report.warning(
                        f"Page {item['page']} in breadcrumbs does not exist.", self.path
                    )
                self.pages[page_path] = page
        return tchildren

    def has_breadcrumbs(self, page: Path) -> bool:
        return page in self.pages

    def get_trail(self, page_path: Path) -> List[Page]:
        trail: List[Page] = []
        while page_path in self.pages:
            p = self.pages[page_path]
            trail.append(p)
            if p.parent:
                page_path = p.parent.page_path
            else:
                break
        trail.reverse()
        return trail

    def get_html(self, input_page: Path, builder: "HTMLBuilder") -> str:

        html: List[str] = []
        divider = "url(&#34;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8'%3E%3Cpath d='M2.5 0L1 1.5 3.5 4 1 6.5 2.5 8l4-4-4-4z' fill='%236c757d'/%3E%3C/svg%3E&#34;)"
        html.append(
            f'<nav style="--bs-breadcrumb-divider: {divider};" aria-label="breadcrumb">'
        )
        html.append('<ol class="breadcrumb">')
        for page in self.get_trail(input_page):
            if page.page_path == input_page:
                html.append(
                    f'<li class="breadcrumb-item active" aria-current="page">{page.title}</li>'
                )
            else:
                path = get_relative_path(
                    builder.get_target_file(input_page),
                    builder.get_target_file(page.page_path),
                )
                html.append(
                    f'<li class="breadcrumb-item"><a href="{path}">{page.title}</a></li>'
                )
        html.append("</ol>")
        html.append("</nav>")
        return "\n".join(html)


class Page2:
    def __init__(self, path: Path, title: str):
        self.path = path
        self.title = title
        self.children: List[Page2] = []

    def get_list(self) -> List[Any]:
        if len(self.children) > 0:
            children = [x.get_list() for x in self.children]
            return [{"path": self.path, "title": self.title}, children]
        else:
            return [{"path": self.path, "title": self.title}]

from pathlib import Path
from shutil import copy
from typing import List, Sequence, Set

import supermark.doc

from .base import Extension
from .chunks import Builder, Chunk
from .examples_yaml import YAMLExamples
from .report import Report
from .utils import write_file
from .write_md import nav_link_back

DOC_FOLDER = "supermark"


class DocBuilder(Builder):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        base_path: Path,
        template_file: Path,
        report: Report,
        verbose: bool = False,
    ) -> None:
        super().__init__(
            input_path,
            output_path,
            base_path,
            template_file,
            report,
            verbose,
        )
        self.target_folder = input_path / DOC_FOLDER

    def find_used_extensions(self) -> Set[Extension]:
        files = list(
            self.input_path.glob(
                "**/*.md",
            )
        )
        files = [file for file in files if not file.match(f"{DOC_FOLDER}/**")]
        extensions_used: Set[Extension] = set()
        for source_file_path in files:
            _ = self.parse_file(source_file_path, extensions_used)
        return extensions_used

    def build(
        self,
    ) -> None:
        self.target_folder.mkdir(exist_ok=True)
        self.copy_docs()

        extensions_used = self.find_used_extensions()

        # Overview page
        md: List[str] = []
        nav_link_back("Documentation", "index.html", md)
        md.append("# Extensions")
        for used in [True, False]:
            if used:
                md.append("### Extensions used in this Site")
            else:
                md.append("### Other Extensions")
            md.append("<ul>")
            # for folder in sorted(folders):
            folders: set[Path] = set()
            for extension in self.core.get_all_extensions():
                # Extensions can show up several times, but folder is unique
                folder = extension.folder
                if folder in folders:
                    continue
                folders.add(extension.folder)
                is_used = extension in extensions_used
                if is_used != used:
                    continue
                x = str(folder.name)
                doc = extension.get_doc_summary()
                if doc is None:
                    doc = ""
                md.append(f'<li><a href="{x}.html">{x}</a> {doc}</li>')
            md.append("</ul>\n\n\n\n")
            write_file("\n".join(md), self.target_folder / "extensions.md", self.report)

        # Page for each extension
        for extension in self.core.get_all_extensions():
            # for folder in folders:
            folder = extension.folder
            mdx: List[str] = []
            nav_link_back("All extensions", "extensions.html", mdx)
            is_first_extension_of_folder = True
            for e in self.core.get_all_extensions():
                if e.folder == folder and is_first_extension_of_folder:
                    self._build_extension(e, mdx, is_first_extension_of_folder)
                    is_first_extension_of_folder = False
            write_file(
                "\n".join(mdx),
                self.target_folder / f"{folder.name}.md",
                self.report,
            )

    def copy_docs(self):
        for file in Path(supermark.doc.__file__).parent.glob("*.md"):
            copy(file, self.target_folder)

    def _build_extension(
        self, extension: Extension, md: List[str], is_first_extension_of_folder: bool
    ):
        md.append(f"\n\n# Extension {extension.folder.name}\n")
        doc = extension.get_doc()
        if doc is not None and doc.exists() and is_first_extension_of_folder:
            with open(doc, encoding="utf-8") as file:
                lines = file.readlines()
                md.append("".join(lines))

        example_chunks = self._load_example_chunks(extension)

        ye = YAMLExamples(example_chunks)
        ye.write_doc(md)

        # table = extension.get_doc_table(example_chunks)
        # if table is not None:
        #    table.flush_row_group()
        #    md.append("\n\n\n")
        #    md.append(table.get_html())
        #    md.append("\n\n\n")

        for index, example in enumerate(extension.get_examples()):
            if example.exists():
                self._build_example(extension, example, index, md)

    def _load_example_chunks(
        self,
        extension: Extension,
    ) -> Sequence[Chunk]:
        example_chunks: List[Chunk] = []
        for example in extension.get_examples():
            chunks = self.core.parse_file(example)
            if chunks is not None:
                for c in chunks:
                    example_chunks.append(c)
        return example_chunks

    def _build_example(
        self, extension: Extension, example: Path, index: int, md: List[str]
    ):
        md.append(f"\n\n# Example {index+1}\n")
        code: str = ""
        # include example directly, to show the result
        with open(example, encoding="utf-8") as file:
            code = "".join(file.readlines())
        md.append(code)
        md.append("\n\n\n")
        md.append("\n\n## Source Code\n")
        # include code of the example
        md.append(f"```{self._guess_code_language(code)}")
        md.append(code)
        md.append("```")
        md.append("\n\n\n")

    def _guess_code_language(self, code: str) -> str:
        if code.startswith("---"):
            return "yaml"
        return ""

import ast
import copy
import difflib
import gzip
import hashlib
import os
import pickle
import re
import shutil
import stat
import subprocess
import tempfile
import textwrap
from functools import cached_property
from pathlib import Path
from typing import Any, Callable, Dict, List, Match, Tuple, NamedTuple

import merge3
import tomlkit
from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option
from poetry.plugins.application_plugin import ApplicationPlugin
from tomlkit.container import OutOfOrderTableProxy as TomlOutOfOrderTable
from tomlkit.items import AoT as TomlAoT
from tomlkit.items import Item as TomlItem
from tomlkit.items import Table as TomlTable

FileState = Dict[str, Any]


class LogEntry(NamedTuple):
    id: str
    author: str
    date: str
    comment: str


class TemplateState:
    files: Dict[Path, FileState]
    repository: str
    questions: Dict[str, Any]
    context: Dict[str, Any]
    log_id: str | None = None

    def __init__(self, repository: str, context: Dict[str, Any]):
        self.repository = repository
        self.files = {}
        self.questions = {}
        self.context = context

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def dumps(self) -> None:
        Path("pytemplate.state").write_bytes(gzip.compress(pickle.dumps(self)))

    @classmethod
    def loads(cls) -> "TemplateState":
        if not Path("pytemplate.state").exists():
            raise RuntimeError("Missing pytemplate.state file")
        return pickle.loads(gzip.decompress(Path("pytemplate.state").read_bytes()))


class TemplateBaseCommand(Command):
    dump_state = True

    def handle(self) -> int:
        state = self.get_state()
        target_dir = self.get_target_dir()
        new_state = copy.deepcopy(state)
        self.handle_command(new_state, target_dir)
        if self.dump_state and new_state != state:
            self.print("\u2757 Save state")
            new_state.dumps()
        return 0

    def handle_command(self, state: TemplateState, target_dir: Path) -> None:
        raise NotImplementedError()

    def get_state(self) -> TemplateState:
        return TemplateState.loads()

    def get_target_dir(self) -> Path:
        return Path(os.getcwd())

    def print(self, message: str) -> None:
        self.io.write_line(message)

    def print_file(self, path: Path, flag: str, ignore: bool = False, conflict: bool = False, **_kwargs: Any) -> None:
        if ignore:
            self.print(f"<fg=cyan>\u24e7  {path}</>")
            return
        extra = "[conflict]" if conflict else ""
        if flag == "initial":
            color, icon = "yellow", "\u24d8"
        elif flag == "optional":
            color, icon = "blue", "\u24de"
        elif flag == "protected":
            color, icon = "magenta", "\u24df"
        else:
            color, icon = "gray", "?"
        if conflict:
            color = "red"
        self.print(f"<fg={color}>{icon}  {path} {extra}</>")


class TemplateCommand(TemplateBaseCommand):
    def handle_command(self, state: TemplateState, target_dir: Path) -> None:
        logs = self.get_logs(state)
        files = self.get_files(state)

        if not target_dir.exists():
            os.makedirs(target_dir)
        os.chdir(target_dir)

        self.handle_files(state, files, logs)
        self.done()

    def get_files(self, state) -> Dict[Path, "File"]:
        tmp_dir = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            subprocess.check_output(
                ["git", "clone", "--depth=1", f"ssh://{state.repository}", tmp_dir],
                stderr=subprocess.DEVNULL,
            )
            os.chdir(tmp_dir)
            files = self.init_template(state)
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp_dir)
        return files

    def get_logs(self, state: TemplateState) -> List[LogEntry]:
        tmp_dir = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            subprocess.check_output(
                ["git", "clone", "--bare", f"ssh://{state.repository}", tmp_dir],
                stderr=subprocess.DEVNULL,
            )
            os.chdir(tmp_dir)
            result = subprocess.check_output(
                ["git", "--no-pager", "log", '--pretty=%H#%an#%aI#%s'],
                stderr=subprocess.DEVNULL,
            ).decode("utf-8")
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp_dir)
        logs = []
        for rec in result.splitlines():
            entry = LogEntry(*rec.split('#', 3))
            if entry.id == state.log_id:
                break
            logs.append(entry)
        return logs

    def init_template(self, state: TemplateState) -> Dict[Path, "File"]:
        files = {
            p: {"flag": "protected", "readonly": True}
            for p in Path(".").glob("**/*")
            if not p.is_relative_to(".git") and not p.is_dir()
        }
        globals_ = {
            "current_version": state.context.get("version", (1, 0, 0)),
            "exclude": self.cmd_exclude(files),
            "set_initial": self.cmd_set_initial(files),
            "set_protected": self.cmd_set_protected(files),
            "set_optional": self.cmd_set_optional(files),
            "ask": self.cmd_ask(state),
            "print": self.cmd_print,
            "__builtins__": {},
        }
        context = {**state.context}
        if Path("pytemplate.py").exists():
            exec(Path("pytemplate.py").read_text(encoding="utf-8"), globals_, context)
            globals_["exclude"](["pytemplate.py"])  # type:ignore
            state.context = {**context}

        def repl(m: Match) -> str:
            val = repr(context.get(m.group(1), ""))
            return val[1:-1].replace('"', '\\"') if val.startswith("'") else val[1:-1].replace("'", "\\'")

        result: Dict[Path, File] = {}
        for path, options in files.items():
            if path.name.startswith("@"):
                content = re.sub(r"{%\s*([a-zA-Z_0-9]+)\s*%}", repl, path.read_text(encoding="utf-8")).encode("utf-8")
            else:
                content = path.read_bytes()
            mode = path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            path = (path.parent / path.name[1:]) if (path.name.startswith("@") or path.name.startswith("#")) else path
            result[path] = FILES.get(path.suffix, File)(state.files.setdefault(path, {}), path, options, mode, content)
        return result

    def handle_files(self, state: TemplateState, files: Dict[Path, "File"], logs: List[LogEntry]) -> None:
        raise NotImplementedError()

    def show_logs(self, logs) -> None:
        for rec in logs:
            self.print(f"<fg=magenta>{rec.author} <fg=yellow>{rec.date}</></>:")
            self.print(f"{textwrap.indent(rec.comment, '  ')}")
            self.print("")

    def done(self) -> None:
        self.print("\u2728 Done!")

    def walk_template_files(
        self, files: Dict[Path, Dict[str, Any]], patterns: List[str] | str, fn: Callable[[Dict[Path, Any], Path], Any]
    ) -> None:
        if isinstance(patterns, str):
            patterns = [patterns]
        for pattern in patterns:
            for path in Path(".").glob(str(pattern)):
                if path in files:
                    fn(files, path)

    def write_file(self, file: "File") -> bool:
        self.print_file(file.path, flag=file.options["flag"], conflict=file.merged_content.has_conflicts)
        return file.write()

    def cmd_set_initial(self, files: Dict[Path, Dict[str, Any]]) -> Callable[[List[str]], None]:
        def set_initial(patterns: List[str] | str) -> None:
            self.walk_template_files(files, patterns, lambda t, p: t[p].update({"flag": "initial", "readonly": False}))

        return set_initial

    def cmd_set_optional(self, files: Dict[Path, Dict[str, Any]]) -> Callable[[List[str]], None]:
        def set_optional(patterns: List[str] | str) -> None:
            self.walk_template_files(
                files, patterns, lambda t, p: t[p].update({"flag": "optional", "readonly": False})
            )

        return set_optional

    def cmd_set_protected(self, files: Dict[Path, Dict[str, Any]]) -> Callable[[List[str]], None]:
        def set_protected(patterns: List[str] | str, readonly: bool = True) -> None:
            self.walk_template_files(
                files, patterns, lambda t, p: t[p].update({"flag": "protected", "readonly": readonly})
            )

        return set_protected

    def cmd_exclude(self, files: Dict[Path, Dict[str, Any]]) -> Callable[[List[str]], None]:
        def exclude(patterns: List[str] | str) -> None:
            self.walk_template_files(files, patterns, lambda t, p: t.pop(p))

        return exclude

    def cmd_ask(self, state: TemplateState) -> Callable:
        def ask(question: str, default: Any = None) -> Any:
            if question in state.questions:
                return state.questions[question]
            answer = state.questions[question] = self.ask(question, default)
            return answer

        return ask

    def cmd_print(self, message: str) -> None:
        self.print(message)


class TemplateInitCommand(TemplateCommand):
    name = "template init"
    description = "Create project from template."
    arguments = [
        argument("repository", "Template repository.", multiple=False),
        argument("target", "Target directory name.", multiple=False),
    ]

    def get_state(self) -> TemplateState:
        return TemplateState(repository=self.argument("repository"), context={"target": self.argument("target")})

    def get_target_dir(self) -> Path:
        target = Path(os.getcwd()) / self.argument("target")
        if target.exists() and not target.is_dir():
            raise RuntimeError(f"File {target} exists.")
        if any(target.glob("*")):
            raise RuntimeError(f"Target directory {target} is not empty.")
        return target

    def handle_files(self, state: TemplateState, files: Dict[Path, "File"], logs: List[LogEntry]) -> None:
        self.print("\U0001f680 Init template...")
        for file in files.values():
            self.write_file(file)
        if logs:
            state.log_id = logs[0].id

    def done(self) -> None:
        self.call("update")
        super().done()


class TemplateUpdateCommand(TemplateCommand):
    name = "template update"
    description = "Update project from template."
    arguments = []
    options = [
        option("update", description="Run poetry update."),
    ]

    def get_update_files(self, state: TemplateState, files: Dict[Path, "File"]) -> "List[Tuple[str, Path | File]]":
        result: List[Tuple[str, Path | File]] = []
        error = False
        for path in sorted(set(state.files).union(files)):
            if path not in files:
                result.append(("delete", path))
                continue
            file = files[path]
            if file.is_ignored or file.is_initial:
                continue
            if file.is_new and file.exists():
                error = True
                self.print(f"<fg=yellow>\u2757 file {file.path} already exists</>")
                continue
            if file.exists() and not file.is_file():
                error = True
                self.print(f"<fg=yellow>\u2757 {file.path} is not a regular file</>")
                continue
            if file.is_new:
                result.append(("create", file))
            elif not file.exists():
                result.append(("restore", file))
            elif file.is_changed:
                result.append(("merge", file))

        if error:
            raise RuntimeError("Fix errors and try again")

        return result

    def check_conflicts(self, state: TemplateState) -> None:
        conflicts = [(path, meta) for path, meta in sorted(state.files.items()) if meta.get("conflict")]
        if conflicts:
            self.print("<fg=yellow>\u2757 There are unresolved conflicts:</>")
            for path, meta in conflicts:
                self.print_file(path, **meta)
            self.print("")
            self.print("<fg=yellow>\u2757 Resolve conflicts and tag files using `poetry template fix`</>")
            raise RuntimeError("Cancelled")

    def handle_files(self, state: TemplateState, files: Dict[Path, "File"], logs: List[LogEntry]) -> None:
        self.print("\U0001f680 Start update...")
        self.print("")
        self.check_conflicts(state)

        if state.log_id is not None:
            self.show_logs(logs)

        remove: List[Path] = []
        write: List[File] = []

        for what, file in self.get_update_files(state, files):
            if what == "delete":
                self.print(f"<fg=yellow>\u2757 [-] <fg=magenta>{file}</> will be deleted</>")
                assert isinstance(file, Path)
                remove.append(file)
                continue
            assert isinstance(file, File)
            if what == "create":
                self.print(f"<fg=yellow>\u2757 [+] <fg=magenta>{file.path}</> will be created</>")
                write.append(file)
            elif what == "restore":
                self.print(f"<fg=yellow>\u2757 [+] <fg=magenta>{file.path}</> will be restored</>")
                write.append(file)
            elif what == "merge":
                if file.unified_diff:
                    op = "will be merged" if file.is_optional else "will be overwritten"
                    conflict = "<fg=red>with CONFLICTS</>" if file.merged_content.has_conflicts else ""
                    self.print(f"<fg=yellow>\u2757 [*] <fg=magenta>{file.path}</> {op} {conflict}</>")
                    write.append(file)

        if remove or write:
            self.print("")
            if self.ask("Are you sure you want to continue? [y/N]", default="N") != "y":
                raise RuntimeError("Cancelled")
            self.print("")

        if write:
            self.print("\U0001f680 Write files...")
            for file in write:
                self.write_file(file)
            self.print("")

        if remove:
            self.print("\U0001f680 Remove files...")
            for p in remove:
                self.print(f"<fg=red>\u24e7  {p}</>")
                p.unlink(missing_ok=True)
                path = p.parent
                while path != Path(".") and not any(path.glob("*")):
                    path.rmdir()
                    path = path.parent
                state.files.pop(p)
            self.print("")

        if logs:
            state.log_id = logs[0].id

    def done(self) -> None:
        if self.option("update"):
            self.call("update")
        super().done()


class TemplateIncomingCommand(TemplateUpdateCommand):
    dump_state = False
    name = "template incoming"
    description = "Show incoming changes."
    arguments = []
    options = []

    def handle_files(self, state: TemplateState, files: Dict[Path, "File"], logs: List[LogEntry]) -> None:
        self.print("\U0001f680 Check incoming updates...")
        self.print("")
        self.check_conflicts(state)

        if state.log_id is not None:
            self.show_logs(logs)

        for what, file in self.get_update_files(state, files):
            if what == "delete":
                self.print(f"<fg=yellow>\u2757 [-] <fg=magenta>{file}</> will be deleted</>")
                self.print("=" * 79)
                continue
            assert isinstance(file, File)
            if what == "create":
                self.print(f"<fg=yellow>\u2757 [+] <fg=magenta>{file.path}</> will be created</>")
                self.print("=" * 79)
            elif what == "restore":
                self.print(f"<fg=yellow>\u2757 [+] <fg=magenta>{file.path}</> will be restored</>")
                self.print("=" * 79)
            elif what == "merge":
                if file.unified_diff:
                    op = "will be merged" if file.is_optional else "will be overwritten"
                    conflict = "<fg=red>with CONFLICTS</>" if file.merged_content.has_conflicts else ""
                    self.print(f"<fg=yellow>\u2757 [*] <fg=magenta>{file.path}</> {op} {conflict}</>")
                    self.print("-" * 79)
                    self.print_diff(file.unified_diff)
                    self.print("=" * 79)

    def print_diff(self, content: List[str]) -> None:
        for line in content:
            line = line.rstrip()
            line = self.io.output.formatter.escape(line)
            if line.startswith("-"):
                self.print(f"<fg=red>{line}</>")
            elif line.startswith("+"):
                self.print(f"<fg=green>{line}</>")
            else:
                self.print(line)

    def done(self) -> None:
        TemplateCommand.done(self)


class TemplateListCommand(TemplateBaseCommand):
    name = "template list"
    description = "Show template files."
    arguments = []
    options = []

    def handle_command(self, state: TemplateState, target_dir: Path) -> None:
        for path, meta in sorted(state.files.items()):
            self.print_file(path, **meta)


class TemplateLinkCommand(TemplateBaseCommand):
    name = "template link"
    description = "Link/unlink specified file."
    arguments = [
        argument("file", "File to link/unlink.", multiple=False),
    ]
    options = [
        option("unlink", description="Unlink"),
    ]

    def handle_command(self, state: TemplateState, target_dir: Path) -> None:
        path = Path(self.argument("file"))
        if path not in state.files:
            raise RuntimeError("Given file does not exist")
        if self.option("unlink"):
            state.files[path].update({"ignore": True})
        else:
            state.files[path].update({"ignore": False})


class TemplateFixCommand(TemplateBaseCommand):
    name = "template fix"
    description = "Fix resolved conflict."
    arguments = [
        argument("file", "File to fix.", multiple=False),
    ]

    def handle_command(self, state: TemplateState, target_dir: Path) -> None:
        path = Path(self.argument("file"))
        if path not in state.files:
            raise RuntimeError("The given file does not exist")
        if not state.files[path].get("conflict"):
            raise RuntimeError("The given file has no conflicts")
        state.files[path]["conflict"] = False
        state.files[path]["lock"] = FILES.get(path.suffix, File).get_hash(path.read_bytes())


class TemplatePlugin(ApplicationPlugin):
    def activate(self, application: Application, *args: Any, **kwargs: Any) -> None:
        application.command_loader.register_factory("template init", TemplateInitCommand)  # type:ignore
        application.command_loader.register_factory("template update", TemplateUpdateCommand)  # type:ignore
        application.command_loader.register_factory("template incoming", TemplateIncomingCommand)  # type:ignore
        application.command_loader.register_factory("template list", TemplateListCommand)  # type:ignore
        application.command_loader.register_factory("template link", TemplateLinkCommand)  # type:ignore
        application.command_loader.register_factory("template fix", TemplateFixCommand)  # type:ignore


class MergedContent(bytes):
    has_conflicts: bool = False


class File:
    def __init__(self, state: FileState, path: Path, options: Dict[str, Any], xmode: int, content: bytes):
        self.state = state
        self.path = path
        self.options = options
        self.content = content
        self.xmode = xmode

    @property
    def is_initial(self) -> bool:
        return self.options["flag"] == "initial"

    @property
    def is_optional(self) -> bool:
        return self.options["flag"] == "optional"

    @property
    def is_protected(self) -> bool:
        return self.options["flag"] == "protected"

    @property
    def is_readonly(self) -> bool:
        return bool(self.options["readonly"])

    @property
    def is_new(self) -> bool:
        return not self.state

    @property
    def is_ignored(self) -> bool:
        return bool(self.state and self.state.get("ignore"))

    @cached_property
    def is_locally_changed(self) -> bool:
        return self.state.get("lock") != self.get_hash(self.local_content)

    @cached_property
    def is_template_changed(self) -> bool:
        return self.get_hash(self.content) != self.get_hash(self.base_content)

    @cached_property
    def is_changed(self) -> bool:
        return self.is_locally_changed or self.is_template_changed

    @cached_property
    def base_content(self) -> bytes:
        return self.state.get("content") or b""

    @cached_property
    def local_content(self) -> bytes:
        if self.path.is_file():
            return self.path.read_bytes()
        return b""

    @cached_property
    def merged_content(self) -> MergedContent:
        if not self.path.exists() or self.is_new:
            return MergedContent(self.content)
        return self.get_merged_content()

    @cached_property
    def unified_diff(self) -> List[str]:
        return list(
            difflib.unified_diff(
                self.local_content.decode("utf-8").splitlines(keepends=True),
                self.merged_content.decode("utf-8").splitlines(keepends=True),
                fromfile=str(self.path),
                tofile=str(self.path),
            )
        )

    def exists(self) -> bool:
        return self.path.exists()

    def is_file(self) -> bool:
        return self.path.is_file()

    def write(self) -> bool:
        if self.is_changed or self.is_new:
            if not self.path.parent.exists():
                os.makedirs(self.path.parent)
            if self.path.exists():
                self.path.chmod(0o644)
            self.path.write_bytes(self.merged_content)
            if self.is_protected and self.is_readonly:
                self.path.chmod(0o444 | self.xmode)
            else:
                self.path.chmod(0o644 | self.xmode)
            state = {
                "content": self.content,
                "lock": self.get_hash(self.merged_content),
                "flag": self.options["flag"],
                "conflict": self.merged_content.has_conflicts,
            }
            self.state.update(state)
            return True
        return False

    @classmethod
    def get_hash(cls, data: bytes) -> str:
        return hashlib.md5(data).hexdigest()

    def get_merged_content(self) -> MergedContent:
        if self.is_optional:
            m3 = merge3.Merge3(
                self.base_content.decode("utf-8").splitlines(keepends=True),
                self.local_content.decode("utf-8").splitlines(keepends=True),
                self.content.decode("utf-8").splitlines(keepends=True),
            )
            result = MergedContent(
                "".join(
                    m3.merge_lines(
                        name_a=f"LOCAL: {self.path}",
                        name_b=f"REMOTE: {self.path}",
                        name_base=f"BASE: {self.path}",
                    )
                ).encode("utf-8")
            )
            result.has_conflicts = any(x[0] == "conflict" for x in m3.merge_regions())
            return result

        return MergedContent(self.content)


class PyFile(File):
    @classmethod
    def get_hash(cls, data: bytes) -> str:
        try:
            file = ast.unparse(ast.parse(data)).encode("utf-8")
        except SyntaxError:
            file = data
        return hashlib.md5(file).hexdigest()


class TomlFile(File):
    def get_merged_content(self) -> MergedContent:
        result = self._merge(self._load(self.base_content), self._load(self.content), self._load(self.local_content))
        return MergedContent(tomlkit.dumps(result).encode("utf-8"))

    @classmethod
    def _load(cls, data: bytes) -> Any:
        return cls._normalize_doc(tomlkit.loads(data)) if data.strip() else None

    @classmethod
    def _normalize_doc(cls, data: tomlkit.TOMLDocument) -> tomlkit.TOMLDocument:
        result = tomlkit.TOMLDocument()
        for k, v in data.items():
            result.add(k, cls._normalize_item(v))
        return result

    @classmethod
    def _normalize_item(cls, data: TomlOutOfOrderTable | TomlItem) -> TomlItem:
        if isinstance(data, (TomlTable, TomlOutOfOrderTable)):
            return cls._normalize_table(data)
        elif isinstance(data, TomlAoT):
            return cls._normalize_aot(data)
        return data

    @classmethod
    def _normalize_table(cls, data: TomlTable | TomlOutOfOrderTable) -> TomlTable:
        result = tomlkit.table()
        for k in data:
            result.add(k, cls._normalize_item(data[k]))
        result._is_super_table = all(isinstance(x, (TomlTable, TomlAoT)) for x in result.values())
        return result

    @classmethod
    def _normalize_aot(cls, data: TomlAoT) -> TomlAoT:
        result = tomlkit.aot()
        for v in data:
            result.append(cls._normalize_item(v))  # type:ignore
        return result

    @classmethod
    def _merge(cls, prev: Any, new: Any, cur: Any) -> Any:
        prev = prev if isinstance(prev, (TomlTable, tomlkit.TOMLDocument)) else {}
        cur = cur if isinstance(cur, (TomlTable, tomlkit.TOMLDocument)) else {}
        for key in new:
            if isinstance(new[key], TomlTable):
                cls._merge(prev.get(key), new[key], cur.get(key))
        for key in cur:
            if key in new or key in prev:
                continue
            new[key] = cur[key]
        if isinstance(new, TomlTable):
            new._is_super_table = all(isinstance(x, (TomlTable, TomlAoT)) for x in new.values())
        return new


FILES = {".py": PyFile, ".toml": TomlFile}

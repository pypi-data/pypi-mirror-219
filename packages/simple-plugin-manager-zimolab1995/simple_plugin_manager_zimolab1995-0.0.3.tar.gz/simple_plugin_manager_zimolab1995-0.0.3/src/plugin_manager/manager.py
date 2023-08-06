import codecs
import os.path
import shutil
import sys
import warnings
from tempfile import TemporaryDirectory
from typing import List, Dict

from code_exec.checker import StaticCodeChecker
from code_exec.executor import CodeExecutor
from dulwich import porcelain

from .exceptions import PluginNotInstalled, InvalidPlugin, PluginAlreadyInstalled
from .plugin import PluginInfo


class PluginCodeExecutor(CodeExecutor):
    def __init__(self,
                 static_checker: StaticCodeChecker | None = None,
                 whitelist: List[str] | None = None,
                 blacklist: List[str] | None = None):
        if static_checker is None:
            static_checker = StaticCodeChecker(
                no_import=False,
                no_private_attr_access=False,
                unsafe_calls=blacklist
            )
        super().__init__(
            static_checker=static_checker
        )
        self._whitelist = whitelist
        self._blacklist = blacklist

    def exec(self, source, filename, globals_=None, locals_=None, whitelist=None, blacklist=None, **compile_kwargs):
        if whitelist is None:
            whitelist = self._whitelist
        if blacklist is None:
            blacklist = self._blacklist
        return super().exec(source, filename, globals_, locals_, whitelist, blacklist, **compile_kwargs)


class PluginManager(object):
    PLUGIN_FILENAME = "__init__.py"

    def __init__(self, install_location: str, add_to_pythonpath: bool = True, executor: PluginCodeExecutor = None):
        if executor is None:
            executor = PluginCodeExecutor()

        self._executor = executor
        self._install_location = None
        self._add_to_pythonpath = add_to_pythonpath
        self._exec_globals = None
        self._cached = {}

        self.install_location = install_location

    @property
    def install_location(self):
        return self._install_location

    @property
    def executor(self):
        return self._executor

    @executor.setter
    def executor(self, exe: PluginCodeExecutor):
        if exe is None:
            exe = PluginCodeExecutor()
        self._executor = exe

    @install_location.setter
    def install_location(self, directory: str):
        old_install_dir = self._install_location
        if old_install_dir and self._add_to_pythonpath and old_install_dir in sys.path:
            sys.path.remove(old_install_dir)

        new_install_dir = self._normpath(directory)
        if not os.path.isdir(new_install_dir):
            os.makedirs(new_install_dir, exist_ok=True)
        self._install_location = new_install_dir
        if self._add_to_pythonpath:
            sys.path.append(self._install_location)

    def install(self, plugin_dir: str, encoding: str, cache: bool = True) -> PluginInfo:
        plugin_dir = self._normpath(plugin_dir)
        plugin_name = self._get_plugin_name(plugin_dir)
        if self.is_installed(plugin_name):
            raise PluginAlreadyInstalled(f"plugin named '{plugin_name}' already installed")
        plugin_file = self._normpath(os.path.join(plugin_dir, self.PLUGIN_FILENAME))
        if not os.path.isfile(plugin_file):
            raise InvalidPlugin(f"not a valid plugin: {plugin_file} not found")
        plugin_info = self._load_plugin(plugin_file, encoding)
        valid, reason = self.on_validate(plugin_info)
        if not valid:
            raise InvalidPlugin(f"{reason}")
        plugin_install_path = self._get_plugin_install_path(plugin_name)
        shutil.copytree(src=plugin_dir, dst=plugin_install_path, dirs_exist_ok=True)
        if cache:
            self._cached[plugin_name] = plugin_info
        return plugin_info

    def install_from_archive(self, archive_file: str, encoding: str, cache: bool = True) -> PluginInfo:
        with TemporaryDirectory() as temp_dir:
            plugin_dir = self._unpack_plugin_archive(archive_file=archive_file, extract_dir=temp_dir)
            return self.install(plugin_dir=plugin_dir, encoding=encoding, cache=cache)

    def install_from_git(self, git_repo: str, encoding: str, cache: bool = True) -> PluginInfo:
        with TemporaryDirectory() as temp_dir:
            plugin_dir = self._git_clone_plugin_repo(repo=git_repo, repo_dir=temp_dir)
            return self.install(plugin_dir=plugin_dir, encoding=encoding, cache=cache)

    def reinstall_from_archive(self, archive_file: str, encoding: str, cache: bool = True) -> PluginInfo:
        with TemporaryDirectory() as temp_dir:
            plugin_dir = self._unpack_plugin_archive(archive_file=archive_file, extract_dir=temp_dir)
            return self.reinstall(plugin_dir=plugin_dir, encoding=encoding, cache=cache)

    def reinstall_from_git(self, git_repo: str, encoding: str, cache: bool = True) -> PluginInfo:
        with TemporaryDirectory() as temp_dir:
            plugin_dir = self._git_clone_plugin_repo(repo=git_repo, repo_dir=temp_dir)
            return self.reinstall(plugin_dir=plugin_dir, encoding=encoding, cache=cache)

    def uninstall(self, plugin_name: str):
        if not self.is_installed(plugin_name):
            raise PluginNotInstalled(f"plugin not installed: {plugin_name}")
        plugin_dir = self._get_plugin_install_path(plugin_name)
        shutil.rmtree(
            plugin_dir, ignore_errors=True
        )
        self.remove_cache(plugin_name)

    def reinstall(self, plugin_dir: str, encoding: str, cache: bool = True) -> PluginInfo:
        plugin_dir = self._normpath(plugin_dir)
        plugin_name = self._get_plugin_name(plugin_dir)
        if self.is_installed(plugin_name):
            self.uninstall(plugin_name)
        return self.install(plugin_dir, encoding, cache)

    def update(self, plugin_dir: str, encoding: str, cache: bool = True) -> PluginInfo | None:
        plugin_dir = self._normpath(plugin_dir)
        plugin_name = self._get_plugin_name(plugin_dir)
        if not self.is_installed(plugin_name):
            raise PluginNotInstalled(f"plugin not installed: {plugin_name}")

        plugin_file = self._normpath(os.path.join(plugin_dir, self.PLUGIN_FILENAME))
        if not os.path.isfile(plugin_file):
            raise InvalidPlugin(f"not a valid plugin: {plugin_file} not found")
        new_plugin_info = self._load_plugin(plugin_file, encoding)
        valid, reason = self.on_validate(new_plugin_info)
        if not valid:
            raise InvalidPlugin(f"{reason}")

        try:
            current_plugin_info = self.get_plugin(plugin_name, encoding, no_cache=True)
            if current_plugin_info.version >= new_plugin_info.version:
                warnings.warn("no need to update")
                return None
        except BaseException as e:
            warnings.warn(f"failed to get current plugin info: {e}")
            return None

        plugin_install_path = self._get_plugin_install_path(plugin_name)
        shutil.rmtree(plugin_install_path, ignore_errors=True)
        shutil.copytree(src=plugin_dir, dst=plugin_install_path, dirs_exist_ok=True)
        self.remove_cache(plugin_name)
        if cache:
            self._cached[plugin_name] = new_plugin_info
        return new_plugin_info

    def update_from_git(self, git_repo: str, encoding: str, cache: bool = True) -> PluginInfo | None:
        with TemporaryDirectory() as temp_dir:
            plugin_dir = self._git_clone_plugin_repo(repo=git_repo, repo_dir=temp_dir)
            return self.update(plugin_dir=plugin_dir, encoding=encoding, cache=cache)

    def update_from_archive(self, archive_file: str, encoding: str, cache: bool = True) -> PluginInfo | None:
        with TemporaryDirectory() as temp_dir:
            plugin_dir = self._unpack_plugin_archive(archive_file=archive_file, extract_dir=temp_dir)
            return self.update(plugin_dir=plugin_dir, encoding=encoding, cache=cache)

    def is_installed(self, plugin_name: str) -> bool:
        return os.path.isdir(self._get_plugin_install_path(plugin_name))

    def get_plugin_names(self) -> List[str]:
        all_files = os.listdir(self.install_location)
        plugin_names = []
        for path in all_files:
            full_path = os.path.join(self.install_location, path)
            if not os.path.isdir(full_path):
                continue
            if not os.path.isfile(os.path.join(full_path, self.PLUGIN_FILENAME)):
                continue
            plugin_names.append(self._get_plugin_name(full_path))
        return plugin_names

    def get_plugins(self, encoding: str, no_cache: bool = False) -> Dict[str, PluginInfo | BaseException]:
        plugin_names = self.get_plugin_names()
        result = {}
        for plugin_name in plugin_names:
            try:
                plugin_info = self.get_plugin(plugin_name, encoding, no_cache)
                result[plugin_name] = plugin_info
            except BaseException as e:
                result[plugin_name] = e
        return result

    def get_plugin(self, plugin_name: str, encoding: str, no_cache: bool = False) -> PluginInfo:
        if not self.is_installed(plugin_name):
            raise PluginNotInstalled(f"plugin not installed: {plugin_name}")
        plugin_file = self._get_plugin_file_path(plugin_name)
        if not os.path.isfile(plugin_file):
            raise InvalidPlugin(f"'{plugin_name}' is not a valid plugin: {plugin_file} not found")

        if no_cache:
            self.remove_cache(plugin_name)

        if plugin_name in self._cached:
            return self._cached[plugin_name]
        plugin_info = self._load_plugin(plugin_file, encoding)
        if not no_cache:
            self._cached[plugin_name] = plugin_info
        return plugin_info

    def get_install_path(self, plugin_name: str) -> str:
        if not self.is_installed(plugin_name):
            raise PluginNotInstalled(f"plugin not installed: {plugin_name}")
        return self._get_plugin_install_path(plugin_name)

    def remove_cache(self, plugin_name):
        if plugin_name in self._cached:
            del self._cached[plugin_name]

    def clear_caches(self):
        self._cached.clear()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def on_validate(self, plugin_info: PluginInfo) -> (bool, str):
        """
        validate plugin_info, override this to impl your own validation logic
        """
        return True, None

    def _load_plugin(self, plugin_file: str, encoding: str) -> PluginInfo:
        try:
            source = self._readfile(plugin_file, encoding)
        except BaseException as e:
            raise e
        plugin_dir = self._normpath(os.path.dirname(plugin_file))
        plugin_name = self._get_plugin_name(plugin_dir)
        sys.path.append(plugin_dir)
        try:
            locals_ = {}
            self._executor.exec(source=source, filename=plugin_file, globals_=self._exec_globals, locals_=locals_)
            return PluginInfo.from_exec_result(plugin_name, locals_)
        except BaseException as e:
            raise InvalidPlugin(e)
        finally:
            if plugin_dir in sys.path:
                sys.path.remove(plugin_dir)

    @staticmethod
    def _get_plugin_name(path: str):
        if os.path.isfile(path):
            return path.split(".")[0]
        elif os.path.isdir(path):
            return os.path.basename(path)
        else:
            return path

    def _get_plugin_install_path(self, plugin_name: str):
        return self._normpath(os.path.join(self._install_location, plugin_name))

    def _get_plugin_file_path(self, plugin_name: str):
        return self._normpath(os.path.join(self._install_location, plugin_name, self.PLUGIN_FILENAME))

    @staticmethod
    def _readfile(filepath: str, encoding: str):
        with codecs.open(filepath, encoding=encoding) as f:
            return f.read()

    @staticmethod
    def _normpath(path: str):
        return os.path.normpath(os.path.abspath(path))

    def _unpack_plugin_archive(self, archive_file: str, extract_dir: str):
        extract_dir = self._normpath(extract_dir)
        try:
            shutil.unpack_archive(filename=archive_file, extract_dir=extract_dir)
        except BaseException as e:
            raise InvalidPlugin(f"failed to unpack plugin archive file: {e}")
        # get the plugin name from the archive file name
        plugin_name = self._get_plugin_name(archive_file)
        plugin_dir = self._normpath(os.path.join(extract_dir, plugin_name))
        if not os.path.isdir(plugin_dir):
            raise InvalidPlugin(f"invalid plugin archive file: {archive_file}")
        return plugin_dir

    def _git_clone_plugin_repo(self, repo: str, repo_dir: str):
        origin_cwd = os.getcwd()
        os.chdir(repo_dir)
        exception = None
        plugin_dir = None
        try:
            repo = porcelain.clone(source=repo)
            plugin_dir = self._normpath(repo.path)
            repo.close()
        except BaseException as e:
            exception = e
        finally:
            os.chdir(origin_cwd)
            if exception is not None:
                raise InvalidPlugin(f"failed to clone plugin repo: {exception}")
            else:
                return plugin_dir


from pathlib import Path

from rich.progress import Progress

from pycryptor.utils import hash_password, find_pattern_match
from pycryptor.file_io import EncryptIO, DecryptIO


class App:
	ENCRYPT = 0
	DECRYPT = 1

	def __init__(self, args: object) -> None:
		path_args = []
		for path in args.paths:
			matches = find_pattern_match(path)

			if not matches:
				matches = [Path(path)]

			path_args.extend(matches)
		
		self._mode = self.ENCRYPT if args.encrypt else self.DECRYPT
		self._mode_str = "encrypt" if args.encrypt else "decrypt"

		self._key = hash_password(args.key.encode())
		self._paths = path_args
		self._buffer_size = args.buffer_size


	def _display_logo(self) -> None:
		print(
			"\n\x1b[96m"
			" ╔═════════════════════════════════════════════════════════╗\n"
			" ║      ____        ______                 __              ║\n"
			" ║     / __ \__  __/ ____/______  ______  / /_____  _____  ║\n"
			" ║    / /_/ / / / / /   / ___/ / / / __ \/ __/ __ \/ ___/  ║\n"
			" ║   / ____/ /_/ / /___/ /  / /_/ / /_/ / /_/ /_/ / /      ║\n"
			" ║  /_/    \__, /\____/_/   \__, / .___/\__/\____/_/       ║\n"
			" ║        /____/           /____/_/                        ║\n"
			" ║                                                         ║\n"
			" ╚═════════════════════════════════════════════════════════╝"
			"\x1b[0m\n"
		)

	def _display_params(self) -> None:
		print(
			f" operation mode : {self._mode_str}\n"
			f" total files    : {len(self._paths)} files\n"
			f" buffer size    : {self._buffer_size}\n"
		)

	def _file_task(self, progress: Progress, file_path: Path) -> None:
		if self._mode == self.ENCRYPT:
			crypt_file = EncryptIO(self._key, file_path, self._buffer_size)
		else:
			crypt_file = DecryptIO(self._key, file_path, self._buffer_size)

		task = progress.add_task(
			f" {file_path.name}",
			total=crypt_file.size
		)

		while not crypt_file.finished:
			advance_size = crypt_file.handle_buffer()
			progress.update(task, advance=advance_size)
		
		crypt_file.close()

	def run(self) -> None:
		self._display_logo()
		self._display_params()

		with Progress() as progress:
			for path in self._paths:
				self._file_task(progress, path)
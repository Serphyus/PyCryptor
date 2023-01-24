import argparse

from pycryptor.app import App

from Crypto.Cipher import AES


def main() -> None:
	parser = argparse.ArgumentParser(description="cli tool for encrypting and decrypting files")

	parser.add_argument("paths", nargs="*", help="filepaths to encrypt/decrypt")
	parser.add_argument("-e", "--encrypt", action="store_true", help="encrypt mode")
	parser.add_argument("-d", "--decrypt", action="store_true", help="decrypt mode")
	parser.add_argument("-k", "--key", action="store", help="password to use for encrypting/decrypting")
	parser.add_argument("-b", "--buffer_size", action="store", type=int, default=4096, help="buffer size which must be a product of 16")

	args = parser.parse_args()

	if args.encrypt and args.decrypt:
		parser.error("too many modes selected")
	
	if args.key is None:
		parser.error("missing key argument when decrypting")

	if (args.buffer_size % AES.block_size):
		parser.error(f"buffer_size must be a product of {AES.block_size}")

	app = App(args)

	try:
		app.run()
	except Exception as e:
		print(f"\n\n \x1b[91m[!]\x1b[0m {e}\n")


if __name__ == "__main__":
	main()
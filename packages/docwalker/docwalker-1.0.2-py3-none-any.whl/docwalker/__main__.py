from docwalker.app import ViewerApp
from docwalker.cli import PARSER, generate_config


def main():
    args = PARSER.parse_args()
    config = generate_config(f"{args.dir}/{args.file}" if args.file else ".dwconf")
    app = ViewerApp(args.dir, config)
    app.run()


if __name__ == "__main__":
    main()

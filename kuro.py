import argparse

def print_banner():
    with open("banner.txt") as f:
        print(f.read())

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Kuro — Your Terminal AI Agent"
)
    subparsers = parser.add_subparsers(dest="command")
    
    summarize_parser=subparsers.add_parser("summarize", help="Summarize a file")
    summarize_parser.add_argument("file", help="Path to file to summarize")
    subparsers.add_parser("commit", help="Make a Git commit")
    subparsers.add_parser("ask", help="Ask a question")
    subparsers.add_parser("exit", help="Exit the program")
    args = parser.parse_args()

    if args.command == "summarize":
        print("📄 You chose to summarize a file")
        try:
            with open(args.file, 'r') as f:
                lines=f.readlines()
                print("\n Summary: \n")
                print("".join(lines[:5]))
        except FileNotFoundError:
                print("File not found, please check the path.")
        # You'll later call your summarize function here

    elif args.command == "commit":
        print("💾 You chose to commit with Git")
        # Git automation goes here

    elif args.command == "ask":
        print("🤖 You asked me something")
        # AI question logic goes here

    elif args.command == "exit":
        print("👋 Goodbye!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

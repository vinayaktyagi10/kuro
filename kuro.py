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
    commit_parser=subparsers.add_parser("commit", help="Make a Git commit")
    commit_parser.add_argument("message", help="Make a git comment")
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
        import subprocess
        
# checking git repo first and then proceed to add,commit and push.
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("X not a Git Repo. Use 'git init' first.")

        print("Commiting...")
        try:
            subprocess.run(["git", "add", "."],check=True)
            subprocess.run(["git", "commit", "-m", args.message],check=True) 
            subprocess.run(["git", "push"],check=True)
            print("Changes pushed successfully! :)")
        except suprocess.CalledProcessError as e:
            print("Git operation failed..", e)

    elif args.command == "ask":
        print("🤖 You asked me something")
        # AI question logic goes here

    elif args.command == "exit":
        print("👋 Goodbye!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

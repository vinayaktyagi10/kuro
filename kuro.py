#!/usr/bin/env python3

import argparse
import subprocess
import os
from mistral_agent import ask_mistral 
from mistral_agent import load_history

BASE_DIR= "/home/ricing/kuro"

def print_banner():
    banner_path=os.path.join(BASE_DIR, "banner.txt")
    with open(banner_path) as f:
        print(f.read())

def get_git_diff():
    try:
        result=subprocess.run(["git", "diff", "--staged"],
                              capture_output=True,
                              text=True,
                              check=True,
                              )
        diff=result.stdout.strip()

        if not diff:
                result=subprocess.run(
                ["git", "diff"],
                capture_output=True,
                text=True,
                check=True,
                )
                diff=result.stdout.strip()
        return diff
    except subprocess.CalledProcessError:
        return None

def generate_commit(diff):
    prompt=(
        "You are a helpful AI that generates concise, clear, "
        "and conventional Git commit messages, try to keep the subject line <=72 based on the following git diff: \n\n" f"{diff}\n\nCommit message:"
    )
    response, _=ask_mistral(prompt, history=[])
    return response.strip()

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Kuro — Your Terminal AI Agent"
)
    subparsers = parser.add_subparsers(dest="command")
    
    chat_parser=subparsers.add_parser("chat", help="Enter AI chat mode")

    commit_parser=subparsers.add_parser("commit", help="Make a Git commit")
    commit_parser.add_argument("message", nargs="?", help="Make a git comment")
    commit_parser.add_argument("--ai", action="store_true", help="Generate commit message using AI from git diff")

    subparsers.add_parser("exit", help="Exit the program")

    args = parser.parse_args()
    loaded_file=None
    loaded_path=None

    if args.command=="chat":
        print("Entering AI chat. Type 'exit' to leave. \n")


        history=load_history()

        while True:
            try:
                user_input=input("You > ").strip()
                if user_input.lower() == "exit":
                        print("Exiting chat, goodbye!")
                        break
                elif user_input.startswith("/load "):
                        path=user_input[len("/load "):].strip()
                        try:
                            with open(path, 'r') as f:
                                loaded_file=f.read()
                                loaded_path=path
                            print(f"File `{path}` loaded into session memory.")
                        except FileNotFoundError:
                            print(f"File not found.")
                        continue
    
                elif user_input=="/unload":
                    loaded_file=None
                    loaded_path=None
                    print("File context cleared.")
                    continue

                elif user_input=="/show":
                        if loaded_file:
                            print(f"\n Currently loaded: `{loaded_path}`\n\n{loadedfile}\n")
                        else:
                            print("No file loaded.")
                        continue
                
                if loaded_path:
                        print(f"File context active: {loaded_path}")
                if loaded_file:
                    user_input = (
                        f"You are an AI assistant working with the file `{loaded_path}`.\n\n"
                        f"--- FILE CONTENT START ---\n{loaded_file}\n--- FILE CONTENT END ---\n\n"
                        f"Now, answer the following based on the above file:\n{user_input}"
                    )
                response, history=ask_mistral(user_input, history)
                print(f"\n Kuro > {response}\n")
            except KeyboardInterrupt:
                print("\n Exiting chat")
                break
    



    elif args.command == "commit":
        print("💾 You chose to commit with Git")
        
# checking git repo first and then proceed to add,commit and push.
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("X not a Git Repo. Use 'git init' first.")
            return

        if args.command == "commit":
    # Check if inside a Git repo
           try:
                subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.DEVNULL)
           except subprocess.CalledProcessError:
             print("X Not a Git repository. Use 'git init' first.")
             return

           if args.ai:
             print("Generating commit message with AI...")
             diff = get_git_diff()
             if not diff:
                print("⚠️ No changes detected to commit.")
                return

             commit_msg = generate_commit(diff)
             print(f"AI Commit Message:\n{commit_msg}\n")

             confirm = input("Commit with this message? (y/n): ").strip().lower()
             if confirm != "y":
                print("Commit aborted.")
                return

           else:
                if not args.message:
                    print("X Please provide a commit message or use --ai to generate one.")
                    return
                commit_msg = args.message

    # Proceed to git add, commit, push
           try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", commit_msg], check=True)
                subprocess.run(["git", "push"], check=True)
                print("Changes pushed successfully!")
           except subprocess.CalledProcessError as e:
                print("Git operation failed:", e)



    elif args.command == "exit":
        print("👋 Goodbye!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

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

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Kuro — Your Terminal AI Agent"
)
    subparsers = parser.add_subparsers(dest="command")
    
    chat_parser=subparsers.add_parser("chat", help="Enter AI chat mode")

    commit_parser=subparsers.add_parser("commit", help="Make a Git commit")
    commit_parser.add_argument("message", help="Make a git comment")

    subparsers.add_parser("exit", help="Exit the program")

    args = parser.parse_args()

    if args.command=="chat":
        print("Entering AI chat. Type 'exit' to leave. \n")


        history=load_history()

        while True:
            try:
                user_input=input("You > ").strip()
                if user_input.lower() in ['exit']:
                        print("Exiting chat, goodbye!")
                        break
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

        print("Commiting...")
        try:
            subprocess.run(["git", "add", "."],check=True)
            subprocess.run(["git", "commit", "-m", args.message],check=True) 
            subprocess.run(["git", "push"],check=True)
            print("Changes pushed successfully! :)")
        except subprocess.CalledProcessError as e:
            print("Git operation failed..", e)



    elif args.command == "exit":
        print("👋 Goodbye!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

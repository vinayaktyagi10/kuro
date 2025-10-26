#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys
from mistral_agent import ask_mistral
from mistral_agent import load_history

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def print_banner():
    banner_path = os.path.join(BASE_DIR, "banner.txt")
    try:
        with open(banner_path) as f:
            print(f.read())
    except FileNotFoundError:
        print("🖤 Kuro - Your Terminal AI Assistant")


def check_git_repo():
    """Check if current directory is a git repository"""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_git_status():
    """Get current git status"""
    try:
        result = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_git_diff(staged=True):
    """Get git diff with better error handling"""
    try:
        cmd = ["git", "diff"]
        if staged:
            cmd.append("--staged")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        diff = result.stdout.strip()

        # If staged is empty, try unstaged
        if staged and not diff:
            result = subprocess.run(
                ["git", "diff"], capture_output=True, text=True, check=True
            )
            diff = result.stdout.strip()

        return diff
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting git diff: {e}")
        return None


def generate_commit_message(diff, message_type="conventional"):
    """Generate commit message with improved prompt"""

    if message_type == "conventional":
        prompt = (
            "You are a Git commit message expert. Generate a clear, conventional commit message "
            "following these rules:\n"
            "1. Use conventional commit format: type(scope): subject\n"
            "2. Types: feat, fix, docs, style, refactor, test, chore\n"
            "3. Keep subject line under 72 characters\n"
            "4. Use imperative mood (e.g., 'add' not 'added')\n"
            "5. Don't end subject with period\n"
            "6. Optionally add a body if changes are complex\n\n"
            f"Based on this diff, generate ONLY the commit message:\n\n{diff}\n\n"
            "Commit message:"
        )
    elif message_type == "detailed":
        prompt = (
            "You are a Git commit message expert. Generate a detailed commit message "
            "with both subject and body:\n"
            "1. Subject line under 72 characters\n"
            "2. Blank line\n"
            "3. Body explaining what and why (not how)\n"
            "4. Use conventional commit format\n\n"
            f"Based on this diff:\n\n{diff}\n\n"
            "Commit message:"
        )
    else:  # simple
        prompt = (
            "Generate a concise, clear Git commit message (under 72 characters) "
            f"for these changes:\n\n{diff}\n\n"
            "Commit message:"
        )

    response, _ = ask_mistral(prompt, history=[])
    return response.strip()


def preview_commit():
    """Show what will be committed"""
    status = get_git_status()
    if status:
        print("\n📋 Changes to be committed:")
        print(status)
    else:
        print("\n⚠️  No changes detected")
        return False
    return True


def handle_commit(args):
    """Handle git commit with enhanced features"""

    # Check if in git repo
    if not check_git_repo():
        print("❌ Not a Git repository. Use 'git init' first.")
        return

    # Show what will be committed
    if not preview_commit():
        return

    commit_msg = None

    # AI-generated commit message
    if args.ai:
        print("\n🤖 Generating commit message with AI...")

        # Get diff
        diff = get_git_diff(staged=False)
        if not diff:
            print("⚠️  No changes detected to commit.")
            return

        # Determine message type
        msg_type = "conventional"
        if hasattr(args, "detailed") and args.detailed:
            msg_type = "detailed"
        elif hasattr(args, "simple") and args.simple:
            msg_type = "simple"

        # Generate message
        commit_msg = generate_commit_message(diff, msg_type)
        print(f"\n💡 AI Generated Commit Message:")
        print("─" * 50)
        print(commit_msg)
        print("─" * 50)

        # Confirm with user
        confirm = input("\n✓ Use this message? (y/n/e to edit): ").strip().lower()

        if confirm == "e":
            print("\n✏️  Enter your commit message:")
            commit_msg = input().strip()
        elif confirm != "y":
            print("❌ Commit aborted.")
            return

    # Manual commit message
    else:
        if not args.message:
            print("❌ Please provide a commit message or use --ai to generate one.")
            print("   Example: kuro commit 'your message' or kuro commit --ai")
            return
        commit_msg = args.message

    # Stage all changes if --add or -a flag
    if hasattr(args, "add") and args.add:
        try:
            print("\n📦 Staging all changes...")
            subprocess.run(["git", "add", "."], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to stage changes: {e}")
            return

    # Commit
    try:
        print(f"\n💾 Committing...")
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        print("✓ Committed successfully!")

        # Push if --push or -p flag
        if hasattr(args, "push") and args.push:
            print("\n🚀 Pushing to remote...")
            result = subprocess.run(["git", "push"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Pushed successfully!")
            else:
                print(f"⚠️  Push failed: {result.stderr}")
                print("   Try: git push")
        else:
            print("\n💡 Tip: Use --push or -p to automatically push after commit")

    except subprocess.CalledProcessError as e:
        print(f"❌ Commit failed: {e}")


def handle_chat(args):
    """Handle chat mode with enhanced features"""
    print("💬 Entering AI chat mode. Type 'exit' to leave.\n")
    print("Commands:")
    print("  /load <file>  - Load a file into context")
    print("  /unload       - Clear file context")
    print("  /show         - Show loaded file")
    print("  /clear        - Clear chat history")
    print("  exit          - Exit chat mode\n")

    history = load_history()
    loaded_file = None
    loaded_path = None

    while True:
        try:
            user_input = input("You > ").strip()

            if user_input.lower() == "exit":
                print("👋 Exiting chat, goodbye!")
                break

            elif user_input.startswith("/load "):
                path = user_input[len("/load ") :].strip()
                try:
                    with open(path, "r") as f:
                        loaded_file = f.read()
                        loaded_path = path
                    print(f"✓ File `{path}` loaded into session memory.")
                except FileNotFoundError:
                    print(f"❌ File not found: {path}")
                except Exception as e:
                    print(f"❌ Error loading file: {e}")
                continue

            elif user_input == "/unload":
                loaded_file = None
                loaded_path = None
                print("✓ File context cleared.")
                continue

            elif user_input == "/show":
                if loaded_file:
                    print(f"\n📄 Currently loaded: `{loaded_path}`")
                    print("─" * 50)
                    print(loaded_file[:500])  # Show first 500 chars
                    if len(loaded_file) > 500:
                        print(f"\n... ({len(loaded_file) - 500} more characters)")
                    print("─" * 50)
                else:
                    print("⚠️  No file loaded.")
                continue

            elif user_input == "/clear":
                history = []
                print("✓ Chat history cleared.")
                continue

            # Show context indicator
            if loaded_path:
                print(f"📎 Context: {loaded_path}")

            # Add file context to prompt
            if loaded_file:
                user_input = (
                    f"You are an AI assistant working with the file `{loaded_path}`.\n\n"
                    f"--- FILE CONTENT START ---\n{loaded_file}\n--- FILE CONTENT END ---\n\n"
                    f"Now, answer the following based on the above file:\n{user_input}"
                )

            response, history = ask_mistral(user_input, history)
            print(f"\nKuro > {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Exiting chat")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="🖤 Kuro — Your Terminal AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Enter AI chat mode")

    # Commit command with enhanced options
    commit_parser = subparsers.add_parser(
        "commit", help="Make a Git commit with optional AI assistance"
    )
    commit_parser.add_argument(
        "message", nargs="?", help="Commit message (optional if using --ai)"
    )
    commit_parser.add_argument(
        "--ai", action="store_true", help="Generate commit message using AI"
    )
    commit_parser.add_argument(
        "--detailed",
        action="store_true",
        help="Generate detailed commit message with body (use with --ai)",
    )
    commit_parser.add_argument(
        "--simple",
        action="store_true",
        help="Generate simple commit message (use with --ai)",
    )
    commit_parser.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Stage all changes before committing (git add .)",
    )
    commit_parser.add_argument(
        "-p", "--push", action="store_true", help="Push to remote after committing"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status", help="Show git status with AI summary"
    )
    status_parser.add_argument(
        "--ai", action="store_true", help="Get AI summary of changes"
    )

    args = parser.parse_args()

    if args.command == "chat":
        handle_chat(args)

    elif args.command == "commit":
        handle_commit(args)

    elif args.command == "status":
        if not check_git_repo():
            print("❌ Not a Git repository.")
            return

        status = get_git_status()
        if status:
            print("\n📋 Git Status:")
            print(status)

            if args.ai:
                diff = get_git_diff(staged=False)
                if diff:
                    print("\n🤖 AI Summary:")
                    prompt = f"Summarize these git changes in 2-3 sentences:\n\n{diff}"
                    summary, _ = ask_mistral(prompt, history=[])
                    print(summary)
        else:
            print("✓ Working tree clean")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

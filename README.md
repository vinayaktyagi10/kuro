# 🧠 Kuro — Your Terminal AI Assistant

Kuro is a minimalist yet powerful terminal-based AI assistant built with Python, powered by [Mistral](https://mistral.ai/) running locally via [Ollama](https://ollama.com/). It's designed to be extendable, smart, and just the right kind of helpful.

![screenshot](https://your-screenshot-url-if-any)

---

## ✨ Features

- 💬 **Chat with Kuro** — Natural AI conversations directly from your terminal.
- 🧠 **Local LLM Powered** — Uses Mistral running via Ollama for fast, private AI responses.
- 🧾 **Contextual Memory** — Temporarily load a file into memory during a session for context-aware replies.
- 📁 **Git Integration** — Commit, add, and push code with Kuro in one command.
- 🗃️ **Chat History** — Optionally stores chat history across sessions in `~/.kuro_history.json`.
- ⚙️ **Extensible Architecture** — Add your own commands and AI abilities easily.

---

## 🛠️ Installation

Make sure you have:

- Python 3.8+
- [`ollama`](https://ollama.com) installed and running locally with the `mistral` model:

```bash
ollama run mistral```

Then:

```git clone https://github.com/your-username/kuro.git
cd kuro
pip install -r requirements.txt
chmod +x kuro.py
ln -s $(pwd)/kuro.py ~/.local/bin/kuro```

Now just type kuro from anywhere in your terminal!

---

## 🚀 Usage

### General Command Format:

```kuro [command] [options]```

### 💬Chat Mode:

```kuro chat```

- Talk to Kuro

- Load a file with /load /path/to/file

- Show or clear context with /show or /unload

- Exit any time with exit

### 🔧 Git Commit Mode

```kuro commit "your commit message"```

- Automatically stages, commits, and pushes

- Use --ai to generate commit message from git diff (optional feature)

---

## 🧩 Planned Features

- /explain, /doc, /refactor — Code intelligence commands

- /todo, /calendar, /weather — Personal assistant extensions

- Multi-file context memory

- Project summary mode

---

## License

MIT License

---

## 🤝 Contributing

Contributions are welcome! File an issue or open a pull request with your ideas, improvements, or features.

---

## 💬 Acknowledgments

- Ollama for effortless local LLM hosting

- Mistral for their blazing-fast open models

- Inspired by a love for clean CLI workflows and functional AI tools


🖤 Kuro isn't meant to replace your tools. It's meant to understand them.

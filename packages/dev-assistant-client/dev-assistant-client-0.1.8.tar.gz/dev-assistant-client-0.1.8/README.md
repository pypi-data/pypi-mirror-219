# Dev Assistant

Welcome to the [Dev Assistant](https://devassistant.tonet.dev) plugin for ChatGPT.

## What is it?

[Dev Assistant](https://devassistant.tonet.dev) is a plugin for ChatGPT that assists us developers by executing tasks directly on our devices.

Dev Assistant Client (this repo) is a Python package that is basically the core component of the project. It receives instructions from ChatGPT via Dev Assistant plugin, executes it on any of your devices and send the response back.

## Features

The Dev Assistant Local Client is designed to streamline your development process by offering a range of functionalities:

- **File Management**: Create, read, update, and delete files. List the contents of a directory. You can manage your files without leaving your conversation with ChatGPT.

- **Git Version Control**: Initialize a Git repository, add changes to the staging area, commit changes, and push changes to a remote repository. Get the status of the Git repository. You can manage your Git repositories directly through ChatGPT.

- **Terminal Commands Execution**: Execute commands directly in the terminal. You can run any command in your terminal directly from ChatGPT.

## Requirements

- 👌🏼 Python 3.6+
- 👌🏼 pip
- 💸 ChatGPT Plus subscription _(for plugins store access)_

## Installation

- Create a Dev Assistant account at [devassistant.tonet.dev](https://devassistant.tonet.dev)
- Generate a token at [devassistant.tonet.dev/token](https://devassistant.tonet.dev/token) for ChatGPT and save it. You'll need it later.
- Install the local client:
  - [Install Python](https://www.python.org/downloads/)
  - [Install pip](https://pip.pypa.io/en/stable/installing/)
  - Run `pip install dev-assistant-client` in your terminal
  - You will be prompted to enter your email and password. Enter the credentials you used to create your Dev Assistant account.
  - If everything went well, you should see a message saying "Successfully logged in!" and the client will be listening for instructions from ChatGPT.
- Install the ChatGPT plugin:
  - On the [ChatGPT Plugins Store](https://chat.openai.com/plugins), click in the **"Install an unverified plugin"** at bottom of Plugin store dialog window, paste the <https://devassistant.tonet.dev> and click on "Find plugin".
  - ChatGPT will ask you to enter your credentials. Insert the token generated in the previous step and click "Install plugin".
  - Enable the plugin in the list of installed plugins and you're good to go!
 
## Usage

Once installed, you can use the `dev-assistant` command in your terminal to start the client.

If you're not already logged in, you'll be prompted to enter your email and password. Once authenticated, the client will automatically establish a connection with the server.

You can now ask ChatGPT to execute commands on your device. For example, you can ask ChatGPT to create a new file, add changes to a Git repository, or run a command in the terminal.

You can do `CRTL+C` to stop the client at any time.

To log out, use:

```bash
dev-assistant logout
```

This command will remove your saved authentication token, ensuring your security.

## Contributing

We welcome contributions! If you have an idea for an improvement or have found a bug, please open an issue. Feel free to fork the repository and submit a pull request if you'd like to contribute code. Please follow the code style and conventions used in the existing codebase.

## License

The Dev Assistant Local Client is open-source software, licensed under the [MIT license](LICENSE).

## Support

If you encounter any problems or have any questions, don't hesitate to open an issue on GitHub. We're here to help!

## Acknowledgements

A big thank you to all contributors and users for your support! We couldn't do it without you.

## Authors

- [Luciano T.](https://github.com/lucianotonet)
- [ChatGPT](https://chat.openai.com/)
- [GitHub Copilot](https://copilot.github.com/)
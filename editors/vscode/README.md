# Ooju VS Code Support

This folder contains a local VS Code extension for Ooju syntax highlighting.

## What It Adds
- `.oj` file recognition
- Syntax highlighting for keywords, variables, strings, numbers, operators, punctuation, and comments
- `//` line comments
- Bracket and quote auto-closing

## Install Locally
1. Open VS Code.
2. Open the `editors/vscode` folder as a workspace.
3. Press `F5` and choose `Run Ooju Extension`.
4. In the new Extension Development Host window, open any `.oj` file.

## Install As A VSIX
1. From `editors/vscode`, run `npm install`.
2. Run `npm run package`.
3. In VS Code, open the Extensions view.
4. Click the `...` menu in the top-right of the Extensions panel.
5. Choose `Install from VSIX...` and select the generated `.vsix` file.

## Develop Locally
1. Open the `editors/vscode` folder in VS Code.
2. Press `F5` to launch an Extension Development Host.
3. Open any `.oj` file in the new window.

The grammar file is in `syntaxes/ooju.tmLanguage.json`.

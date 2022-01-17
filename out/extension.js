"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
//@ts-ignore LanguageClientOptions以外見つからないと言われるのでしゃーなし
const vscode_languageclient_1 = require("vscode-languageclient");
const path = require("path");
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "corgi_ide" is now active!');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('corgi_ide.helloWorld', () => {
        // The code you place here will be executed every time your command is executed
        // Display a message box to the user
        vscode.window.showInformationMessage('Hello World from corgi_ide!');
    });
    context.subscriptions.push(disposable);
    let serverPath = context.asAbsolutePath(path.join("server", "server.py"));
    console.log(`@@[${serverPath}]`);
    let serverOptions = {
        command: "python",
        args: [serverPath],
    };
    // 多田さんも言っていた plaintext
    let clientOptions = {
        documentSelector: [
            // { scheme: "file", language: "plaintext" },
            { scheme: "file", language: "python" },
        ],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher("**/.clientrc"),
        }
    };
    // Start language server and client.
    let client = new vscode_languageclient_1.LanguageClient("corgi-with-ide", "Language Server in Python", serverOptions, clientOptions);
    client.start();
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
/*
"use strict";

import * as path from "path";
import { ExtensionContext, window as Window } from "vscode";
import { LanguageClient, LanguageClientOptions, RevealOutputChannelOn, ServerOptions, TransportKind } from "vscode-languageclient";

// 拡張機能を立ち上げたときに呼び出す関数
export function activate(context: ExtensionContext): void {
  const serverModule = context.asAbsolutePath(path.join("server", "out", "server.js"));
  const debugOptions = { execArgv: ["--nolazy", "--inspect=6009"], cwd: process.cwd() };
  const serverOptions: ServerOptions = {
    run: { module: serverModule, transport: TransportKind.ipc, options: { cwd: process.cwd() } },
    debug: {
      module: serverModule,
      transport: TransportKind.ipc,
      options: debugOptions,
    },
  };
  // 対象とする言語．今回は.txtファイルと.mdファイル
  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      {
        scheme: "file",
        language: "plaintext",
      },
      {
        scheme: "file",
        language: "markdown",
      }],
    diagnosticCollectionName: "sample",
    revealOutputChannelOn: RevealOutputChannelOn.Never,
  };

  let client: LanguageClient;
  try {
    client = new LanguageClient("Sample LSP Server", serverOptions, clientOptions);
  } catch (err) {
    Window.showErrorMessage("The extension couldn't be started. See the output channel for details.");
    return;
  }
  client.registerProposedFeatures();

  context.subscriptions.push(
    client.start(),
  );
}
*/
//# sourceMappingURL=extension.js.map
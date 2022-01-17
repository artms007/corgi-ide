# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import logging

# from modules import modules_dl
# modules_dl()

from find import find_ZENKAKU_and_IMPORT
from corgi import generate_nmt, compose_nmt

from pyls_jsonrpc.dispatchers import MethodDispatcher
from pyls_jsonrpc.endpoint import Endpoint
from pyls_jsonrpc.streams import JsonRpcStreamReader, JsonRpcStreamWriter

IS_KANJI = re.compile(r'[一-龥]+')
IS_ZENKAKU = re.compile(r'[ぁ-んァ-ン一-龥]+')

# タイムログ用
from slackweb import Slack
HOST = 'slack.com'
ID = 'T02R283SH6G'
ID2 = 'B02RPMMGEQ0'
ID3 = 'YckxhYuVcf8bKY8QfzNuk5Mt'
WEB_HOOK_URL = f'https://hooks.{HOST}/services/{ID}/{ID2}/{ID3}'
slack = Slack(WEB_HOOK_URL)

# ログ出力
logging.basicConfig(
  handlers = [
    logging.FileHandler(
      filename = f"{os.path.expanduser('~/Desktop')}/corgi.log",
      encoding='utf-8',
      mode='a+'
    )
  ],
  level = logging.DEBUG,
  format = "%(relativeCreated)08d[ms] - %(name)s - %(levelname)s - %(processName)-10s - %(threadName)s -\n*** %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
log = logging.getLogger("pyls_jsonrpc")
log.addHandler(console)


class SampleLanguageServer(MethodDispatcher):
  def __init__(self):
    self.jsonrpc_stream_reader = JsonRpcStreamReader(sys.stdin.buffer)
    self.jsonrpc_stream_writer = JsonRpcStreamWriter(sys.stdout.buffer)
    self.endpoint = Endpoint(self, self.jsonrpc_stream_writer.write)
    self.lastDocument = ''

  def start(self):
    self.jsonrpc_stream_reader.listen(self.endpoint.consume)

  def do_corgi(self, text):
    nmt = compose_nmt(generate_nmt())
    return nmt(text, beams=3)

  # クライアントからサーバに 'method': 'initialize' が渡った時に実行されるメソッド
  def m_initialize(self, rootUri=None, **kwargs):
    # ここの設定でどのタイミングで通信するか等を決めるっぽい
    return {"capabilities": {
      'codeActionProvider': True,
      # 'codeLensProvider': {
      #   'resolveProvider': False,  # We may need to make this configurable
      # },
      'completionProvider': {
        'resolveProvider': False,  # We know everything ahead of time
        # 'triggerCharacters': r'[ぁ-んァ-ン一-龥]+'
        'triggerCharacters': ['.', '#']
      },
      'documentFormattingProvider': True,
      # 'documentHighlightProvider': True,
      # 'documentRangeFormattingProvider': True,
      # 'documentSymbolProvider': True,
      # 'definitionProvider': True,
      # 'hoverProvider': True,
      # 'referencesProvider': True,
      # 'renameProvider': True,
      # 'foldingRangeProvider': True,
      # 'signatureHelpProvider': {
      #   'triggerCharacters': ['(', ',', '=']
      # },
      'textDocumentSync': {
        # 0 : NONE
        # 1 : FULL 毎回ファイルの中身を全部送る
        # 2 : INCREMENTAL 差分だけ
        'change': 1,
        'save': {
          'includeText': True,
        },
        'openClose': True,
      },
      'workspace': {
        'workspaceFolders': {
          'supported': True,
          'changeNotifications': True
        }
      }
    }}

  # クライアントからサーバに 'method': 'textDocument/didClose' が渡った時に実行されるメソッド
  def m_text_document__did_close(self, textDocument=None, **_kwargs):
    pass

  # クライアントからサーバに 'method': 'textDocument/didOpen' が渡った時に実行されるメソッド
  # 適当に0行0文字目から5行5文字目までの文字をWARNING扱い（指定範囲が存在しなくてもエラーにはならない）
  def m_text_document__did_open(self, textDocument=None, **_kwargs):
    self.lastDocument = textDocument['text']
    self.endpoint.notify("textDocument/publishDiagnostics", params={'uri':textDocument['uri'], 'diagnostics': []})
    # self.endpoint.notify("textDocument/publishDiagnostics",params={'uri':textDocument['uri'], 'diagnostics': [{
    #   'source': 'vscpylspext',
    #   'range': {'start':{'line':0, 'character':0}, 'end':{'line':5, 'character':5}},
    #   'message':'エラーだよ',
    #   'severity': 2,  # 1~4
    #   'code': ''
    # }]})

  # クライアントからサーバに 'method': 'textDocument/didChange' が渡った時に実行されるメソッド
  # 漢字部分をINFORMATION扱い
  def m_text_document__did_change(self, contentChanges=None, textDocument=None, **_kwargs):
    doc = contentChanges[0]['text']
    self.lastDocument = doc
    lines = doc.split('\n')
    modules = []
    variable = []
    diagnostics = []

    for i,line in enumerate(lines):       
      d = find_ZENKAKU_and_IMPORT(i, line, variable, modules)
      if d:
        diagnostics.extend(d)

    self.endpoint.notify("textDocument/publishDiagnostics",params={'uri':textDocument['uri'], 'diagnostics': diagnostics})


  # クライアントからサーバに 'method': 'textDocument/didSave' が渡った時に実行されるメソッド
  # 空の通知を送れば全エラーが消える？
  def m_text_document__did_save(self, textDocument=None, **_kwargs):
    self.endpoint.notify("textDocument/publishDiagnostics",params={'uri':textDocument['uri'], 'diagnostics': []})


  def m_text_document__code_action(self, textDocument=None, range=None, context=None, **_kwargs):
    code_actions = []
    changes1, changes2, changes3 = [], [], []
    # pattern = ''

    for diag in context['diagnostics']:
      if diag['source'] == 'corgi-ide':
        where = diag['range']
        text = '# option ' + diag['data']

        # タイムログ用
        start_time = time.time()

        comps = self.do_corgi(text)
        
        changes1.append({
          'range': where,
          # 'newText': text
          # 'newText': 'sep=","'
          'newText': comps[0][0]
        }) 
        changes2.append({
          'range': where,
          'newText': comps[0][1]
        }) 
        changes3.append({
          'range': where,
          'newText': comps[0][2]
        })                 

    if len(changes3) > 0:
      code_actions.append({
        'title': comps[0][0],
        'kind': 'quickfix',
        'diagnostics': [diag],
        # 'isPreferred': True,
        'edit': {
          'changes': {
            textDocument['uri'] : changes1
          }
        }
      })  
      code_actions.append({
        'title': comps[0][1],
        'kind': 'quickfix',
        'diagnostics': [diag],
        # 'isPreferred': True,
        'edit': {
          'changes': {
            textDocument['uri'] : changes2
          }
        }
      }) 
      code_actions.append({
        'title': comps[0][1],
        'kind': 'quickfix',
        'diagnostics': [diag],
        # 'isPreferred': True,
        'edit': {
          'changes': {
            textDocument['uri'] : changes3
          }
        }
      }) 

      # タイムログ用
      elapsed_time = time.time() - start_time
      slack.notify(text=elapsed_time)   
        
      return code_actions


  def m_text_document__completion(self, textDocument=None, position=None, **_kwargs):
    # for diag in context['diagnostics']:
    #   if diag['source'] == 'corgi-ide':
    #     text = 'カンマ区切り'
    completion = {
      'isIncomplete': True,
      'items': [{
        'label': "カンマ区切り",
        'insertText': 'sep = ","'
      },{
        'label': "aを入力します"
      }]
    }
    return completion

  # ドキュメントのフォーマット実行時に呼ばれる
  def m_text_document__formatting(self, textDocument=None, _options=None, **_kwargs):
    return [{
      'range': {
        'start': {'line': 0, 'character': 0},
        'end': {'line': len(self.lastDocument.split('\n')), 'character': 0}
      },
      'newText': IS_ZENKAKU.sub('XX', self.lastDocument)
    }]


if __name__ == "__main__":
  ls = SampleLanguageServer()
  ls.start()


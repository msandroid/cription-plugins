# Cription plugins for Cursor, Claude, Codex and Antigravity

On-device transcription and your Cription notes, available to AI coding agents and assistants through **plugins** and **skills**. The MCP server lives in [msandroid/cription-mcp](https://github.com/msandroid/cription-mcp).

- 🎙️ **Transcribe** local audio and video files with Apple's on-device SpeechAnalyzer (the engine Cription uses for its best-scoring languages, e.g. Japanese).
- 📝 **Summarize** transcripts into minutes, interview findings, lecture notes or sales-call summaries with Cription's templates.
- 🔎 **Search and read** the notes you recorded with the Cription Mac app (read-only).
- 🔒 **On-device recognition**: audio is processed on your Mac. Tool results are returned to your AI client.

**Release: [v0.4.0](https://github.com/msandroid/cription-plugins/releases/tag/v0.4.0)** · MCP server pinned to **v0.3.1**. [日本語の詳しい導入手順](https://github.com/msandroid/cription-mcp/blob/v0.3.1/docs/INSTALL.ja.md) · [日本語概要](#日本語)

## Notion and Manus

Notion page export and authenticated HTTPS MCP for Manus / Notion Custom Agents are available in [Cription MCP v0.4.0](https://github.com/msandroid/cription-mcp/releases/tag/v0.4.0). Install that server release separately and follow the [Japanese connection guide](https://github.com/msandroid/cription-mcp/blob/v0.4.0/docs/NOTION-MANUS.ja.md). The existing v0.4.0 coding-agent plugin keeps its v0.3.1 MCP pin.

Notion export was verified by creating and reading back a synthetic page. The shared HTTP transport passed all eight tools and real transcription; public HTTPS passed Bearer authentication and `speech_languages`. Notion Custom Agent testing is blocked by the workspace's Business entitlement. Manus app testing awaits login/terms consent. These are not Marketplace listings for either service.

## Requirements

- macOS 26 or later (for transcription; notes work on older macOS)
- Python 3.9+ (`python3`, bundled with the Xcode Command Line Tools)
- Xcode Command Line Tools (`xcode-select --install`) — the small Swift helper is compiled once on first use
- [`uv`](https://docs.astral.sh/uv/) (`brew install uv`) — the plugin starts the MCP server with `uvx`

## Install

### Claude Code (plugin: MCP server + skills)

```
/plugin marketplace add msandroid/cription-plugins
/plugin install cription@cription
```

### Codex

Install the skills from this release:

```bash
codex plugin marketplace add msandroid/cription-plugins --ref v0.4.0
codex plugin add cription@cription
```

Add the MCP server separately:

```bash
uv tool install --from git+https://github.com/msandroid/cription-mcp@v0.3.1 cription-mcp
uv tool update-shell
```

Reopen your terminal, then run `cription-mcp-setup install codex`. Restart Codex or start a new chat. If the setup command is not on PATH yet, use `"$(uv tool dir --bin)/cription-mcp-setup"`.

### Claude Desktop

Easiest: download `cription-<version>.mcpb` from [cription-mcp Releases](https://github.com/msandroid/cription-mcp/releases) and double-click it (or drag it into Claude → Settings → Extensions).

Or add to `~/Library/Application Support/Claude/claude_desktop_config.json` and restart Claude:

```json
{
  "mcpServers": {
    "cription": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/msandroid/cription-mcp@v0.3.1", "cription-mcp"]
    }
  }
}
```

Use the absolute path to `uvx` (`which uvx`) if Claude cannot find it.

### Antigravity

For a standalone MCP connection:

```bash
uv tool install --from git+https://github.com/msandroid/cription-mcp@v0.3.1 cription-mcp
uv tool update-shell
```

Reopen your terminal and run `cription-mcp-setup install antigravity`. Restart Antigravity, then check **Customizations → Installed → MCP Servers → cription → 8 tools enabled**. Older IDE versions can use `install antigravity-legacy`.

To use the plugin with shared summary skills instead, download this release:

```bash
git clone --branch v0.4.0 --depth 1 https://github.com/msandroid/cription-plugins.git
```

In Antigravity, run `/plugin install /absolute/path/to/cription-plugins/plugins/cription`, replacing the path with your clone's absolute path. See [Google's plugin installation guide](https://www.antigravity.google/docs/plugins?tab=cli).

Use **one** MCP registration in each client. If the plugin cannot find `uvx` in the GUI environment, use the standalone setup command, which configures absolute executable paths, and avoid also enabling the plugin's MCP connection.

### ChatGPT

ChatGPT uses the local server through OpenAI's private **Secure MCP Tunnel**. Follow the [Cription MCP setup guide](https://github.com/msandroid/cription-mcp#chatgpt-private-secure-mcp-tunnel). It requires a tunnel associated with your ChatGPT workspace, a runtime key with Tunnels Read + Use, and a running official `tunnel-client`. The v0.3.1 server includes setup commands and `read_transcript` for paging long transcripts without local file access. Each user creates their own Tunnel and runtime key; the GitHub release does not give access to a shared hosted server.

The Claude and Antigravity plugin configurations pin MCP **v0.3.1**. These files do not install a ChatGPT public-directory plugin. For full ChatGPT setup, see the [Japanese guide](https://github.com/msandroid/cription-mcp/blob/v0.3.1/docs/INSTALL.ja.md#4-chatgpt).

### Cursor (native plugin: MCP + three skills)

```bash
git clone --branch v0.4.0 --depth 1 https://github.com/msandroid/cription-plugins.git
cd cription-plugins
python3 scripts/install_cursor.py
```

Install `uv` first (`brew install uv`) if needed. The installer copies the native Cursor plugin into `~/.cursor/plugins/local/cription` and resolves uvx to an absolute path for GUI launches. Restart Cursor or run **Developer: Reload Window**, then check **Customize** for Cription, three skills and eight MCP tools. Enterprise administrators must allow local plugin imports. Marketplace listing/review is separate; GitHub/local installation is available now.

Run the same script with `--replace` to update; it backs up your previous plugin outside the auto-loaded local folder. Remove `~/.cursor/plugins/local/cription` and reload Cursor to uninstall.

For **MCP only**, install [Cription MCP v0.3.1](https://github.com/msandroid/cription-mcp/releases/tag/v0.3.1), then run `cription-mcp-setup install cursor`. This preserves other entries in `~/.cursor/mcp.json` and creates a backup. The native plugin already includes MCP: use one method to avoid duplicate tools. If switching from standalone MCP, remove only `mcpServers.cription` from the global/project MCP JSON before installing the plugin.

Ask Cursor Agent: “Call Cription speech_languages.” For audio, pass an absolute path on this Mac. Recognition is local; returned transcripts and note text go to the model selected in Cursor. Remote Cloud Agents cannot access this Mac's local server.

Official references: [Cursor local plugins](https://prod.cursor.com/docs/plugins), [Cursor MCP](https://prod.cursor.com/help/customization/mcp).

## Tools

| Tool | What it does |
|---|---|
| `transcribe_audio` | Audio/video file → transcript with `[mm:ss]` timestamps. Options: `locale` (e.g. `ja-JP`), `terms` (names/jargon to spell right), `timestamps`, `save_to`. Long transcripts are saved to a file and can be paged with `read_transcript`. |
| `speech_languages` | Locales the on-device engine supports and has installed. |
| `read_transcript` (MCP v0.2.0+) | Read long generated transcripts in pages, including from ChatGPT. |
| `list_notes` | Your Cription notes, newest first (`limit`, `folder`, `since`). |
| `search_notes` | Full-text search over titles, summaries, transcripts and memos. |
| `get_note` | One note: transcript with speakers, summary, to-dos, memos, bookmarks. |
| `list_folders` | Note folders and counts. |
| `cription_status` | What this Mac supports and which note stores were found. |

## Skills

| Skill | Use |
|---|---|
| `transcribe` | Transcribing a file well: locale, terms, long recordings. |
| `summarize-transcript` | Cription's five summary templates (General, Meeting, Interview, Lecture, Sales call). |
| `cription-notes` | Answering questions from your recordings with citations. |

## Examples

- "Transcribe ~/Downloads/standup.m4a and list the action items with owners."
- "このインタビュー動画（~/Movies/interview.mov）を文字起こしして、印象的な発言を5つ挙げて"
- "What did we decide about pricing in last week's Cription notes?"

## Privacy

The server only reads files you ask it to transcribe and the Cription app's local preferences (`~/Library/Preferences/Cription.plist` or the app container). It writes only its compiled helper and long transcripts under `~/Library/Caches/cription-mcp` (or the plugin data folder). The AI client you use decides what it does with the results.

## Limits

- Supported transcription languages are Apple's SpeechAnalyzer locales (`speech_languages`). Cription the app supports more languages with additional engines.
- No speaker diarization in `transcribe_audio` yet; notes recorded in the app keep their speaker labels.
- Notes recorded on iPhone are visible only once they are on the Mac.

---

## 日本語

Cription の**オンデバイス文字起こし**と**ノート**を、Claude Code・Claude Desktop・Codex・Cursor などの AI エージェントから使えるようにする MCP サーバーとプラグインです。

- **文字起こし**：手元の音声・動画ファイルを Apple SpeechAnalyzer でオンデバイスで文字起こしします（日本語で Cription が最も精度の高いエンジン）。
- **要約**：Cription アプリと同じテンプレート（一般・会議・インタビュー・講義・商談）で議事録にします。
- **ノート検索**：Cription の Mac アプリで録音したノートを読み取り専用で検索・参照します。
- **プライバシー**：音声認識は Mac 上で処理します。返された文字起こし・ノート本文は、接続先の AI サービスに渡ります。

必要なもの：macOS 26 以降（文字起こし）、Xcode Command Line Tools（初回に小さな Swift ヘルパーをビルドします）、`uv`。MCP サーバー本体は [cription-mcp](https://github.com/msandroid/cription-mcp) にあります。

インストール方法は上の [Install](#install) を参照してください。Claude Code なら次の2行です。

```
/plugin marketplace add msandroid/cription-plugins
/plugin install cription@cription
```

## Update and remove

For Claude Code, refresh the marketplace and update the plugin from `/plugin`. For Codex, refresh/re-add the marketplace at the desired release ref, then install that plugin version with `codex plugin add cription@cription`. For an Antigravity local install, download the new tagged source and reinstall its plugin directory. Restart the client afterward.

Standalone server update/removal, config paths and troubleshooting are documented in the [installation guide](https://github.com/msandroid/cription-mcp/blob/v0.3.1/docs/INSTALL.ja.md#更新と削除). Removing a plugin or server does not delete your Cription recordings.

## License

MIT

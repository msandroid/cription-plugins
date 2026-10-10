---
name: transcribe
description: Transcribe a local audio or video file (meeting recording, interview, lecture, voice memo, screen recording) on-device with Cription's transcribe_audio tool. Use when the user points at an audio/video file or asks what was said in a recording.
---

# Transcribe a recording on-device

Use the `transcribe_audio` tool from the **cription** MCP server. It runs Apple SpeechAnalyzer on the user's Mac; the audio never leaves the machine.

## Steps

1. **Find the file.** Use the absolute path. Common formats work directly (wav, m4a, mp3, aiff, caf, mp4, mov). For other containers (webm, mkv, ogg), convert first if `ffmpeg` is available: `ffmpeg -i in.webm -ac 1 -ar 16000 /tmp/in.wav`.
2. **Pick the locale.** Pass `locale` when you know the spoken language (`ja-JP`, `en-US`, `zh-CN`, `de-DE`, …). Without it the Mac's locale is used, which is wrong for foreign-language recordings. Ask the user if you cannot tell. `speech_languages` lists what is supported; the first use of a locale downloads Apple's speech assets once.
3. **Add terms.** Pass names, product names and jargon from the conversation or the file name as `terms` so they are spelled correctly.
4. **Long recordings.** Transcripts over ~40k characters are saved to a file (`savedTo`) and only a preview is returned; read the file in parts. Use `save_to` when the user wants a transcript file anyway.
5. **Report.** Give the user what they asked for (summary, quotes, answers) rather than dumping the whole transcript. Quote with `[mm:ss]` timestamps so they can find the passage.

## If the tool is missing

The cription MCP server is not connected. Run `cription_status` if available; otherwise tell the user to set it up:

- Claude Code: `/plugin marketplace add msandroid/cription-plugins` then `/plugin install cription@cription`
- Codex / other clients: `codex mcp add cription -- uvx --from git+https://github.com/msandroid/cription-mcp cription-mcp`

Requirements: macOS 26+, Xcode Command Line Tools (`xcode-select --install`) for the one-time build.

---
name: meta-ads-setup
description: Set up, reconnect, or check official Meta Ads CLI and Meta Ads MCP for FAPI course learners in local Codex Desktop or Claude Code. Guide Meta Business setup in the browser and run local installation on the learner's behalf without handing them terminal commands.
---

# Set up Meta Ads for a course learner

Use the learner's chosen language. Work in a local desktop session on the learner's computer. This package runs on macOS or Linux, including WSL when the host runs the session inside WSL. If the session is remote or uses native Windows, guide the learner to a supported local session before opening the credential form.

Resolve the absolute path to <code>scripts/course-ads.sh</code> next to this skill. Invoke it through Bash. The commands in this skill are for the agent to run. The learner uses the Meta browser screens, the local credential form, and any approvals their app presents.

## First setup

1. Read [the Meta browser walkthrough](references/meta-browser.md). If access is already configured, verify it before repeating setup. Guide the learner from their first incomplete step, one screen at a time. A real ad account ID and a token with the stated scopes are the inputs to the local form. The user may share the account ID in chat.
2. Run <code>bash /absolute/path/to/course-ads.sh install</code> on the learner's computer. This installs the pinned official Meta Ads CLI and MCP transport in the course's user directory. If the platform asks for approval for the download or user-directory write, identify the operation in the approval. Reuse the installed runtime on subsequent runs.
3. Run <code>bash /absolute/path/to/course-ads.sh connect</code> as an ongoing command. Give the learner the exact loopback URL printed by the command. Direct them to enter the account ID and token in that form. Ask them to return after the form confirms the save, then check the running command. Keep the token out of messages, tool arguments, logs, and output. Read credentials through the supplied commands only.
4. Run <code>bash /absolute/path/to/course-ads.sh cli adaccount get</code> and <code>bash /absolute/path/to/course-ads.sh cli campaign list --limit 3 --fields id,name,status</code>. Compare the returned account ID with the intended account. Use [the browser walkthrough](references/meta-browser.md#když-krok-nefunguje) to diagnose an error.
5. Connect the client to the official Meta Ads MCP endpoint through the local launcher.
   - In Codex, use the installed Codex command to register the local server once. The known macOS desktop app binary is at <code>/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex</code> if <code>codex</code> is absent from PATH. Check the existing server entry before replacing it. Run <code>codex mcp add fapi-course-meta-ads -- bash /absolute/path/to/course-ads.sh mcp</code> with the resolved executable and launcher. If the client executable is unavailable, guide the learner to **Settings → MCP servers → Add server → STDIO** and show the command and the two argument values to paste into those fields. Reload the server or start a new local session when the client still has the old tool list.
   - In Claude Code, the plugin declares <code>fapi-course-meta-ads</code>. Reload the plugin or start a new local session once the token is saved, then check for its tools.
6. Verify MCP by actually calling <code>ads_get_ad_accounts</code> on <code>fapi-course-meta-ads</code>. Confirm the same account ID and name through both tools. Server registration alone is insufficient evidence. Give each route its own observed result and a concrete fix for any failed route. If a new session is required, provide the exact chat prompt that resumes the test.

## Check access or rotate a token

For an access check, repeat both read tests using the current configuration. For a token rotation, open the local form again, then repeat both tests and reload the MCP server if it already held the previous token.

For later requests to manage ads, use the local CLI wrapper or the official Meta Ads MCP tools when the user authorizes the specific change. The wrapper selects the saved account. Pass that account ID explicitly to MCP tools that take an account argument. Pass absolute paths for creative files. A connection test consists of reads. After a write with an unclear outcome, read the saved campaign state before trying again through either route. Meta Marketing API limits also apply to the CLI.

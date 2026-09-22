# Security and data boundaries

**English** · [繁體中文](SECURITY.zh-TW.md)

This repository is a portfolio reference and an offline demonstration. It has no live NAS adapter, production credential store or scheduled-task installer. Running the demo operates on files under the output directory you select. Use a dedicated output directory, not a folder containing business workbooks.

The fixtures are fictional. Published operational evidence consists of authored summaries, source report filenames and hashes; the private reports, account names, internal hosts, raw records and session files are excluded. Historical screenshots were already redacted in the public repository. The code and documentation do not establish that every historical deployment followed the present guidance.

When adapting the ideas, keep credentials outside instructions, logs and source control. Treat authentication failures, unreadable workbooks and incomplete responses as distinct failures. Validate the candidate and the transferred copy before allowing source cleanup. The local demo preserves supported text cells, not arbitrary Excel features, and does not implement network rollback.

If you find an issue, open a [repository issue](https://github.com/jackyngtf/autonomous-agent-workflows/issues) with a minimal synthetic reproduction. Do not attach real credentials, personal records, internal URLs or private workbooks. Do not test against a production system to demonstrate a portfolio bug.

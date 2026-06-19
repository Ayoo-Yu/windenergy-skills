# Output Run Folders

Use this protocol whenever a renewable skill writes files.

## Required Behavior

Create a separate run folder for each skill invocation before writing generated
artifacts. Do not write new reports, tracked documents, figures, slide decks,
reference exports, or intermediate JSON files directly into the source folder
unless the user explicitly requests that layout.

## Default Location

Use the folder that contains the primary input file as the source folder. Create
run folders under:

```text
<SOURCE_DIR>/skill_runs/<YYYYMMDD-HHMMSS>_<skill-name>_<target-or-mode>/
```

Examples:

```text
D:/papers/RE0530/skill_runs/20260531-153012_windenergy-submission_renewable-energy/
D:/papers/RE0530/skill_runs/20260531-153012_windenergy-polishing_manuscript/
```

If no source folder exists, create the run folder under the current working
directory. If the user supplies an output directory, create the run folder under
that directory.

## File Placement

- Place every generated file for the invocation inside the run folder.
- Keep original source files unchanged in their original location.
- Use relative links inside Markdown reports when linking files inside the same
  run folder.
- Use absolute paths in the chat response.
- Keep intermediate plans, changes JSON, extracted text, scan reports, and logs
  in the same run folder when they explain the generated output.
- Put derived images or figure crops under `assets/` inside the run folder.
- Prefer existing bundled scripts and JSON plan files over creating new helper
  scripts for routine operations.

## Tool Failure Recovery

If a file-writing tool fails because required parameters such as `file_path` or
`content` are missing, stop retrying that same malformed call. Use the run
folder and the relevant bundled script instead.

For Word polishing, compression, cross-reference coloring, and citation-marker
coloring:

```bash
python <skill_root>/scripts/polish_docx.py INPUT.docx changes.json OUTPUT.docx --color-crossrefs
```

Only create new helper scripts when the existing bundled script cannot perform
the operation and the user request genuinely requires new automation.

## Manifest

Write `RUN_MANIFEST.md` in the run folder with:

- skill name
- timestamp
- source directory
- target journal or mode
- input files
- generated files
- manual author decisions

## Script

Use the helper script when a deterministic path is useful:

```bash
python <skill_root>/../_shared/scripts/create_run_folder.py --source-dir SOURCE_DIR --skill windenergy-submission --target renewable-energy
```

The script prints JSON containing `run_dir` and `manifest_path`.

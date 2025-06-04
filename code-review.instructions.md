---
applyTo: "**"
---
# Project coding review strategy

- Apply the [general coding guidelines](https://google.github.io/eng-practices/review/) to review code.
- Execute pre-commit hooks to check code style and quality.
    formatter: `ruff`
    linter: `ruff`
    typeChecker: `mypy`
    licenseChecker: `licensecheck`

## Guidelines
- [general coding guidelines](https://google.github.io/styleguide/) に従っているか確認
- 必ず英語でわかりやすいようにコメントを英語で入れてください
- docs/以下のファイルは実装の内容が変わったら一緒に必ず修正してください
- docs/以下のファイルは内容が変わるような実装は必ず私に許可を得てください。
- Add a comment at the end of the file: 'Contains AI-generated edits.'
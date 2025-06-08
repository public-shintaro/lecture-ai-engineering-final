├── .gitattributes
├── .github
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows
    │   ├── deploy.yml
    │   ├── integrate.yml
    │   ├── lint.yml
    │   └── test.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── LICENSE
├── README.md
├── docs
    ├── architecture.drawio.svg
    ├── argo.drawio.svg
    ├── argo.md
    ├── changelog.md
    ├── contributing.md
    ├── eval-dataset.md
    ├── eval-method.md
    ├── eval-result.md
    ├── eval-summary.png
    ├── index.md
    └── prompts.md
├── eval
    ├── __main__.py
    ├── impl
    │   ├── __init__.py
    │   ├── cache_repository.py
    │   ├── figure.py
    │   ├── gcs_helper.py
    │   ├── llm.py
    │   └── parser.py
    ├── models
    │   └── __init__.py
    ├── settings.py
    └── usecase
    │   ├── __init__.py
    │   └── evaluator.py
├── exparso
    ├── __init__.py
    ├── core
    │   ├── __init__.py
    │   ├── context
    │   │   ├── __init__.py
    │   │   └── update_context.py
    │   ├── docs_type
    │   │   ├── __init__.py
    │   │   └── judge_document_type.py
    │   ├── parse
    │   │   ├── __init__.py
    │   │   └── parse_document.py
    │   ├── parse_core_service.py
    │   ├── prompt
    │   │   ├── __init__.py
    │   │   ├── default_prompt.py
    │   │   └── prompt.py
    │   └── type.py
    ├── llm
    │   ├── __init__.py
    │   ├── claude.py
    │   ├── gemini.py
    │   ├── llm_factory.py
    │   └── openai.py
    ├── loader
    │   ├── __init__.py
    │   ├── csv_loader.py
    │   ├── docx_loader.py
    │   ├── image_loader.py
    │   ├── loader_factory.py
    │   ├── pdf_loader.py
    │   ├── pptx_loader.py
    │   ├── text_file_loader.py
    │   └── xlsx_loader.py
    └── model
    │   ├── __init__.py
    │   ├── cost.py
    │   ├── document.py
    │   ├── image.py
    │   ├── llm.py
    │   ├── page_contents.py
    │   └── page_loader.py
├── mkdocs.yml
├── pyproject.toml
├── tests
    ├── __init__.py
    ├── constants.py
    ├── data
    │   ├── test.bmp
    │   ├── test.csv
    │   ├── test.docx
    │   ├── test.jpg
    │   ├── test.md
    │   ├── test.pdf
    │   ├── test.pptx
    │   └── test.xlsx
    ├── integrate
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── core
    │   │   ├── __init__.py
    │   │   ├── conftest.py
    │   │   ├── test_docs_type.py
    │   │   ├── test_parse_document.py
    │   │   └── test_update_context.py
    │   ├── llm
    │   │   ├── __init__.py
    │   │   ├── conftest.py
    │   │   ├── test_claude.py
    │   │   ├── test_gemini.py
    │   │   └── test_openai.py
    │   ├── loader
    │   │   ├── __init__.py
    │   │   ├── test_docx_loader.py
    │   │   └── test_pptx_loader.py
    │   ├── test_error.py
    │   ├── test_model_aoai.py
    │   ├── test_model_claude.py
    │   ├── test_model_gemini.py
    │   └── test_model_none.py
    └── unit
    │   ├── __init__.py
    │   ├── core
    │       ├── __init__.py
    │       └── prompt
    │       │   ├── __init__.py
    │       │   └── test_prompt.py
    │   ├── llm
    │       ├── __Init__.py
    │       └── test_llm_factory.py
    │   ├── loader
    │       ├── __Init__.py
    │       ├── test_csv_loader.py
    │       ├── test_image_loader.py
    │       ├── test_pdf_loader.py
    │       ├── test_text_file_loader.py
    │       └── test_xlsx_loader.py
    │   └── model
    │       ├── __init__.py
    │       ├── test_document.py
    │       └── test_llm_model.py
└── uv.lock


/.gitattributes:
--------------------------------------------------------------------------------
 1 | *.jpg filter=lfs diff=lfs merge=lfs -text
 2 | *.pdf filter=lfs diff=lfs merge=lfs -text
 3 | *.png filter=lfs diff=lfs merge=lfs -text
 4 | *.jpg filter=lfs diff=lfs merge=lfs -text
 5 | *.bmp filter=lfs diff=lfs merge=lfs -text
 6 | *.gif filter=lfs diff=lfs merge=lfs -text
 7 | *.jpeg filter=lfs diff=lfs merge=lfs -text
 8 | *.tiff filter=lfs diff=lfs merge=lfs -text
 9 | *.tif filter=lfs diff=lfs merge=lfs -text
10 | *.csv filter=lfs diff=lfs merge=lfs -text
11 | *.xls filter=lfs diff=lfs merge=lfs -text
12 | *.xlsx filter=lfs diff=lfs merge=lfs -text
13 | *.doc filter=lfs diff=lfs merge=lfs -text
14 | *.docx filter=lfs diff=lfs merge=lfs -text
15 | *.ppt filter=lfs diff=lfs merge=lfs -text
16 | *.pptx filter=lfs diff=lfs merge=lfs -text
17 |


--------------------------------------------------------------------------------
/.github/PULL_REQUEST_TEMPLATE.md:
--------------------------------------------------------------------------------
1 | #### 変更内容
2 |
3 | - 主な変更点を箇条書きで記載してください。
4 |


--------------------------------------------------------------------------------
/.github/workflows/deploy.yml:
--------------------------------------------------------------------------------
 1 | name: deploy library
 2 |
 3 | on:
 4 |   push:
 5 |     tags:
 6 |       - "v*"
 7 |
 8 | jobs:
 9 |   check_conditions:
10 |     runs-on: ubuntu-latest
11 |     outputs:
12 |       version: ${{ steps.check_conditions.outputs.version }}
13 |       exist_tag: ${{ steps.check_conditions.outputs.exist_tag }}
14 |     steps:
15 |       - uses: actions/checkout@v4
16 |       - name: Check conditions
17 |         id: check_conditions
18 |         run: |
19 |           export VERSION=v$(grep -m1 'version = ' pyproject.toml | sed -E "s/version = ['\"]([^'\"]+)['\"].*/\1/")
20 |           # タグと一致するかの確認
21 |           if [[ ${{ github.ref_name }} != $VERSION ]]; then
22 |             # Actionを終了する
23 |             echo "exist_tag=true" >> $GITHUB_OUTPUT
24 |           else
25 |             echo "exist_tag=false" >> $GITHUB_OUTPUT
26 |             echo "version=$VERSION" >> $GITHUB_OUTPUT
27 |           fi
28 |
29 |   deploy-repo:
30 |     permissions:
31 |       id-token: write
32 |       contents: write
33 |     runs-on: ubuntu-latest
34 |     needs: check_conditions
35 |     steps:
36 |       - uses: actions/checkout@v4
37 |       - uses: actions/setup-python@v5
38 |         with:
39 |           python-version: 3.12
40 |
41 |       - name: Install uv
42 |         uses: astral-sh/setup-uv@v3
43 |         with:
44 |           version: "0.5.20"
45 |
46 |       - name: Deploy PyPI Repo
47 |         run: |
48 |           uv build
49 |           uv run --only-group deploy twine upload dist/* -r pypi \
50 |             -u ${{ secrets.PYPI_USERNAME }} \
51 |             -p ${{ secrets.PYPI_API_TOKEN }}
52 |
53 |       - name: Build the documentation
54 |         run: |
55 |           uv run --only-group docs mkdocs build
56 |
57 |       - name: Deploy to GitHub Pages
58 |         uses: peaceiris/actions-gh-pages@v3
59 |         with:
60 |           github_token: ${{ secrets.GITHUB_TOKEN }}
61 |           publish_dir: site
62 |           publish_branch: gh-pages
63 |


--------------------------------------------------------------------------------
/.github/workflows/integrate.yml:
--------------------------------------------------------------------------------
 1 | name: integration test
 2 |
 3 | on:
 4 |   workflow_call:
 5 |   workflow_dispatch:
 6 |   pull_request:
 7 |     branches:
 8 |       - main
 9 |     paths:
10 |       - exparso/**/*.py
11 |       - tests/**/*.py
12 |       - ".github/workflows/test.yml"
13 |       - ".github/workflows/integrate.yml"
14 |       - ".github/workflows/evaluate.yml"
15 |
16 | jobs:
17 |   lint:
18 |     uses: ./.github/workflows/lint.yml
19 |
20 |   unittest_3_12:
21 |     needs: lint
22 |     uses: ./.github/workflows/test.yml
23 |     with:
24 |       PYTHON_VERSION: "3.12"
25 |       TEST_PATH: unit
26 |     secrets: inherit
27 |
28 |   unittest_3_11:
29 |     needs: lint
30 |     uses: ./.github/workflows/test.yml
31 |     with:
32 |       PYTHON_VERSION: "3.11"
33 |       TEST_PATH: unit
34 |     secrets: inherit
35 |
36 |   unittest_3_10:
37 |     needs: lint
38 |     uses: ./.github/workflows/test.yml
39 |     with:
40 |       PYTHON_VERSION: "3.10"
41 |       TEST_PATH: unit
42 |     secrets: inherit
43 |
44 |   integrate_3_12:
45 |     needs: [unittest_3_12, unittest_3_11, unittest_3_10]
46 |     uses: ./.github/workflows/test.yml
47 |     with:
48 |       PYTHON_VERSION: "3.12"
49 |       TEST_PATH: integrate
50 |     secrets: inherit
51 |
52 |   integrate_3_11:
53 |     needs: [unittest_3_12, unittest_3_11, unittest_3_10]
54 |     uses: ./.github/workflows/test.yml
55 |     with:
56 |       PYTHON_VERSION: "3.11"
57 |       TEST_PATH: integrate
58 |     secrets: inherit
59 |
60 |   integrate_3_10:
61 |     needs: [unittest_3_12, unittest_3_11, unittest_3_10]
62 |     uses: ./.github/workflows/test.yml
63 |     with:
64 |       PYTHON_VERSION: "3.10"
65 |       TEST_PATH: integrate
66 |     secrets: inherit
67 |
68 |


--------------------------------------------------------------------------------
/.github/workflows/lint.yml:
--------------------------------------------------------------------------------
 1 | name: lint
 2 |
 3 | on:
 4 |   workflow_call:
 5 |
 6 | env:
 7 |   PYTHON_VERSION: 3.12
 8 |
 9 | jobs:
10 |   lint:
11 |     runs-on: ubuntu-latest
12 |     steps:
13 |       - uses: actions/checkout@v4
14 |
15 |       - uses: actions/setup-python@v5
16 |         with:
17 |           python-version: ${{ env.PYTHON_VERSION }}
18 |
19 |       - name: Install uv
20 |         uses: astral-sh/setup-uv@v3
21 |         with:
22 |           version: "0.5.20"
23 |
24 |       - name: Run lint
25 |         run: uv run ruff check .
26 |
27 |       - name: Run format check
28 |         run: uv run ruff format --check .
29 |
30 |       - name: Run type check
31 |         run: uv run mypy exparso
32 |


--------------------------------------------------------------------------------
/.github/workflows/test.yml:
--------------------------------------------------------------------------------
 1 | name: test
 2 |
 3 | on:
 4 |   workflow_call:
 5 |     inputs:
 6 |       PYTHON_VERSION:
 7 |         required: true
 8 |         type: string
 9 |       TEST_PATH:
10 |         required: true
11 |         type: string
12 |
13 | jobs:
14 |   test:
15 |     permissions:
16 |       id-token: write
17 |       contents: read
18 |     runs-on: ubuntu-latest
19 |     steps:
20 |       - name: libreoffice
21 |         if: inputs.TEST_PATH == 'integrate'
22 |         run: |
23 |           sudo apt-get update
24 |           sudo apt-get install -y libreoffice
25 |
26 |       - uses: actions/checkout@v4
27 |         with:
28 |           lfs: true
29 |
30 |       - name: delete .python-version
31 |         run: |
32 |           rm -rf .python-version
33 |
34 |       - uses: actions/setup-python@v5
35 |         with:
36 |           python-version: ${{ inputs.PYTHON_VERSION }}
37 |
38 |       - name: Install uv
39 |         uses: astral-sh/setup-uv@v3
40 |         with:
41 |           version: "0.5.20"
42 |
43 |       - name: Read all secrets and set them to environment variables
44 |         if: inputs.TEST_PATH == 'integrate'
45 |         env:
46 |           ALL_SECRETS: ${{ toJSON(secrets) }}
47 |         run: |
48 |           # 全てのシークレットをループして環境変数に設定
49 |           echo "$ALL_SECRETS" | jq -r 'to_entries[] | "\(.key)=\(.value)"' | \
50 |           while IFS= read -r line; do
51 |             # シークレットのキーと値を取得
52 |             key=$(echo "$line" | cut -d'=' -f1)
53 |             value=$(echo "$line" | cut -d'=' -f2-)
54 |             # 環境変数として設定
55 |             echo "$key=$value" >> $GITHUB_ENV
56 |           done
57 |
58 |       - name: Authenticate to Google Cloud
59 |         if: inputs.TEST_PATH == 'integrate'
60 |         uses: google-github-actions/auth@v2
61 |         with:
62 |           workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
63 |           service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}
64 |
65 |       - name: Run pytest
66 |         run: uv run pytest tests/${{ inputs.TEST_PATH }}
67 |


--------------------------------------------------------------------------------
/.gitignore:
--------------------------------------------------------------------------------
  1 | # Created by https://www.toptal.com/developers/gitignore/api/macos,windows,python,venv,visualstudiocode
  2 | # Edit at https://www.toptal.com/developers/gitignore?templates=macos,windows,python,venv,visualstudiocode
  3 |
  4 | ### macOS ###
  5 | # General
  6 | .DS_Store
  7 | .AppleDouble
  8 | .LSOverride
  9 |
 10 | # Icon must end with two \r
 11 | Icon
 12 |
 13 |
 14 | # Thumbnails
 15 | ._*
 16 |
 17 | # Files that might appear in the root of a volume
 18 | .DocumentRevisions-V100
 19 | .fseventsd
 20 | .Spotlight-V100
 21 | .TemporaryItems
 22 | .Trashes
 23 | .VolumeIcon.icns
 24 | .com.apple.timemachine.donotpresent
 25 |
 26 | # Directories potentially created on remote AFP share
 27 | .AppleDB
 28 | .AppleDesktop
 29 | Network Trash Folder
 30 | Temporary Items
 31 | .apdisk
 32 |
 33 | ### macOS Patch ###
 34 | # iCloud generated files
 35 | *.icloud
 36 |
 37 | ### Python ###
 38 | # Byte-compiled / optimized / DLL files
 39 | __pycache__/
 40 | *.py[cod]
 41 | *$py.class
 42 |
 43 | # C extensions
 44 | *.so
 45 |
 46 | # Distribution / packaging
 47 | .Python
 48 | build/
 49 | develop-eggs/
 50 | dist/
 51 | downloads/
 52 | eggs/
 53 | .eggs/
 54 | lib/
 55 | lib64/
 56 | parts/
 57 | sdist/
 58 | var/
 59 | wheels/
 60 | share/python-wheels/
 61 | *.egg-info/
 62 | .installed.cfg
 63 | *.egg
 64 | MANIFEST
 65 |
 66 | # PyInstaller
 67 | #  Usually these files are written by a python script from a template
 68 | #  before PyInstaller builds the exe, so as to inject date/other infos into it.
 69 | *.manifest
 70 | *.spec
 71 |
 72 | # Installer logs
 73 | pip-log.txt
 74 | pip-delete-this-directory.txt
 75 |
 76 | # Unit test / coverage reports
 77 | htmlcov/
 78 | .tox/
 79 | .nox/
 80 | .coverage
 81 | .coverage.*
 82 | .cache
 83 | nosetests.xml
 84 | coverage.xml
 85 | *.cover
 86 | *.py,cover
 87 | .hypothesis/
 88 | .pytest_cache/
 89 | cover/
 90 |
 91 | # Translations
 92 | *.mo
 93 | *.pot
 94 |
 95 | # Django stuff:
 96 | *.log
 97 | local_settings.py
 98 | db.sqlite3
 99 | db.sqlite3-journal
100 |
101 | # Flask stuff:
102 | instance/
103 | .webassets-cache
104 |
105 | # Scrapy stuff:
106 | .scrapy
107 |
108 | # Sphinx documentation
109 | docs/_build/
110 |
111 | # PyBuilder
112 | .pybuilder/
113 | target/
114 |
115 | # Jupyter Notebook
116 | .ipynb_checkpoints
117 |
118 | # IPython
119 | profile_default/
120 | ipython_config.py
121 |
122 | # pyenv
123 | #   For a library or package, you might want to ignore these files since the code is
124 | #   intended to run in multiple environments; otherwise, check them in:
125 | # .python-version
126 |
127 | # pipenv
128 | #   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
129 | #   However, in case of collaboration, if having platform-specific dependencies or dependencies
130 | #   having no cross-platform support, pipenv may install dependencies that don't work, or not
131 | #   install all needed dependencies.
132 | #Pipfile.lock
133 |
134 | # poetry
135 | #   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
136 | #   This is especially recommended for binary packages to ensure reproducibility, and is more
137 | #   commonly ignored for libraries.
138 | #   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
139 | #poetry.lock
140 |
141 | # pdm
142 | #   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
143 | #pdm.lock
144 | #   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
145 | #   in version control.
146 | #   https://pdm.fming.dev/#use-with-ide
147 | .pdm.toml
148 |
149 | # PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
150 | __pypackages__/
151 |
152 | # Celery stuff
153 | celerybeat-schedule
154 | celerybeat.pid
155 |
156 | # SageMath parsed files
157 | *.sage.py
158 |
159 | # Environments
160 | .env
161 | .env.eval
162 | .venv
163 | env/
164 | venv/
165 | ENV/
166 | env.bak/
167 | venv.bak/
168 |
169 | # Spyder project settings
170 | .spyderproject
171 | .spyproject
172 |
173 | # Rope project settings
174 | .ropeproject
175 |
176 | # mkdocs documentation
177 | /site
178 |
179 | # mypy
180 | .mypy_cache/
181 | .dmypy.json
182 | dmypy.json
183 |
184 | # Pyre type checker
185 | .pyre/
186 |
187 | # pytype static type analyzer
188 | .pytype/
189 |
190 | # Cython debug symbols
191 | cython_debug/
192 |
193 | # PyCharm
194 | #  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
195 | #  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
196 | #  and can be added to the global gitignore or merged into this file.  For a more nuclear
197 | #  option (not recommended) you can uncomment the following to ignore the entire idea folder.
198 | #.idea/
199 |
200 | ### Python Patch ###
201 | # ruff
202 | .ruff_cache/
203 |
204 | # LSP config files
205 | pyrightconfig.json
206 |
207 | ### venv ###
208 | # Virtualenv
209 | # http://iamzed.com/2009/05/07/a-primer-on-virtualenv/
210 | [Bb]in
211 | [Ii]nclude
212 | [Ll]ib
213 | [Ll]ib64
214 | [Ll]ocal
215 | [Ss]cripts
216 | pyvenv.cfg
217 | pip-selfcheck.json
218 |
219 | ### VisualStudioCode ###
220 |
221 | # Local History for Visual Studio Code
222 | .history/
223 |
224 | # Built Visual Studio Code Extensions
225 | *.vsix
226 |
227 | ### VisualStudioCode Patch ###
228 | # Ignore all local history of files
229 | .history
230 | .ionide
231 |
232 | ### Windows ###
233 | # Windows thumbnail cache files
234 | Thumbs.db
235 | Thumbs.db:encryptable
236 | ehthumbs.db
237 | ehthumbs_vista.db
238 |
239 | # Dump file
240 | *.stackdump
241 |
242 | # Folder config file
243 | [Dd]esktop.ini
244 |
245 | # Recycle Bin used on file shares
246 | $RECYCLE.BIN/
247 |
248 | # Windows Installer files
249 | *.cab
250 | *.msi
251 | *.msix
252 | *.msm
253 | *.msp
254 |
255 | # Windows shortcuts
256 | *.lnk
257 |
258 | # End of https://www.toptal.com/developers/gitignore/api/macos,windows,python,venv,visualstudiocode
259 |
260 | # Redis dump file
261 | *.rdb
262 |
263 | # Secrets directory
264 | secrets/*
265 |
266 | # data
267 | result
268 | ~*.xlsx
269 |
270 | .vscode


--------------------------------------------------------------------------------
/.pre-commit-config.yaml:
--------------------------------------------------------------------------------
 1 | default_stages: [pre-commit]
 2 | default_language_version:
 3 |     python: python3.12
 4 | repos:
 5 | -   repo: local
 6 |     hooks:
 7 |     -   id: format
 8 |         name: format
 9 |         entry: uv run ruff format
10 |         language: system
11 |         files: .*\.(py|ipynb)$
12 |     -   id: lint
13 |         name: lint
14 |         entry: uv run ruff check
15 |         language: system
16 |         files: .*\.(py|ipynb)$
17 |     -   id: type-check
18 |         name: type-check
19 |         entry: uv run mypy exparso --explicit-package-bases
20 |         language: system
21 |         pass_filenames: false
22 |     -   id: unittest
23 |         name: unittest
24 |         language: system
25 |         always_run: true
26 |         pass_filenames: false
27 |         entry: uv run pytest tests/unit
28 |


--------------------------------------------------------------------------------
/.python-version:
--------------------------------------------------------------------------------
1 | 3.12
2 |


--------------------------------------------------------------------------------
/LICENSE:
--------------------------------------------------------------------------------
 1 | MIT License
 2 |
 3 | Copyright (c) 2025 Insight Edge Inc.
 4 |
 5 | Permission is hereby granted, free of charge, to any person obtaining a copy
 6 | of this software and associated documentation files (the "Software"), to deal
 7 | in the Software without restriction, including without limitation the rights
 8 | to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 9 | copies of the Software, and to permit persons to whom the Software is
10 | furnished to do so, subject to the following conditions:
11 |
12 | The above copyright notice and this permission notice shall be included in all
13 | copies or substantial portions of the Software.
14 |
15 | THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
16 | IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
17 | FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
18 | AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
19 | LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
20 | OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
21 | SOFTWARE.
22 |


--------------------------------------------------------------------------------
/README.md:
--------------------------------------------------------------------------------
 1 | # 📑 Exparso
 2 |
 3 | ![python](https://img.shields.io/badge/python-%20%203.10%20|%203.11%20|%203.12-blue)
 4 |
 5 | 本ライブラリは、画像を含むドキュメントのパースを行うためのライブラリです。
 6 | テキストとして出力することで、従来のベクトル検索や全文検索での利用を可能することを目的とします。
 7 | [](<より詳しい情報に関しては、[こちら](https://congenial-waddle-5krzvq6.pages.github.io/)を参照してください。>)
 8 |
 9 | ## 📥 インストール方法
10 |
11 | ### LibreOffice
12 |
13 | Office ファイルをテキストに変換するために、LibreOffice をインストールします。
14 |
15 | ```bash
16 | # Ubuntu
17 | sudo apt install libreoffice
18 |
19 | # Mac
20 | brew install --cask libreoffice
21 | ```
22 |
23 | ### ライブラリのインストール
24 |
25 | ```bash
26 | pip install exparso
27 | ```
28 |
29 | ## 💡 使用方法
30 |
31 | `parse_document` 関数を利用して、ドキュメントをパースします。
32 |
33 | ```python
34 | from exparso import parse_document
35 | from langchain_openai import AzureChatOpenAI
36 |
37 | llm_model = AzureChatOpenAI(model="gpt-4o")
38 | text = parse_document(path="path/to/document.pdf", model=llm_model)
39 | ```
40 |
41 | ## 📑 対応ファイル
42 |
43 | | コンテンツタイプ      | 拡張子                     |
44 | | --------------------- | -------------------------- |
45 | | **📑 ドキュメント**   | PDF, PowerPoint            |
46 | | **🖼️ 画像**           | JPEG, PNG, BMP             |
47 | | **📝 テキストデータ** | テキストファイル, Markdown |
48 | | **📊 表データ**       | Excel, CSV                 |
49 |
50 | ## 🔥 LLM
51 |
52 | | クラウドベンダー | モデル                                                                                                              |
53 | | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
54 | | Azure            | ChatGPT(`gpt-4o`, `gpt-4o-mini`)                                                                                    |
55 | | Google Cloud     | Claude(`claude-3.7-sonnet`,`claude-3.5-sonnet`), Gemini(`gemini-2.0-flash`,`gemini-1.5-flash-*`,`gemini-2.0-pro-*`) |
56 |


--------------------------------------------------------------------------------
/docs/argo.drawio.svg:
--------------------------------------------------------------------------------
  1 | <svg host="65bd71144e" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="1042px" height="309px" viewBox="-0.5 -0.5 1042 309" content="&lt;mxfile&gt;&lt;diagram id=&quot;R8muaBCvNlKUVFcB-VQq&quot; name=&quot;ページ1&quot;&gt;7VtPc5s4FP8se+BoRkhIwNEkTntoZ3amh909yiDbTDB4MY6T/fQrgWRACNtJwB132kMtPQkhvb+/90Qs9LB9/VLQ3eZ7HrPUgiB+tdCjBSF0CeA/gvJWUxwSkJqyLpJY0hrCj+Q/JonywfUhidm+M7HM87RMdl1ilGcZi8oOjRZFfuxOW+Vp9607umY9wo+Ipn3qX0lcbmqqD72G/pUl6416Mz9gPbKlarI8yX5D4/zYIqGFhR6KPC/r1vb1gaWCe4ov9XNPA6OnjRUsK696wJU725dv6nQs5oeV3SzP+E+4Kbcp7zm8yRcu3v7mHaA6/4iOjVX38bU9+PgmezHdb1gsF+lvU+5cvLtFkJv+wvIt44vxCQVLaZm8dAVBpTzXp3mnR//ME/4KCKTyzWDg2cQJmn/1ClITZ9qC+/xQREyu0bCRN1qbakgVc82Mhg5+J6MHeVRvSi4L5AFKWqxZqd7ljs3NzsnPHVPt54WmB7ls79xc6XeiGefRYVudLjxukpL92NHqXEfuNrq8WOaHLGbxt6Ui7GufAGx4jlMvrCjZ61kOKL3AAHQ1gWDbQTXp2Ni448ppm7Z9IzAC55Rza3Nu4VmBa4WhtcCWjyz/qcfLouaMZMsFNgp+JNyNzdNknXHaNoljsdAoHHS9wA4CD3fY6EAbeaD1z+mzFIg5uM9WKJzKCHx1DHxFFTuJbIQPshEoyjxUc7zuHGiFdyeEGZeCA4Og5/Wuk8IYMoAXZACt+aPib6CG/LtjNCJGpzEtb5HB45JUeNX9jmYdBpJ/DwJZhKs8K2cruk1SvvM5n/KVpS9McKtiD6jGax8rRh24e20P1OuJkSwvtjRtjb3QIqH8l/OclodCoLSz8yK6G5pylJwSgy4A9UjKypIVM36yKMnW/SfzYrehmVyyDg6Ay7ScJVxxMrkaUMepRsqCP7Dia6jVslpJhAgrqNha6pgXcfflp7X4fpfPCV9OrLkvi/yZzaQS9N8ZsygveOjNs1m5SaLnjO3li5IsKRN1Gn1ui/Nn50V5mheGeas0p6V+zDjZ71L6pqanCR+A4I9ku8uLklbhudEc3lpXv9Jhznvu0VcNpIZQz9+eKK5SVa7mtbbK5XXLFye8bPJUmnrERc04A8KULlka0uh5XbmOh5ovCm0JNVOkmK3oIS3Hcg+BYweg5XA9DV1AmxgcBTKgC3cUJ0HeiT7brJGjH0X+1wFZhVm7QDYYG8gOpAWOo4dMHXvU+xonFXAHo2HQjYYciGDVcHrG4yvjWRaNWWJBn7uq0c86mhgKLhtU7ceUIlgQkchny5Uhupa5eHSVpGlrdkyZv4pGsikY6DIKbIh7RhQYbAj5p5mfMiOMr8HotQgDKCh8NxJLQssHPWG0jZB7202+zjOaLhrqGKn3lQZoyiShP7YBXs1rz4Tbjbx2rPlcNgJPURZizhxYoSvFYICT7+L+QChp4saQeFx4QT5V709WJJxJImp9VmgE3sZrIpVaqWTPRdP5TFNdofZ+IlQNo1wDih3AMiM433oOb3DP6wt7F425FSyE5nJKrZXSL5+AT32AAeBTbPLt8rC/7KqnAzMOcruO1wWmNMc3OF5/DPDioYkt9zpbU77wp9gadDVbw/5ktqYOasAnxmpI3w4qrZdm5Ig5nBIu1FPO+RrKfcES3K0bKoXvpP8TIhLXgEh01t5DvdWBge0YylKmeivGtu+PwDt8Pim6PR6bGHoN5D6IaKLAQXeNgVuQeVHQt9a0nZiwN7xIW/dpYDwINOnVL/iwG3MNkGHMSH+mxHFlOfPuihrI9rUwhDxjxXOyQgb2ekL9/u3b9wpWcYhFqhQBCDn8KgHGdTT0hYGNvHYxv58DTxpycB8e3EICMVkS7rGvlMBqtYLRRBLoXWrdWADeJ+sIH85kxyk0YGPO6t0m2mHYvfHnQcl2tXg3IpTGAzHoA7GjH4OIFYRVfYOIi8uwrxX3anBcSjbyu3JyHdtzb2tnKre7M2wNkfYpg+tp178Gf2X8rkFd236Oi6aa6T3f/fKUzwYA6sVobCpGT3v1S4hBQX9f/f6++p346rdCeuG8asxFEPolL3Gh+JojaME8pLlVaAPSt/jJUh/ST33uIRy5QE8ZOd+ujEBjVXrIcEXzdyngQzL1uqahffWHxMdRNzQNz2AaJ1ZrFev5U0tSHDnj88j5Z4MN17d9RwMbDrD9iwnolMBDVYFaHLtZXVSlVLevixKNdQN10d5K+jogsB09QRkx5/T7YcEoHNvHTltAMw5roXtBRuw1KeunPYJlv5auF3iy3zwqOu0n9UvuT9x8q+TsJ+kG1nVD1EF7nzm/V1Og9p2YQ4QjdU+JmwL8U2iN29OakYtKJ81p641zXmcaZcUdXzJKIYqYb1g0nfLxJCqEfa2oqHuXAdn2v8IgGr7yuB17iP/U/7kagBrxb1p8U2pPrPlDg50GPxBVn+hoNWN5P/xrAKSOXE6R9xIigpBH93cHad5t/mysFmbz13do8T8=&lt;/diagram&gt;&lt;/mxfile&gt;">
  2 |     <defs/>
  3 |     <g>
  4 |         <path d="M 140 64.87 L 198.63 64.87" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
  5 |         <path d="M 203.88 64.87 L 196.88 68.37 L 198.63 64.87 L 196.88 61.37 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
  6 |         <path d="M 0 -0.13 L 140 -0.13 L 140 116.87 Q 105 93.47 70 116.87 Q 35 140.27 0 116.87 L 0 12.87 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
  7 |         <rect x="20" y="77.37" width="102.38" height="20.5" rx="3.07" ry="3.07" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
  8 |         <g transform="translate(-0.5 -0.5)">
  9 |             <switch>
 10 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
 11 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 100px; height: 1px; padding-top: 88px; margin-left: 21px;">
 12 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
 13 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
 14 |                                 画像
 15 |                             </div>
 16 |                         </div>
 17 |                     </div>
 18 |                 </foreignObject>
 19 |                 <text x="71" y="91" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
 20 |                     画像
 21 |                 </text>
 22 |             </switch>
 23 |         </g>
 24 |         <rect x="20" y="52.87" width="102.38" height="20" rx="3" ry="3" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
 25 |         <g transform="translate(-0.5 -0.5)">
 26 |             <switch>
 27 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
 28 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 100px; height: 1px; padding-top: 63px; margin-left: 21px;">
 29 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
 30 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
 31 |                                 テーブルデータ
 32 |                             </div>
 33 |                         </div>
 34 |                     </div>
 35 |                 </foreignObject>
 36 |                 <text x="71" y="66" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
 37 |                     テーブルデータ
 38 |                 </text>
 39 |             </switch>
 40 |         </g>
 41 |         <rect x="20" y="28.87" width="102.38" height="20" rx="3" ry="3" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
 42 |         <g transform="translate(-0.5 -0.5)">
 43 |             <switch>
 44 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
 45 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 100px; height: 1px; padding-top: 39px; margin-left: 21px;">
 46 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
 47 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
 48 |                                 テキスト
 49 |                             </div>
 50 |                         </div>
 51 |                     </div>
 52 |                 </foreignObject>
 53 |                 <text x="71" y="42" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
 54 |                     テキスト
 55 |                 </text>
 56 |             </switch>
 57 |         </g>
 58 |         <rect x="8.09" y="2.37" width="130" height="40" fill="none" stroke="none" pointer-events="all"/>
 59 |         <g transform="translate(-0.5 -0.5)">
 60 |             <switch>
 61 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
 62 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 9px; margin-left: 9px;">
 63 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
 64 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
 65 |                                 <span style="font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;">
 66 |                                     ページコンテンツ
 67 |                                 </span>
 68 |                             </div>
 69 |                         </div>
 70 |                     </div>
 71 |                 </foreignObject>
 72 |                 <text x="73" y="21" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
 73 |                     ページコンテンツ
 74 |                 </text>
 75 |             </switch>
 76 |         </g>
 77 |         <path d="M 295 64.87 L 359.63 64.87" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
 78 |         <path d="M 364.88 64.87 L 357.88 68.37 L 359.63 64.87 L 357.88 61.37 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
 79 |         <rect x="205" y="45.75" width="90" height="38.25" fill="#dae8fc" stroke="#6c8ebf" pointer-events="all"/>
 80 |         <g transform="translate(-0.5 -0.5)">
 81 |             <switch>
 82 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
 83 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 88px; height: 1px; padding-top: 53px; margin-left: 206px;">
 84 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
 85 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
 86 |                                 ドキュメント
 87 |                                 <br/>
 88 |                                 判別
 89 |                             </div>
 90 |                         </div>
 91 |                     </div>
 92 |                 </foreignObject>
 93 |                 <text x="250" y="65" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
 94 |                     ドキュメント
 95 | 判別
 96 |                 </text>
 97 |             </switch>
 98 |         </g>
 99 |         <path d="M 445.95 64.92 L 488 64.92 Q 498 64.92 498 74.92 L 498 154.08 Q 498 164.08 508 164.09 L 543.63 164.12" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
100 |         <path d="M 548.88 164.12 L 541.88 167.62 L 543.63 164.12 L 541.88 160.62 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
101 |         <g transform="translate(-0.5 -0.5)">
102 |             <switch>
103 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
104 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 115px; margin-left: 498px;">
105 |                         <div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
106 |                             <div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;">
107 |                                 画像を含む
108 |                             </div>
109 |                         </div>
110 |                     </div>
111 |                 </foreignObject>
112 |                 <text x="498" y="118" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle">
113 |                     画像を含む
114 |                 </text>
115 |             </switch>
116 |         </g>
117 |         <path d="M 445.96 64.91 L 723.63 64.91" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
118 |         <path d="M 728.88 64.91 L 721.88 68.41 L 723.63 64.91 L 721.88 61.41 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
119 |         <g transform="translate(-0.5 -0.5)">
120 |             <switch>
121 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
122 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 65px; margin-left: 588px;">
123 |                         <div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
124 |                             <div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;">
125 |                                 画像なしの場合
126 |                             </div>
127 |                         </div>
128 |                     </div>
129 |                 </foreignObject>
130 |                 <text x="588" y="68" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="11px" text-anchor="middle">
131 |                     画像なしの場合
132 |                 </text>
133 |             </switch>
134 |         </g>
135 |         <path d="M 406 24.87 L 446 64.87 L 406 104.87 L 366 64.87 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
136 |         <g transform="translate(-0.5 -0.5)">
137 |             <switch>
138 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
139 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 78px; height: 1px; padding-top: 65px; margin-left: 367px;">
140 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
141 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
142 |                                 <font style="font-size: 12px;">
143 |                                     ドキュメント
144 |                                     <br/>
145 |                                     ・言語種別
146 |                                 </font>
147 |                             </div>
148 |                         </div>
149 |                     </div>
150 |                 </foreignObject>
151 |                 <text x="406" y="68" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
152 |                     ドキュメント
153 | ・言語種別
154 |                 </text>
155 |             </switch>
156 |         </g>
157 |         <path d="M 650 164.17 L 790 164.17 Q 800 164.17 800 154.17 L 800 136.24" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
158 |         <path d="M 800 130.99 L 803.5 137.99 L 800 136.24 L 796.5 137.99 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
159 |         <rect x="550" y="145" width="100" height="38.25" fill="#dae8fc" stroke="#6c8ebf" pointer-events="all"/>
160 |         <g transform="translate(-0.5 -0.5)">
161 |             <switch>
162 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
163 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 98px; height: 1px; padding-top: 152px; margin-left: 551px;">
164 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
165 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
166 |                                 データ
167 |                                 <br/>
168 |                                 読み込み
169 |                             </div>
170 |                         </div>
171 |                     </div>
172 |                 </foreignObject>
173 |                 <text x="600" y="164" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
174 |                     データ
175 | 読み込み
176 |                 </text>
177 |             </switch>
178 |         </g>
179 |         <path d="M 0 194.19 L 140 194.19 L 140 244.48 Q 105 234.42 70 244.48 Q 35 254.54 0 244.48 L 0 199.78 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
180 |         <path d="M 140 224 L 490 224 Q 500 224 500 214 L 500 174.08 Q 500 164.08 510 164.09 L 543.63 164.12" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
181 |         <path d="M 548.88 164.12 L 541.88 167.62 L 543.63 164.12 L 541.88 160.62 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
182 |         <rect x="6.19" y="202.13" width="130" height="40" fill="none" stroke="none" pointer-events="all"/>
183 |         <g transform="translate(-0.5 -0.5)">
184 |             <switch>
185 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
186 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 209px; margin-left: 7px;">
187 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
188 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
189 |                                 ドキュメント
190 |                                 <br/>
191 |                                 コンテキスト
192 |                             </div>
193 |                         </div>
194 |                     </div>
195 |                 </foreignObject>
196 |                 <text x="71" y="221" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
197 |                     ドキュメント
198 | コンテキスト
199 |                 </text>
200 |             </switch>
201 |         </g>
202 |         <rect x="914" y="14.62" width="100" height="38.25" fill="#dae8fc" stroke="#6c8ebf" pointer-events="all"/>
203 |         <g transform="translate(-0.5 -0.5)">
204 |             <switch>
205 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
206 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 98px; height: 1px; padding-top: 22px; margin-left: 915px;">
207 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
208 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
209 |                                 MLLM処理
210 |                             </div>
211 |                         </div>
212 |                     </div>
213 |                 </foreignObject>
214 |                 <text x="964" y="34" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
215 |                     MLLM処理
216 |                 </text>
217 |             </switch>
218 |         </g>
219 |         <rect x="914" y="77.37" width="100" height="38.25" fill="#fff2cc" stroke="#d6b656" pointer-events="all"/>
220 |         <g transform="translate(-0.5 -0.5)">
221 |             <switch>
222 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
223 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 98px; height: 1px; padding-top: 84px; margin-left: 915px;">
224 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
225 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
226 |                                 LLM処理
227 |                             </div>
228 |                         </div>
229 |                     </div>
230 |                 </foreignObject>
231 |                 <text x="964" y="96" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
232 |                     LLM処理
233 |                 </text>
234 |             </switch>
235 |         </g>
236 |         <path d="M 852.38 225.83 L 866.67 225.83 Q 876.67 225.83 885.65 225.52 L 894.64 225.21" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
237 |         <path d="M 899.88 225.03 L 893.01 228.77 L 894.64 225.21 L 892.77 221.77 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
238 |         <rect x="752.38" y="206.74" width="100" height="38.25" fill="#fff2cc" stroke="#d6b656" pointer-events="all"/>
239 |         <g transform="translate(-0.5 -0.5)">
240 |             <switch>
241 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
242 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 98px; height: 1px; padding-top: 214px; margin-left: 753px;">
243 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
244 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
245 |                                 コンテキスト
246 |                                 <br/>
247 |                                 更新
248 |                             </div>
249 |                         </div>
250 |                     </div>
251 |                 </foreignObject>
252 |                 <text x="802" y="226" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
253 |                     コンテキスト
254 | 更新
255 |                 </text>
256 |             </switch>
257 |         </g>
258 |         <path d="M 730 17.87 L 870 17.87 L 870 118.67 Q 835 98.51 800 118.67 Q 765 138.83 730 118.67 L 730 29.07 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
259 |         <rect x="750" y="49.75" width="102.38" height="20" rx="3" ry="3" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
260 |         <g transform="translate(-0.5 -0.5)">
261 |             <switch>
262 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
263 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 100px; height: 1px; padding-top: 60px; margin-left: 751px;">
264 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
265 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
266 |                                 テキスト
267 |                             </div>
268 |                         </div>
269 |                     </div>
270 |                 </foreignObject>
271 |                 <text x="801" y="63" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
272 |                     テキスト
273 |                 </text>
274 |             </switch>
275 |         </g>
276 |         <rect x="736.19" y="22.94" width="130" height="40" fill="none" stroke="none" pointer-events="all"/>
277 |         <g transform="translate(-0.5 -0.5)">
278 |             <switch>
279 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
280 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 30px; margin-left: 737px;">
281 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
282 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
283 |                                 <span style="font-family: Helvetica; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;">
284 |                                     出力
285 |                                 </span>
286 |                             </div>
287 |                         </div>
288 |                     </div>
289 |                 </foreignObject>
290 |                 <text x="801" y="42" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
291 |                     出力
292 |                 </text>
293 |             </switch>
294 |         </g>
295 |         <path d="M 901 197.05 L 1041 197.05 L 1041 247.34 Q 1006 237.28 971 247.34 Q 936 257.4 901 247.34 L 901 202.64 Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
296 |         <rect x="907.19" y="204.99" width="130" height="40" fill="none" stroke="none" pointer-events="all"/>
297 |         <g transform="translate(-0.5 -0.5)">
298 |             <switch>
299 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
300 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 212px; margin-left: 908px;">
301 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
302 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
303 |                                 ドキュメント
304 |                                 <br/>
305 |                                 コンテキスト
306 |                             </div>
307 |                         </div>
308 |                     </div>
309 |                 </foreignObject>
310 |                 <text x="972" y="224" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
311 |                     ドキュメント
312 | コンテキスト
313 |                 </text>
314 |             </switch>
315 |         </g>
316 |         <rect x="748.81" y="75.87" width="102.38" height="20" rx="3" ry="3" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>
317 |         <g transform="translate(-0.5 -0.5)">
318 |             <switch>
319 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
320 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 100px; height: 1px; padding-top: 86px; margin-left: 750px;">
321 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
322 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
323 |                                 トークン数
324 |                             </div>
325 |                         </div>
326 |                     </div>
327 |                 </foreignObject>
328 |                 <text x="800" y="89" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
329 |                     トークン数
330 |                 </text>
331 |             </switch>
332 |         </g>
333 |         <path d="M 140 225 L 746.01 225.86" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
334 |         <path d="M 751.26 225.86 L 744.26 229.35 L 746.01 225.86 L 744.27 222.35 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
335 |         <path d="M 837.1 107.13 L 837.46 199.45" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
336 |         <path d="M 837.48 204.7 L 833.95 197.72 L 837.46 199.45 L 840.95 197.69 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
337 |         <path d="M 972.19 244.99 L 972.19 278.63" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>
338 |         <path d="M 972.19 283.88 L 968.69 276.88 L 972.19 278.63 L 975.69 276.88 Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>
339 |         <rect x="907.19" y="285" width="130" height="22.87" fill="none" stroke="none" pointer-events="all"/>
340 |         <g transform="translate(-0.5 -0.5)">
341 |             <switch>
342 |                 <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">
343 |                     <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe flex-start; justify-content: unsafe center; width: 128px; height: 1px; padding-top: 292px; margin-left: 908px;">
344 |                         <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">
345 |                             <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">
346 |                                 次ページの処理へ
347 |                             </div>
348 |                         </div>
349 |                     </div>
350 |                 </foreignObject>
351 |                 <text x="972" y="304" fill="rgb(0, 0, 0)" font-family="Helvetica" font-size="12px" text-anchor="middle">
352 |                     次ページの処理へ
353 |                 </text>
354 |             </switch>
355 |         </g>
356 |     </g>
357 |     <switch>
358 |         <g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/>
359 |         <a transform="translate(0,-5)" xlink:href="https://www.diagrams.net/doc/faq/svg-export-text-problems" target="_blank">
360 |             <text text-anchor="middle" font-size="10px" x="50%" y="100%">
361 |                 Text is not SVG - cannot display
362 |             </text>
363 |         </a>
364 |     </switch>
365 | </svg>
366 |


--------------------------------------------------------------------------------
/docs/argo.md:
--------------------------------------------------------------------------------
 1 | # アルゴリズム
 2 |
 3 | 本ドキュメントではマルチモーダルLLMを用いたドキュメントのパースについて記述する。
 4 |
 5 | ![image](./argo.drawio.svg)
 6 |
 7 | ## ページ毎にテキストを抽出する
 8 |
 9 | PDFパーサーで抽出したテキストや画像、図表をページ毎にマルチモーダルLLMに入力する。
10 |
11 | ## ドキュメント種別の判別
12 |
13 | ドキュメントのプロパティを取得し、テキストのみの場合は次のページの処理に進む。
14 | 判別に関しては画像を圧縮したうえで、マルチモーダルLLMによる判別を行う。
15 | 各プロパティに即したプロンプトを生成し、マルチモーダルLLMに入力する。
16 |
17 | - 日本語テキスト
18 | - グラフ
19 | - テーブル
20 | - 画像
21 |
22 | プロンプトは以下に従う。
23 |
24 | ```text
25 | Analyze the input image and classify its content according to the following properties.
26 |
27 | - **table**: Select if the image contains a table, such as a grid or matrix displaying structured data.
28 | - **flowchart**: Select if the image contains a flowchart or diagram illustrating a process or sequence of steps.
29 | - **graph**: Select if the image contains a graph, chart, or plot.
30 | - **image**: Select if the image contains any other image except for tables and graphs.
31 | - **ja_text**: Select if the image contains any Japanese text, even if other elements are also present.
32 | - **text**: Select if the image contains any text, even if other elements are also present.
33 |
34 | # Steps
35 |
36 | 1. Analyze the input image to identify all content types present.
37 | 2. For each property(**table**, **flowchart**, **graph**, **image**, **ja_text**, **text**), select all that apply.
38 | ```
39 |
40 | ## コンテキストとメタ情報
41 |
42 | ドキュメントのメタ情報と前ページまでのコンテキストを取得し、マルチモーダルLLMに入力する。
43 | コンテキストはページを読み進めるごとに更新する。
44 |
45 | ```text
46 | Based on the provided context and new information, update the context to include relevant information.
47 |
48 | # Constraints
49 | - List any requirements, prerequisites, or action items extracted from new information, as they may be necessary for further pages.
50 | - New information is provided by user input.
51 | - Maintain the context with 5-7 bullet points.
52 |
53 | # Context
54 |
55 | {context}
56 | ```
57 |
58 | ## ページのテキスト抽出
59 |
60 | コンテキスト情報とページをラフに読み取ったテキストをマルチモーダルLLMに入力する。
61 |
62 | ```text
63 | You are an expert in reading documents from images.
64 | Please write out the content accurately, staying faithful to the given image content.
65 |
66 | # Constraints
67 | - User will input the sentence. Please modify the sentence to make it more accurate.
68 | - Don't hallucinate the content that doesn't exist in the image.
69 | - Document context is provided for reference.
70 | - Transcribe accurately, staying true to the image content and language.
71 |
72 | # Document Type
73 |
74 | ## Text Information
75 | - Please describe the all texts in this documents.
76 |
77 | {document_type_prompt} // ドキュメントの種別に応じたプロンプト
78 |
79 | # Document Context
80 |
81 | {context}
82 | ```
83 |
84 | ## References
85 |
86 | ### マルチモーダルLLM
87 |
88 | - [マルチモーダルLLMとは](https://www.youtube.com/watch?v=nKma3gafkUI)
89 | - [マルチモーダルLLMのプロンプト](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/design-multimodal-prompts?hl=ja)
90 | - [マルチモーダルLLMのプロンプトサーベイ](https://arxiv.org/pdf/2409.19339)
91 |
92 | ### PDFのテキスト抽出
93 |
94 | - [PDFのテキスト抽出(非ページ単位)](https://arxiv.org/pdf/2410.05970)
95 | - [PDFのページ読み込み](https://arxiv.org/pdf/2408.11981)
96 |


--------------------------------------------------------------------------------
/docs/changelog.md:
--------------------------------------------------------------------------------
 1 | # Changelog
 2 |
 3 | 本ファイルでは、リリースや更新内容を時系列で管理します。
 4 |
 5 | ## [0.0.0] - 2025-01-19
 6 |
 7 | - 初回リリース
 8 | - 機能Aを追加
 9 | - ドキュメントの整備
10 |


--------------------------------------------------------------------------------
/docs/contributing.md:
--------------------------------------------------------------------------------
 1 | # コントリビューションガイド
 2 |
 3 | このプロジェクトへのご関心ありがとうございます。本ガイドでは、どのようにプロジェクトへ貢献できるかを説明します。
 4 |
 5 | ## コントリビューションの方法
 6 |
 7 | 1. **リポジトリをフォークする**
 8 |    コントリビューションの作業はご自身のフォークから始めます。
 9 |    [環境構築](#環境構築) を参考にして、ローカル環境をセットアップしてください。
10 | 2. **作業用ブランチを作成する**
11 |    機能追加やバグ修正ごとに、わかりやすい名前のブランチを作成してください。
12 |    例: `feature/add-new-module` や `fix/typo-in-docs` など。  [ブランチ戦略](#ブランチ戦略) を参考にしてください。
13 | 3. **変更をコミットする**
14 |    変更内容を明確にするコミットメッセージを心がけてください。
15 |    コードスタイルやテストを[pre-commit](コードスタイル) により自動でチェックされます。
16 | 4. **Pull Request を送る**
17 |    変更が完了したら、メインリポジトリへ Pull Request を作成してください。
18 |    タイトルや説明文に変更内容の要約を含めてください。
19 |    レビューアーは指摘箇所があればコメントしますので、適宜対応の上、修正コミットを行ってください。
20 |
21 | ## 環境構築
22 |
23 | 以下で依存ライブラリをインストールします。`uv` コマンドを使用していますので、事前にインストールしてください。
24 |
25 | ```bash
26 | uv sync --all-groups
27 | ```
28 |
29 | 結合テストや評価を行う場合は、`.env.sample`から`.env`を作成し、環境変数を設定してください。
30 | `LangFuse`を利用する場合は該当の`Publick/Secret Key`と`Host`を設定してください。
31 |
32 | ## ブランチ戦略
33 |
34 | - `feature/xxx`：新機能の追加
35 | - `fix/xxx`：バグ修正
36 | - `hotfix/xxx`：緊急のバグ修正
37 | - `docs/xxx`：ドキュメント修正
38 |
39 | `main` ブランチへのタグ付けによりリリースを行います。
40 |
41 | ## コードスタイル
42 |
43 | コードスタイルや品質を保つために pre-commit フックを使用しています。以下の手順でセットアップしてください。
44 |
45 | 1. **pre-commit のインストール**
46 |     プロジェクトのルートディレクトリで以下のコマンドを実行します。
47 |
48 |     ```bash
49 |     uv run pre-commit install
50 |     ```
51 |
52 | 2. **設定ファイルの確認**
53 |     `.pre-commit-config.yaml` ファイルに定義されたフックが実行されます。必要に応じて設定を確認・変更してください。
54 |
55 | 3. **コミット時のチェック**
56 |     コミット時に自動的にフックが実行され、コードスタイルやリンターのルールが適用されます。問題がある場合は修正して再度コミットしてください。
57 |
58 | ## 結合テスト
59 |
60 | 結合テストを行う場合は、以下のコマンドを実行してください。
61 |
62 | ```bash
63 | uv run pytest tests/integrate
64 | ```
65 |
66 | ## 評価
67 |
68 | 評価を行う場合は、以下のコマンドを実行してください。
69 |
70 | ```bash
71 | uv run eval
72 | ```
73 |
74 | ## Issue の作成
75 |
76 | - バグを見つけた場合や新機能の提案を行う場合は Issue を作成してください。
77 | - タイトルや詳細な再現手順、期待する結果などをできるだけ明確に書いてください。
78 |
79 | ## その他
80 |
81 | - 大きな改変やアーキテクチャに関わる変更は、事前に Issue で相談してから実装を進めることを推奨します。
82 | - 貢献者同士、互いにリスペクトを持ち、コミュニケーションを取り合いましょう。
83 |
84 | 以上のプロセスを守っていただくことで、スムーズにコラボレーションできます。ご協力ありがとうございます！
85 |


--------------------------------------------------------------------------------
/docs/eval-dataset.md:
--------------------------------------------------------------------------------
 1 | # データセット
 2 |
 3 | ## ドキュメントデータセット
 4 |
 5 | データセットは以下の属性を持つデータ群(PDFファイル)を用います。
 6 |
 7 | |属性|詳細|
 8 | |---|---|
 9 | |グラフ|棒グラフ、円グラフ、折れ線グラフ|
10 | |フローチャート|手順書、アルゴリズム説明書|
11 | |テーブル|単純テーブル、結合テーブル|
12 | |要OCRテキスト|手書きテキスト、非構造テキスト、スクリーンショット|
13 |
14 | ## 質問データセット
15 |
16 | [ドキュメントデータセット](#ドキュメントデータセット)に対して、質問と正回答を用意します。
17 | 質問内容は一問一答&クローズド形式とし、一つのデータセットにつき複数の質問を用意します。
18 |
19 | ```text
20 | ex.
21 | Q. フローチャートにおけるAからBへの矢印の意味は？ A. APIリクエスト
22 |
23 | ex.
24 | Q. テーブルの中でも最も身長が高い人物は？ A. Aさん
25 | ```
26 |


--------------------------------------------------------------------------------
/docs/eval-method.md:
--------------------------------------------------------------------------------
 1 | # 評価方法
 2 |
 3 | [評価レポジトリ](https://github.com/InsightEdgeJP/parse-docs-eval)により、以下の方法で評価を行います。
 4 |
 5 | 0. API利用量を削減するために各種処理はローカルストレイジにキャッシュします。
 6 | 1. ライブラリの出力をコンテキストとして、評価データセットの質問を投げます。
 7 | 2. 回答を取得し、正回答と比較し、正当かどうかを100点満点で判定します。
 8 |
 9 | ```mermaid
10 | graph LR
11 |     A[ライブラリ出力] --コンテキスト--> B(LLMによる回答)
12 |     C[質問]　--> B
13 |     B --回答--> D[回答]
14 |     D --比較--> F
15 |     E[正回答] --> F(LLMによる評価)
16 |     F --> G[評価結果]
17 | ```
18 |
19 | `LLMによる回答` は、以下のプロンプトで回答します。
20 |
21 | ```text
22 | You are a helpful assistant.
23 | Please respond to the query using the provided Context.
24 | If the query contains information not included in the Context, reply with "I don’t know".
25 |
26 | ## Output
27 | Please follow the JSON format below for the output.
28 |
29 | "answer": str
30 |
31 | ## Context
32 | {context}
33 | ```
34 |
35 | `LLMによる評価` は、以下のプロンプトで判定します。
36 |
37 | ```text
38 | You are an excellent evaluator.
39 | Please grade the user’s responses to the following questions on a scale of 0 to 100 points.
40 | Provide only the score.
41 |
42 | ## Output
43 | Please follow the JSON format below for the output.
44 |
45 | "rank": int
46 |
47 | ## Query
48 | {query}
49 |
50 | ## Expected:
51 | {expected}
52 | ```
53 |
54 | ## ベンチマーク対象
55 |
56 | 以下をベンチマーク対象とします。
57 |
58 | - [Azure Document Intelligence](https://learn.microsoft.com/ja-jp/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0)
59 | - [pymupdf4llm](https://github.com/pymupdf/RAG/tree/main)
60 | - [docling](https://github.com/DS4SD/docling/tree/main)
61 |


--------------------------------------------------------------------------------
/docs/eval-result.md:
--------------------------------------------------------------------------------
1 | # 📈 Result
2 |
3 | 下図は最新のバージョンの評価結果を表しています。
4 |
5 | ![summary](eval-summary.png)
6 |


--------------------------------------------------------------------------------
/docs/eval-summary.png:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:ec5072dc0b1331324477000014775914cb907b7f17a8f2885962452dc7edc169
3 | size 45608
4 |


--------------------------------------------------------------------------------
/docs/index.md:
--------------------------------------------------------------------------------
  1 | # Parse Doc Library
  2 |
  3 | ![python](https://img.shields.io/badge/python-%20%203.10%20|%203.11%20|%203.12-blue)
  4 |
  5 | 本ライブラリは、画像を含むドキュメントのパースを行うためのライブラリです。
  6 | テキストとして出力することで、従来のベクトル検索や全文検索での利用を可能することを目的とします。
  7 |
  8 | ## 📝 ドキュメントのパース
  9 |
 10 | ### Background
 11 |
 12 | - 多くのドキュメントには、グラフや画像のような非テキストが含まれる
 13 | - これらのドキュメントをRAGのような検索システムに組み込むためには、テキストドメインに変更する必要がある(画像やテキストを同一のベクトルにする技術はまだ有効ではない)
 14 | - MLLMの進展に伴い実装が容易化したものの、まだ各案件で真剣に取り組みには工数がかかる部分ではある
 15 |
 16 | ### Goal
 17 |
 18 | 1. ドキュメントの全文抽出を行うツールを提供
 19 | 2. ツールの評価を行い、継続的に改善するためのCI/CDを構築
 20 | 3. ツールを簡単に導入できるように構築
 21 | 4. 実行時のAPIコストの算出
 22 |
 23 | ![architecture](./architecture.drawio.svg)
 24 |
 25 | ## 📑 対応ファイル
 26 |
 27 | | コンテンツタイプ | 拡張子 |
 28 | |-----------------|--------|
 29 | | **📑 ドキュメント**  | PDF, PowerPoint |
 30 | | **🖼️ 画像**        | JPEG, PNG, BMP |
 31 | | **📝 テキストデータ** | テキストファイル, Markdown |
 32 | | **📊 表データ**     | Excel, CSV |
 33 |
 34 | ## 🔥 LLM
 35 |
 36 | |クラウドベンダー|モデル|
 37 | |-|-|
 38 | |Azure|GPT|
 39 | |Google Cloud|Claude, Gemini|
 40 |
 41 | ## 📥 インストール方法
 42 |
 43 | ### LibreOffice
 44 |
 45 | Officeファイルをテキストに変換するために、LibreOfficeをインストールします。
 46 |
 47 | ```bash
 48 | # Ubuntu
 49 | sudo apt install libreoffice
 50 |
 51 | # Mac
 52 | brew install --cask libreoffice
 53 | ```
 54 |
 55 | ### ライブラリのインストール
 56 |
 57 | ```bash
 58 | pip install exparso
 59 | ```
 60 |
 61 | ## 💡 使用方法
 62 |
 63 | `parse_document` 関数を利用して、ドキュメントをパースします。
 64 |
 65 | ```python
 66 | from exparso import parse_document
 67 |
 68 | # For AzureChatOpenAI
 69 | from langchain_openai import AzureChatOpenAI
 70 | import getpass
 71 | import os
 72 | if "AZURE_OPENAI_API_KEY" not in os.environ:
 73 |     os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
 74 |         "Enter your AzureOpenAI API key: "
 75 |     )
 76 | os.environ["AZURE_OPENAI_ENDPOINT"] = "https://YOUR-ENDPOINT.openai.azure.com/"
 77 | llm_model = AzureChatOpenAI(model="gpt-4o")
 78 |
 79 | # For GoogleChatOpenAI
 80 | import vertexai
 81 | from langchain_google_vertexai import ChatVertexAI
 82 | vertexai.init(project="YOUR_PROJECT", location="us-central1") # Default の認証情報を利用
 83 | llm = ChatVertexAI(model_name="gemini-1.5-pro-002")
 84 |
 85 | text = parse_document(
 86 |       path="path/to/document.pdf",
 87 |       model=llm_model,
 88 |       context="このドキュメントは..."
 89 | )
 90 | ```
 91 |
 92 | `model`は`LangChain`の`BaseChatModel`を継承したクラスで、各LLMベンダーに合わせて、認証情報を設定してください。
 93 |
 94 | - [AzureChatOpenAI](https://python.langchain.com/docs/integrations/chat/azure_chat_openai/)
 95 | - [ChatVertexAI](https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/)
 96 |
 97 | #### プロンプトのカスタマイズ
 98 |
 99 | [プロンプトのカスタマイズ](prompts.md)を参照ください。
100 |
101 | ### アウトプット
102 |
103 | `Document`クラスのインスタンスが返されます。`Document`のプロパティは以下になります。
104 |
105 | ```mermaid
106 | classDiagram
107 |     class Document {
108 |         +list<PageContents> contents
109 |         +Cost cost
110 |     }
111 |
112 |     class PageContents {
113 |         +str contents
114 |         +int page_number
115 |     }
116 |
117 |     class Cost {
118 |         +int input_token
119 |         +int output_token
120 |         +str llm_model_name
121 |     }
122 |
123 |     Document --> PageContents : has
124 |     Document --> Cost : has
125 | ```
126 |


--------------------------------------------------------------------------------
/docs/prompts.md:
--------------------------------------------------------------------------------
  1 | # 🔧 プロンプトのカスタマイズ
  2 |
  3 | ## 📝 `CorePrompt`クラスの概要
  4 |
  5 | `exparso/core/prompt/prompt.py`に定義されている`CorePrompt`クラスは、ドキュメント処理のための様々なプロンプトを管理します。このクラスを使用することで、ライブラリの動作をカスタマイズし、特定のユースケースに合わせたプロンプトを注入することができます。
  6 |
  7 | ## 🚀 `CorePrompt`の使用方法
  8 |
  9 | ### 基本的な使用例
 10 |
 11 | `CorePrompt`クラスをライブラリのエントリーポイントとして使用するには、以下の手順に従います：
 12 |
 13 | ```python
 14 | from exparso import parse_document
 15 | from exparso.core.prompt.prompt import CorePrompt
 16 | from langchain_openai import AzureChatOpenAI
 17 |
 18 | # カスタムプロンプトの定義
 19 | custom_prompts = CorePrompt(
 20 |     judge_document_type="ドキュメントタイプを判定してください: {types_explanation} {format_instructions}",
 21 |     extract_document="内容を抽出してください: {document_type_prompt} {context} {format_instruction}",
 22 |     update_context="コンテキストを更新してください: {context} {format_instructions}",
 23 |     table_prompt="テーブルデータを抽出してください。",
 24 |     flowchart_prompt="フローチャートデータを抽出してください。",
 25 |     graph_prompt="グラフデータを抽出してください。",
 26 |     image_prompt="画像データを抽出してください。",
 27 |     extract_document_text_prompt="テキストを抽出してください: {document_text}",
 28 |     extract_image_only_prompt="画像からテキストを抽出してください: {document_text}"
 29 | )
 30 |
 31 | # LLMモデルの設定
 32 | llm_model = AzureChatOpenAI(model="gpt-4o")
 33 |
 34 | # カスタムプロンプトを使用してドキュメントをパース
 35 | text = parse_document(
 36 |     path="path/to/document.pdf",
 37 |     model=llm_model,
 38 |     context="このドキュメントは...",
 39 |     prompt=custom_prompts
 40 | )
 41 | ```
 42 |
 43 | ## 📋 プロンプトの種類と役割
 44 |
 45 | `CorePrompt`クラスの各フィールドは、ライブラリの特定の機能に対応しています：
 46 |
 47 | | プロンプト名 | 役割 | 必須プレースホルダー |
 48 | |------------|------|-------------------|
 49 | | `judge_document_type` | ドキュメントタイプの判定 | `{types_explanation}`, `{format_instructions}` |
 50 | | `extract_document` | ドキュメント内容の抽出 | `{document_type_prompt}`, `{context}`, `{format_instruction}` |
 51 | | `update_context` | コンテキスト情報の更新 | `{context}`, `{format_instructions}` |
 52 | | `table_prompt` | テーブルデータの抽出 | なし |
 53 | | `flowchart_prompt` | フローチャートデータの抽出 | なし |
 54 | | `graph_prompt` | グラフデータの抽出 | なし |
 55 | | `image_prompt` | 画像データの抽出 | なし |
 56 | | `extract_document_text_prompt` | ドキュメントからのテキスト抽出 | `{document_text}` |
 57 | | `extract_image_only_prompt` | 画像からのテキスト抽出 | `{document_text}` |
 58 |
 59 | ## 🔍 ユースケース別の例
 60 |
 61 | ### 📊 業界特化型プロンプト（医療分野の例）
 62 |
 63 | ```python
 64 | from exparso import parse_document
 65 | from exparso.core.prompt.prompt import CorePrompt
 66 | from langchain_openai import AzureChatOpenAI
 67 |
 68 | # 医療分野向けカスタムプロンプト
 69 | medical_prompts = CorePrompt(
 70 |     judge_document_type="この医療文書のタイプを判定してください: {types_explanation} {format_instructions}",
 71 |     extract_document="この医療文書から臨床情報を抽出してください: {document_type_prompt} 患者情報: {context} {format_instruction}",
 72 |     update_context="患者の医療記録を更新してください: {context} {format_instructions}",
 73 |     table_prompt="この検査結果表から異常値を特定してください。",
 74 |     image_prompt="この医療画像から所見を詳細に説明してください。",
 75 |     # 他のフィールドはデフォルト値を使用
 76 | )
 77 |
 78 | llm_model = AzureChatOpenAI(model="gpt-4o")
 79 |
 80 | # 医療文書の解析
 81 | text = parse_document(
 82 |     path="path/to/medical_report.pdf",
 83 |     model=llm_model,
 84 |     context="患者ID: 12345, 年齢: 45歳, 既往歴: 高血圧",
 85 |     prompt=medical_prompts
 86 | )
 87 | ```
 88 |
 89 | ### 🌐 多言語対応プロンプト
 90 |
 91 | ```python
 92 | from exparso import parse_document
 93 | from exparso.core.prompt.prompt import CorePrompt
 94 | from langchain_google_vertexai import ChatVertexAI
 95 |
 96 | # 言語に応じたプロンプトを取得する関数
 97 | def get_language_prompt(language="ja"):
 98 |     if language == "en":
 99 |         return CorePrompt(
100 |             judge_document_type="Please determine the document type: {types_explanation} {format_instructions}",
101 |             extract_document="Please extract content from this document: {document_type_prompt} Context: {context} {format_instruction}",
102 |             # 他のフィールドは省略
103 |         )
104 |     else:  # デフォルトは日本語
105 |         return CorePrompt(
106 |             judge_document_type="ドキュメントタイプを判定してください: {types_explanation} {format_instructions}",
107 |             extract_document="内容を抽出してください: {document_type_prompt} コンテキスト: {context} {format_instruction}",
108 |             # 他のフィールドは省略
109 |         )
110 |
111 | # 英語ドキュメント用のプロンプトを取得
112 | english_prompt = get_language_prompt("en")
113 |
114 | # LLMモデルの設定
115 | llm_model = ChatVertexAI(model_name="gemini-1.5-pro-002")
116 |
117 | # 英語ドキュメントの解析
118 | text = parse_document(
119 |     path="path/to/english_document.pdf",
120 |     model=llm_model,
121 |     context="This document is about...",
122 |     prompt=english_prompt
123 | )
124 | ```
125 |
126 | ## ⚠️ 注意事項
127 |
128 | 1. すべての必須プレースホルダーが含まれていることを確認してください
129 | 2. 複雑なプロンプトは事前にテストして期待通りの結果が得られることを確認してください


--------------------------------------------------------------------------------
/eval/__main__.py:
--------------------------------------------------------------------------------
 1 | import pandas as pd
 2 | from langchain_core.language_models.chat_models import BaseChatModel
 3 | from tqdm import tqdm
 4 |
 5 | from eval.impl import (
 6 |     AzureDocumentIntelligence,
 7 |     CacheRepository,
 8 |     Docling,
 9 |     Exparso,
10 |     GCSHelper,
11 |     Pymupdf4llm,
12 |     create_llm,
13 |     plot_drift,
14 |     plot_latest_df,
15 | )
16 | from eval.models import Parser, QueryModel
17 | from eval.settings import load_setting_xlsx, settings
18 | from eval.usecase import Evaluator
19 |
20 |
21 | def run_eval(queries: list[QueryModel], models: list[Parser], llm: BaseChatModel) -> pd.DataFrame:
22 |     pattern: list[tuple[Parser, QueryModel]] = [(m, q) for m in models for q in queries]
23 |     df = pd.DataFrame(columns=["model", "file_id", "query", "expected", "answer", "rank"])
24 |     repository = CacheRepository()
25 |     for m, q in tqdm(pattern, desc="Evaluating queries"):
26 |         eval_data = Evaluator(parser=m, query=q, repository=repository).eval(llm)
27 |         new_df = pd.DataFrame([{**eval_data.model_dump()}])
28 |         df = pd.concat([df, new_df], ignore_index=True)
29 |
30 |     return df
31 |
32 |
33 | def history(gcs_helper: GCSHelper, result_prefix: str) -> pd.DataFrame:
34 |     history_data = gcs_helper.get_blob_list(result_prefix)
35 |     history_dfs = [
36 |         gcs_helper.download_blob_to_df(blob_name).assign(
37 |             datetime=pd.to_datetime(blob_name.split(".")[0].split("_")[-1])
38 |         )
39 |         for blob_name in history_data
40 |     ]
41 |     df = pd.concat(history_dfs, ignore_index=True)
42 |     return df
43 |
44 |
45 | if __name__ == "__main__":
46 |     import argparse
47 |
48 |     parser = argparse.ArgumentParser(description="Run the evaluation")
49 |     parser.add_argument("--benchmark", help="Benchmark", action="store_true")
50 |     parser.add_argument("--save-gcs", help="Save gcs result", action="store_true")
51 |
52 |     args = parser.parse_args()
53 |
54 |     print("Loading setting...")
55 |     queries = load_setting_xlsx()
56 |
57 |     llm = create_llm()
58 |     parse_lib = Exparso(model=llm, model_name="gemini-1.5-pro-002")
59 |
60 |     gcs_helper = GCSHelper(bucket_name=settings.gcs_bucket)
61 |
62 |     if args.benchmark:
63 |         models = [Pymupdf4llm(), AzureDocumentIntelligence(), Docling()]
64 |         df = run_eval(queries=queries, models=models, llm=llm)
65 |         gcs_helper.upload_df_to_blob(df=df, blob_name=settings.benchmark_blob_name)
66 |
67 |     benchmark_df = gcs_helper.download_blob_to_df(settings.benchmark_blob_name)
68 |     df = run_eval(queries=queries, models=[parse_lib], llm=llm)
69 |
70 |     df = pd.concat([benchmark_df, df], ignore_index=True)
71 |     df.to_excel(settings.result_excel_path, index=False)
72 |
73 |     plot_latest_df(df, settings.result_latest_plot_path)
74 |
75 |     if args.save_gcs:
76 |         df = pd.read_excel(settings.result_excel_path)
77 |         gcs_helper.upload_df_to_blob(df=df, blob_name=settings.result_blob_name)
78 |         gcs_helper.upload_file_to_blob(settings.result_latest_plot_path, settings.result_latest_plot_blob)
79 |
80 |         df = history(gcs_helper, settings.result_blob_prefix)
81 |         drift = plot_drift(df, settings.result_drift_plot_path)
82 |         gcs_helper.upload_file_to_blob(settings.result_drift_plot_path, settings.result_drift_plot_blob)
83 |


--------------------------------------------------------------------------------
/eval/impl/__init__.py:
--------------------------------------------------------------------------------
 1 | from eval.impl.cache_repository import CacheRepository
 2 | from eval.impl.figure import plot_drift, plot_latest_df
 3 | from eval.impl.gcs_helper import GCSHelper
 4 | from eval.impl.llm import create_llm
 5 | from eval.impl.parser import AzureDocumentIntelligence, Docling, Exparso, Pymupdf4llm
 6 |
 7 | __all__ = [
 8 |     "plot_drift",
 9 |     "plot_latest_df",
10 |     "CacheRepository",
11 |     "AzureDocumentIntelligence",
12 |     "Docling",
13 |     "Exparso",
14 |     "Pymupdf4llm",
15 |     "create_llm",
16 |     "GCSHelper",
17 | ]
18 |


--------------------------------------------------------------------------------
/eval/impl/cache_repository.py:
--------------------------------------------------------------------------------
 1 | import os
 2 | from logging import getLogger
 3 |
 4 | from eval.models import ParseDataModel, Repository
 5 |
 6 | logger = getLogger(__name__)
 7 |
 8 |
 9 | class CacheRepository(Repository):
10 |     cache_dir = ".cache"
11 |
12 |     def __init__(self):
13 |         os.makedirs(self.cache_dir, exist_ok=True)
14 |
15 |     def get(self, id: str) -> ParseDataModel | None:
16 |         file_path = os.path.join(self.cache_dir, f"{id}.json")
17 |         if os.path.exists(file_path):
18 |             with open(file_path, "r") as f:
19 |                 logger.info(f"Load cache: {file_path}")
20 |                 return ParseDataModel.model_validate_json(f.read())
21 |         return None
22 |
23 |     def set(self, id: str, data: ParseDataModel):
24 |         file_path = os.path.join(self.cache_dir, f"{id}.json")
25 |         with open(file_path, "w") as f:
26 |             logger.info(f"Save cache: {file_path}")
27 |             f.write(data.model_dump_json())
28 |


--------------------------------------------------------------------------------
/eval/impl/figure.py:
--------------------------------------------------------------------------------
 1 | import itertools
 2 |
 3 | import numpy as np
 4 | import pandas as pd
 5 | from matplotlib import pyplot as plt
 6 |
 7 |
 8 | def plot_drift(df: pd.DataFrame, output_path: str):
 9 |     df = df.assign(model=df["model"].str.split("@").str[0].replace("azure-document-intelligence", "azure DI"))
10 |
11 |     # ファイル名よりカテゴリの作成、rankが50以上の時correct=1, それ以外は0
12 |     df = (
13 |         df.assign(category=df["file_id"].str.split("_").str[0])
14 |         .assign(item=1)
15 |         .assign(correct=(df["rank"] >= 50).astype(int))
16 |     ).drop(columns=["file_id", "query", "expected", "answer", "rank"])
17 |     # カテゴリごとにスコアを足し算
18 |     df = df.groupby(["category", "model", "datetime"]).sum().reset_index()
19 |
20 |     num_categories = len(df["category"].unique())
21 |
22 |     plt.figure(figsize=(20, 10))
23 |     cols = 2
24 |     rows = num_categories // cols + (num_categories % cols > 0)
25 |     linestyles = ["-", "--", "-.", ":"]
26 |     markers = ["o", "s", "D", "^", "v", "P", "X"]
27 |     linestyle_cycle = itertools.cycle(linestyles)
28 |     marker_cycle = itertools.cycle(markers)
29 |     for i, category in enumerate(df["category"].unique()):
30 |         ax = plt.subplot(rows, cols, i + 1)
31 |         df_category = df[df["category"] == category]
32 |         ax.set_title(category + f"(max score:{df_category['item'].max()})")
33 |         models = df_category["model"].unique()
34 |         for model in models:
35 |             marker = next(marker_cycle)
36 |             linestyle = next(linestyle_cycle)
37 |             ax.plot(
38 |                 df_category[df_category["model"] == model]["datetime"],
39 |                 df_category[df_category["model"] == model]["correct"],
40 |                 label=model,
41 |                 marker=marker,
42 |                 linestyle=linestyle,
43 |                 linewidth=1,
44 |             )
45 |             ax.set_ylim(0, df_category["item"].max() * 1.2)
46 |
47 |         ax.legend()
48 |         ax.set_xlabel("datetime")
49 |         ax.set_ylabel("score")
50 |
51 |         ax.grid()
52 |
53 |     plt.savefig(output_path)
54 |
55 |
56 | def plot_latest_df(df: pd.DataFrame, output_path: str):
57 |     # ファイル名よりカテゴリの作成、rankが50以上の時correct=1, それ以外は0
58 |     df = (
59 |         df.assign(category=df["file_id"].str.split("_").str[0])
60 |         .assign(item=1)
61 |         .assign(correct=(df["rank"] >= 50).astype(int))
62 |     ).drop(columns=["file_id", "query", "expected", "answer", "rank"])
63 |     # カテゴリごとにスコアを足し算
64 |     df = df.groupby(["category", "model"]).sum().reset_index()
65 |
66 |     plt.figure(figsize=(15, 10))
67 |     models = [m.replace("-", "\n") for m in df["model"].unique()]
68 |     categories = df["category"].unique()
69 |
70 |     x_ticks = np.array(range(len(models)))
71 |     total_width = 0.8
72 |     colors = ["b", "g", "r", "c", "m", "y", "k"]
73 |     for i, category in enumerate(categories):
74 |         ax = plt.subplot(2, 2, i + 1)
75 |         df_category = df[df["category"] == category]
76 |         ax.bar(
77 |             x_ticks,
78 |             df_category["correct"] / df_category["item"] * 100,
79 |             label=category,
80 |             width=total_width,
81 |             color=colors,
82 |         )
83 |         ax.set_title(category)
84 |         ax.grid()
85 |         ax.set_ylim(0, 100)
86 |         ax.set_ylabel("correct rate [%]")
87 |         ax.set_xticks(x_ticks, models)
88 |
89 |     plt.savefig(output_path)
90 |


--------------------------------------------------------------------------------
/eval/impl/gcs_helper.py:
--------------------------------------------------------------------------------
 1 | import io
 2 | import tempfile
 3 |
 4 | import pandas as pd
 5 | from google.cloud import storage
 6 |
 7 |
 8 | class GCSHelper:
 9 |     def __init__(self, bucket_name: str):
10 |         self.storage_client = storage.Client()
11 |         self.bucket = self.storage_client.bucket(bucket_name)
12 |
13 |     def download_blob_to_df(self, source_blob_name: str) -> pd.DataFrame:
14 |         blob = self.bucket.blob(source_blob_name)
15 |         excel_data = io.BytesIO(blob.download_as_bytes())
16 |         return pd.read_excel(excel_data)
17 |
18 |     def upload_file_to_blob(self, path: str, blob_name: str):
19 |         blob = self.bucket.blob(blob_name)
20 |         with open(path, "rb") as f:
21 |             blob.upload_from_file(f)
22 |
23 |     def upload_df_to_blob(self, df: pd.DataFrame, blob_name: str):
24 |         with tempfile.TemporaryDirectory() as temp_dir:
25 |             path = f"{temp_dir}/data.xlsx"
26 |             df.to_excel(path, index=False)
27 |             self.upload_file_to_blob(path, blob_name)
28 |
29 |     def get_blob_list(self, prefix: str) -> list[str]:
30 |         blobs = self.bucket.list_blobs(prefix=prefix)
31 |         return [blob.name for blob in blobs]
32 |


--------------------------------------------------------------------------------
/eval/impl/llm.py:
--------------------------------------------------------------------------------
 1 | import vertexai
 2 | from langchain_core.language_models.chat_models import BaseChatModel
 3 | from langchain_google_vertexai import ChatVertexAI
 4 |
 5 | from eval.settings import settings
 6 |
 7 |
 8 | def create_llm() -> BaseChatModel:
 9 |     vertexai.init(project=settings.gcp_project, location="us-central1")
10 |     llm = ChatVertexAI(model_name="gemini-1.5-pro-002")
11 |     return llm
12 |


--------------------------------------------------------------------------------
/eval/impl/parser.py:
--------------------------------------------------------------------------------
 1 | import logging
 2 |
 3 | import pymupdf4llm
 4 | from azure.ai.documentintelligence import DocumentIntelligenceClient
 5 | from azure.ai.documentintelligence.models import DocumentContentFormat
 6 | from azure.identity import DefaultAzureCredential
 7 | from docling.document_converter import DocumentConverter
 8 | from langchain_core.language_models.chat_models import BaseChatModel
 9 | from langfuse.callback import CallbackHandler
10 |
11 | from eval.models import FileModel, ParseDataModel, Parser
12 | from eval.settings import settings
13 | from exparso import parse_document
14 |
15 | logger = logging.getLogger(__name__)
16 |
17 |
18 | class Exparso(Parser):
19 |     def __init__(self, model: BaseChatModel, model_name: str):
20 |         self.llm_model_name = model_name
21 |         self.model = model
22 |
23 |     def parse(self, file: FileModel) -> ParseDataModel:
24 |         if settings.langfuse_host:
25 |             langfuse_handler = CallbackHandler(
26 |                 trace_name=file.id,
27 |                 user_id=self.llm_model_name,
28 |                 public_key=settings.langfuse_public_key,
29 |                 secret_key=settings.langfuse_secret_key,
30 |                 host=settings.langfuse_host,
31 |             )
32 |             config = {"callbacks": [langfuse_handler]}
33 |         else:
34 |             config = None
35 |         docs = parse_document(file.path, self.model, config=config)  # type: ignore
36 |         retval = ParseDataModel(
37 |             file_id=file.id,
38 |             model=self.llm_model_name,
39 |             document=[d.contents for d in docs.contents],
40 |         )
41 |         return retval
42 |
43 |     @property
44 |     def model_name(self) -> str:
45 |         return self.llm_model_name
46 |
47 |
48 | class Pymupdf4llm(Parser):
49 |     def parse(self, file: FileModel) -> ParseDataModel:
50 |         md_text = pymupdf4llm.to_markdown(file.path)
51 |         retval = ParseDataModel(file_id=file.id, model="pymupdf4llm", document=[md_text])
52 |         return retval
53 |
54 |     @property
55 |     def model_name(self) -> str:
56 |         return "pymupdf4llm"
57 |
58 |
59 | class AzureDocumentIntelligence(Parser):
60 |     def parse(self, file: FileModel) -> ParseDataModel:
61 |         credential = DefaultAzureCredential()
62 |         client = DocumentIntelligenceClient(endpoint=settings.azure_document_endpoint, credential=credential)
63 |         with open(file.path, "rb") as f:
64 |             response = client.begin_analyze_document(
65 |                 model_id="prebuilt-layout",
66 |                 body=f,
67 |                 output_content_format=DocumentContentFormat.MARKDOWN,
68 |                 content_type="application/octet-stream",
69 |             )
70 |         result = response.result().content.split("<!-- PageBreak -->")
71 |         retval = ParseDataModel(file_id=file.id, model="azure-document-intelligence", document=result)
72 |         return retval
73 |
74 |     @property
75 |     def model_name(self) -> str:
76 |         return "azure-document-intelligence"
77 |
78 |
79 | class Docling(Parser):
80 |     def parse(self, file: FileModel) -> ParseDataModel:
81 |         converter = DocumentConverter()
82 |         result = converter.convert(file.path)
83 |         md_text = result.document.export_to_markdown()
84 |         retval = ParseDataModel(file_id=file.id, model="docling", document=[md_text])
85 |         return retval
86 |
87 |     @property
88 |     def model_name(self) -> str:
89 |         return "docling"
90 |


--------------------------------------------------------------------------------
/eval/models/__init__.py:
--------------------------------------------------------------------------------
 1 | import hashlib
 2 | from abc import abstractmethod
 3 |
 4 | from pydantic import BaseModel
 5 |
 6 |
 7 | class FileModel(BaseModel):
 8 |     path: str
 9 |     id: str
10 |
11 |
12 | class QueryModel(BaseModel):
13 |     query: str
14 |     expected: str
15 |     page_number: int
16 |     file: FileModel = FileModel(path="", id="")
17 |
18 |     @property
19 |     def query_id(self) -> str:
20 |         return hashlib.md5(self.query.encode()).hexdigest()
21 |
22 |     @property
23 |     def display_file_id(self) -> str:
24 |         return self.file.id.split(".")[0]
25 |
26 |
27 | class EvalDataModel(BaseModel):
28 |     query: str
29 |     expected: str
30 |     answer: str
31 |     rank: int
32 |     file_id: str
33 |     model: str
34 |
35 |
36 | class ParseDataModel(BaseModel):
37 |     file_id: str
38 |     model: str
39 |     document: list[str]
40 |     evals: dict[str, EvalDataModel] = {}
41 |
42 |
43 | class Repository:
44 |     @abstractmethod
45 |     def get(self, id: str) -> ParseDataModel | None:
46 |         pass
47 |
48 |     @abstractmethod
49 |     def set(self, id: str, data: ParseDataModel):
50 |         pass
51 |
52 |
53 | class Parser:
54 |     @abstractmethod
55 |     def parse(self, file: FileModel) -> ParseDataModel:
56 |         pass
57 |
58 |     @property
59 |     @abstractmethod
60 |     def model_name(self) -> str:
61 |         pass
62 |


--------------------------------------------------------------------------------
/eval/settings.py:
--------------------------------------------------------------------------------
 1 | import os
 2 | from datetime import datetime
 3 |
 4 | import pandas as pd
 5 | from pydantic import Field
 6 | from pydantic_settings import BaseSettings, SettingsConfigDict
 7 |
 8 | from eval.models import FileModel, QueryModel
 9 |
10 |
11 | class Settings(BaseSettings):
12 |     model_config: SettingsConfigDict = {
13 |         "env_file": ".env",
14 |         "env_file_encoding": "utf-8",
15 |         "extra": "ignore",
16 |         "case_sensitive": True,
17 |     }
18 |     setting_xlsx_path: str = "eval/data/setting.xlsx"
19 |     eval_data_dir: str = "eval/data"
20 |     result_excel_path: str = "eval/data/result/result.xlsx"
21 |     result_latest_plot_path: str = "eval/data/result/summary.png"
22 |     result_drift_plot_path: str = "eval/data/result/drift.png"
23 |
24 |     # GCS
25 |     gcs_bucket: str = "parse-docs-lib"
26 |     benchmark_blob_name: str = "eval/benchmark.xlsx"
27 |
28 |     environment: str = Field(alias="ENVIRONMENT", default="local")
29 |
30 |     result_drift_plot_blob: str = "eval/result/drift.png"
31 |     result_latest_plot_blob: str = "eval/result/summary.png"
32 |
33 |     result_blob_prefix: str = "eval/result/"
34 |     result_blob_name: str = "eval/result/result_{date}.xlsx".format(date=datetime.now().strftime("%Y%m%d%H%M%S"))
35 |
36 |     gcp_project: str = Field(alias="GCP_PROJECT", default="")
37 |     azure_document_endpoint: str = Field(alias="AZURE_DOCUMENT_ENDPOINT", default="")
38 |
39 |     langfuse_secret_key: str = Field(alias="LANGFUSE_SECRET_KEY", default="")
40 |     langfuse_public_key: str = Field(alias="LANGFUSE_PUBLIC_KEY", default="")
41 |     langfuse_host: str = Field(alias="LANGFUSE_HOST", default="")
42 |
43 |     @property
44 |     def eval_blob_prefix(self) -> str:
45 |         return "eval/image/stage" if self.environment != "main" else "eval/image/main"
46 |
47 |
48 | def load_setting_xlsx() -> list[QueryModel]:
49 |     file_path = settings.setting_xlsx_path
50 |
51 |     query_pd = pd.read_excel(file_path, sheet_name="query")
52 |     queries = [QueryModel(**row) for row in query_pd.to_dict(orient="records")]  # type: ignore
53 |     file_ids: list[str] = [row["file_id"] for row in query_pd.to_dict(orient="records")]
54 |
55 |     for q, f in zip(queries, file_ids):
56 |         q.file = FileModel(path=os.path.join(settings.eval_data_dir, f), id=f)
57 |     return queries
58 |
59 |
60 | settings = Settings()
61 |


--------------------------------------------------------------------------------
/eval/usecase/__init__.py:
--------------------------------------------------------------------------------
1 | from eval.usecase.evaluator import Evaluator
2 |
3 | __all__ = ["Evaluator"]
4 |


--------------------------------------------------------------------------------
/eval/usecase/evaluator.py:
--------------------------------------------------------------------------------
 1 | from logging import getLogger
 2 |
 3 | from langchain.output_parsers import PydanticOutputParser
 4 | from langchain_core.language_models.chat_models import BaseChatModel
 5 | from pydantic import BaseModel
 6 |
 7 | from eval.models import EvalDataModel, Parser, QueryModel, Repository
 8 |
 9 | logger = getLogger(__name__)
10 |
11 |
12 | class Evaluator:
13 |     def __init__(self, parser: Parser, repository: Repository, query: QueryModel):
14 |         self.parser = parser
15 |         self.repository = repository
16 |         self.query = query
17 |         self.parser_id = f"{self.parser.model_name}-{self.query.display_file_id}"
18 |
19 |     def eval(self, llm: BaseChatModel) -> EvalDataModel:
20 |         if result := self.repository.get(self.parser_id):
21 |             if self.query.query_id in result.evals:
22 |                 return result.evals[self.query.query_id]
23 |         else:
24 |             result = self.parser.parse(self.query.file)
25 |             self.repository.set(self.parser_id, result)
26 |
27 |         page_number = self.query.page_number if len(result.document) > self.query.page_number else 0
28 |         try:
29 |             answer, score = evaluation(self.query.query, self.query.expected, result.document[page_number], llm)
30 |         except Exception as e:
31 |             answer = f"Error {e}"
32 |             score = 0
33 |
34 |         eval_data = EvalDataModel(
35 |             query=self.query.query,
36 |             expected=self.query.expected,
37 |             answer=answer,
38 |             rank=score,
39 |             file_id=self.query.display_file_id,
40 |             model=self.parser.model_name,
41 |         )
42 |
43 |         result.evals[self.query.query_id] = eval_data
44 |         self.repository.set(self.parser_id, result)
45 |         return eval_data
46 |
47 |
48 | def evaluation(query: str, expected: str, context: str, client: BaseChatModel) -> tuple[str, int]:
49 |     class RagResult(BaseModel):
50 |         answer: str
51 |
52 |     context = context.replace("{", "{{").replace("}", "}}")
53 |     system_message = """You are a helpful assistant.
54 | Please respond to the query using the provided Context.
55 | If the query contains information not included in the Context, reply with "I don’t know".
56 |
57 | ## Context\n{context}\n
58 | ## Query\n{query}\n
59 | ## Output\n{instruction}"""
60 |     output_parser = PydanticOutputParser(pydantic_object=RagResult)
61 |     rag_result = (client | output_parser).invoke(
62 |         system_message.format(context=context, instruction=output_parser.get_format_instructions(), query=query)
63 |     )
64 |
65 |     class EvalResult(BaseModel):
66 |         rank: int
67 |
68 |     system_message = """You are an excellent evaluator.
69 | Please grade the user’s responses to the following questions on a scale of 0 to 100 points.
70 | Provide only the score.
71 |
72 | ## Example
73 | - If the user’s response is perfect, assign 100 points.
74 | - If the user’s response is incorrect, assign 0 points.
75 | ## Query\n{query}\n
76 | ## Expected\n{expected}\n
77 | ## User Response\n{answer}\n
78 | ## Output\n{instruction}
79 | """
80 |     output_parser = PydanticOutputParser(pydantic_object=EvalResult)
81 |     response = (client | output_parser).invoke(
82 |         system_message.format(
83 |             query=query,
84 |             expected=expected,
85 |             instruction=output_parser.get_format_instructions(),
86 |             answer=rag_result.answer,
87 |         )
88 |     )
89 |     return rag_result.answer, response.rank
90 |


--------------------------------------------------------------------------------
/exparso/__init__.py:
--------------------------------------------------------------------------------
 1 | import logging
 2 | import os
 3 | from typing import Optional
 4 |
 5 | from langchain_core.language_models.chat_models import BaseChatModel
 6 | from langchain_core.runnables import RunnableConfig
 7 |
 8 | from .core import JAPANESE_CORE_PROMPT, CorePrompt, ParseCoreService
 9 | from .llm import LlmFactory
10 | from .loader import LoaderFactory
11 | from .model import Document
12 |
13 | logger = logging.getLogger(__name__)
14 |
15 |
16 | def parse_document(
17 |     path: str,
18 |     model: Optional[BaseChatModel] = None,
19 |     context: Optional[str] = None,
20 |     prompt: CorePrompt = JAPANESE_CORE_PROMPT,
21 |     config: Optional[RunnableConfig] = None,
22 | ) -> Document:
23 |     """ドキュメントをMLLMによって読み込む
24 |
25 |     Args:
26 |         path (str): ファイルパス
27 |         model (BaseChatModel): langchain's BaseChatModel
28 |         context (str): ユーザーコンテキスト
29 |         config (dict, optional): LLM Input 設定. Defaults to None.
30 |     Returns:
31 |         Document: ドキュメントの情報
32 |     """
33 |
34 |     # ファイルが存在しない場合はエラーを出力
35 |     if not os.path.exists(path):
36 |         raise FileNotFoundError(f"File not found: {path}")
37 |
38 |     # 拡張子から適したLoaderを呼び出す
39 |     extension = os.path.basename(path).split(".")[-1]
40 |     loader = LoaderFactory.create(extension)
41 |     logger.debug(f"Loader is {loader.__class__.__name__}")
42 |
43 |     # モデル名からインスタンスを生成する
44 |     llm_model = LlmFactory.create(model)
45 |     llm_model_name = llm_model.__class__.__name__ if llm_model else "None"
46 |     logger.debug(f"MLLM model is {llm_model_name}")
47 |
48 |     # ファイルを読み込む
49 |     raw_contents = loader.load(path)
50 |     logger.debug(f"Loaded {len(raw_contents)} pages")
51 |     logger.debug("Start Parse Document")
52 |
53 |     if not llm_model:
54 |         logger.warning("MLLM model is not defined.")
55 |         return Document.from_load_data(raw_contents)
56 |
57 |     # LLMによる処理を行う
58 |     parser = ParseCoreService(llm=llm_model, file_path=path, prompt=prompt, user_context=context, config=config)
59 |     doc = parser(contents=raw_contents)
60 |     return doc
61 |


--------------------------------------------------------------------------------
/exparso/core/__init__.py:
--------------------------------------------------------------------------------
1 | from .parse_core_service import ParseCoreService
2 | from .prompt import ENGLISH_CORE_PROMPT, JAPANESE_CORE_PROMPT, CorePrompt
3 |
4 | __all__ = ["ParseCoreService", "CorePrompt", "JAPANESE_CORE_PROMPT", "ENGLISH_CORE_PROMPT"]
5 |


--------------------------------------------------------------------------------
/exparso/core/context/__init__.py:
--------------------------------------------------------------------------------
1 | from .update_context import update_context
2 |
3 | __all__ = ["update_context"]
4 |


--------------------------------------------------------------------------------
/exparso/core/context/update_context.py:
--------------------------------------------------------------------------------
 1 | import logging
 2 |
 3 | from langchain_core.output_parsers import JsonOutputParser
 4 | from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
 5 | from pydantic import BaseModel
 6 |
 7 | from ...model import HumanMessage, LlmModel, LlmResponse, SystemMessage
 8 | from ..prompt import CorePrompt
 9 | from ..type import ContextData, ParseDocument
10 |
11 | logger = logging.getLogger(__name__)
12 |
13 |
14 | def update_context(llm: LlmModel, prompt: CorePrompt) -> Runnable[ParseDocument, ContextData]:
15 |     def pass_through(data: ParseDocument) -> ContextData:
16 |         return data.context
17 |
18 |     def integrate(*args, **kwargs) -> ContextData:
19 |         new = args[0]["new"]
20 |         old = args[0]["old"]
21 |         assert isinstance(new, ContextData) and isinstance(old, ContextData)
22 |
23 |         return ContextData(
24 |             path=old.path,
25 |             cost=new.cost + old.cost,
26 |             content=new.content,
27 |             user_context=old.user_context,
28 |         )
29 |
30 |     def create_messages(data: ParseDocument) -> list[SystemMessage | HumanMessage]:
31 |         parser = JsonOutputParser(pydantic_object=_Answer)
32 |         system_prompt = SystemMessage(
33 |             content=prompt.update_context.format(
34 |                 context=data.context.text(), format_instructions=parser.get_format_instructions()
35 |             ),
36 |         )
37 |         return [system_prompt, HumanMessage(data.new_page.contents)]
38 |
39 |     update_model = RunnableLambda(create_messages) | llm | RunnableLambda(parse)
40 |     model = RunnableParallel(new=update_model, old=RunnableLambda(pass_through)) | RunnableLambda(integrate)
41 |     return model
42 |
43 |
44 | def parse(response: LlmResponse) -> ContextData:
45 |     answer = _Answer.model_validate(response.content)
46 |     return ContextData(
47 |         path="",
48 |         cost=response.cost,
49 |         content=answer.context,
50 |         user_context="",
51 |     )
52 |
53 |
54 | class _Answer(BaseModel):
55 |     context: str
56 |


--------------------------------------------------------------------------------
/exparso/core/docs_type/__init__.py:
--------------------------------------------------------------------------------
1 | from .judge_document_type import judge_document_type, no_judge
2 |
3 | __all__ = ["judge_document_type", "no_judge"]
4 |


--------------------------------------------------------------------------------
/exparso/core/docs_type/judge_document_type.py:
--------------------------------------------------------------------------------
 1 | import copy
 2 | import logging
 3 |
 4 | from langchain_core.output_parsers import JsonOutputParser
 5 | from langchain_core.runnables import Runnable, RunnableLambda
 6 | from pydantic import BaseModel, Field
 7 |
 8 | from ...model import Cost, HumanMessage, LlmModel, LlmResponse, LoadPageContents, SystemMessage
 9 | from ..prompt import CorePrompt
10 | from ..type import DocumentType, DocumentTypeEnum
11 |
12 | logger = logging.getLogger(__name__)
13 |
14 |
15 | def parse_response(response: LlmResponse) -> DocumentType:
16 |     answer = _Answer.model_validate(response.content)
17 |     return DocumentType(types=answer.types, cost=response.cost)
18 |
19 |
20 | def judge_document_type(llm: LlmModel, prompt: CorePrompt) -> Runnable[LoadPageContents, DocumentType]:
21 |     """ページの内容を分析し、ドキュメントの種類を判定します。言語の判定も行う。"""
22 |
23 |     def create_messages(page: LoadPageContents) -> list[SystemMessage | HumanMessage]:
24 |         parser = JsonOutputParser(pydantic_object=_Answer)
25 |         return [
26 |             SystemMessage(
27 |                 content=prompt.judge_document_type.format(
28 |                     format_instructions=parser.get_format_instructions(),
29 |                     types_explanation=DocumentTypeEnum.enum_explain(),
30 |                 )
31 |             ),
32 |             HumanMessage(content="Please analyze this image.", image=copy.copy(page.image), image_low=True),
33 |         ]
34 |
35 |     model = RunnableLambda(create_messages) | llm | RunnableLambda(parse_response)
36 |     return model
37 |
38 |
39 | def no_judge() -> Runnable[LoadPageContents, DocumentType]:
40 |     def default_type(page: LoadPageContents) -> DocumentType:
41 |         return DocumentType(types=[], cost=Cost.zero_cost())
42 |
43 |     return RunnableLambda(default_type)
44 |
45 |
46 | class _Answer(BaseModel):
47 |     types: list[DocumentTypeEnum] = Field(..., description="Types of content present in the document.")
48 |


--------------------------------------------------------------------------------
/exparso/core/parse/__init__.py:
--------------------------------------------------------------------------------
1 | from .parse_document import parse_document
2 |
3 | __all__ = ["parse_document"]
4 |


--------------------------------------------------------------------------------
/exparso/core/parse/parse_document.py:
--------------------------------------------------------------------------------
 1 | import logging
 2 |
 3 | from langchain_core.output_parsers import JsonOutputParser
 4 | from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel, RunnablePassthrough
 5 | from pydantic import BaseModel
 6 |
 7 | from ...model import HumanMessage, LlmModel, LlmResponse, PageContents, SystemMessage
 8 | from ..prompt import CorePrompt
 9 | from ..type import DocumentTypeEnum, InputParseDocument, ParseDocument
10 |
11 | logger = logging.getLogger(__name__)
12 |
13 |
14 | def parse_document(llm: LlmModel, prompt: CorePrompt) -> Runnable[InputParseDocument, ParseDocument]:
15 |     def integrate(*args, **kwargs) -> ParseDocument:
16 |         response = args[0]["response"]
17 |         input_parse_document = args[0]["passthrough"]
18 |         assert isinstance(response, LlmResponse) and isinstance(input_parse_document, InputParseDocument)
19 |         answer = _Answer.model_validate(response.content)
20 |         input_parse_document.context.cost += response.cost
21 |         return ParseDocument(
22 |             new_page=PageContents(contents=answer.output, page_number=input_parse_document.page.page_number),
23 |             context=input_parse_document.context,
24 |         )
25 |
26 |     def create_messages(input_parse_document: InputParseDocument) -> list[SystemMessage | HumanMessage]:
27 |         system_prompt = generate_system_message(input_parse_document.document_type, input_parse_document.context.text())
28 |         human_prompt = HumanMessage(
29 |             content=prompt.extract_human_message(input_parse_document.page.contents),
30 |             image=input_parse_document.page.image,
31 |         )
32 |
33 |         messages: list[SystemMessage | HumanMessage] = [system_prompt, human_prompt]
34 |         return messages
35 |
36 |     def generate_system_message(types: list[DocumentTypeEnum], context: str) -> SystemMessage:
37 |         parser = JsonOutputParser(pydantic_object=_Answer)
38 |         retval = ""
39 |         if DocumentTypeEnum.IMAGE in types:
40 |             retval += prompt.image_prompt
41 |         if DocumentTypeEnum.FLOWCHART in types:
42 |             retval += prompt.flowchart_prompt
43 |         if DocumentTypeEnum.TABLE in types:
44 |             retval += prompt.table_prompt
45 |         if DocumentTypeEnum.GRAPH in types:
46 |             retval += prompt.graph_prompt
47 |
48 |         system_prompt = prompt.extract_document.format(
49 |             document_type_prompt=retval, context=context, format_instruction=parser.get_format_instructions()
50 |         )
51 |         return SystemMessage(content=system_prompt)
52 |
53 |     model = RunnableParallel(
54 |         response=RunnableLambda(create_messages) | llm, passthrough=RunnablePassthrough()
55 |     ) | RunnableLambda(integrate)
56 |     return model
57 |
58 |
59 | class _Answer(BaseModel):
60 |     output: str
61 |


--------------------------------------------------------------------------------
/exparso/core/parse_core_service.py:
--------------------------------------------------------------------------------
 1 | import logging
 2 | from typing import Optional
 3 |
 4 | from langchain_core.runnables import RunnableConfig
 5 | from tenacity import retry, stop_after_attempt, wait_fixed
 6 |
 7 | from ..model import Cost, Document, LlmModel, LoadPageContents, PageContents
 8 | from .context import update_context
 9 | from .docs_type import judge_document_type, no_judge
10 | from .parse import parse_document
11 | from .prompt import CorePrompt
12 | from .type import ContextData, DocumentType, DocumentTypeEnum, InputParseDocument, ParseDocument
13 |
14 | logger = logging.getLogger(__name__)
15 |
16 |
17 | class ParseCoreService:
18 |     def __init__(
19 |         self,
20 |         llm: LlmModel,
21 |         file_path: str,
22 |         prompt: CorePrompt,
23 |         user_context: Optional[str],
24 |         config: Optional[RunnableConfig] = None,
25 |     ) -> None:
26 |         self.parser = parse_document(llm, prompt=prompt)
27 |         self.context_updater = update_context(llm, prompt=prompt)
28 |         self.judge_document = judge_document_type(llm, prompt=prompt)
29 |         self.context = ContextData(path=file_path, cost=Cost.zero_cost(), user_context=user_context)
30 |         self.config = config
31 |
32 |     def __call__(
33 |         self,
34 |         contents: list[LoadPageContents],
35 |     ) -> Document:
36 |         parsed_contents: list[PageContents] = []
37 |
38 |         for i, page in enumerate(contents):
39 |             logger.debug(f"Start Parse Page {page.page_number}")
40 |
41 |             document_type = self.__judge_document_type(page)
42 |             self.context.cost += document_type.cost
43 |
44 |             # 画像認識が必要ない場合は余計な処理を行わない
45 |             if DocumentTypeEnum.TEXT_ONLY in document_type.types or not document_type.types:
46 |                 logger.debug("Document Type is Text Only")
47 |                 continue
48 |
49 |             input_parse_document = InputParseDocument(
50 |                 page=page,
51 |                 context=self.context,
52 |                 document_type=document_type.types,
53 |             )
54 |             parsed_document = self.__parse_document(input_parse_document)
55 |             parsed_contents.append(parsed_document.new_page)
56 |
57 |             if i != len(contents) - 1:
58 |                 self.context = self.__update_context(parsed_document)
59 |             logger.debug(f"End Parse Page {page.page_number}")
60 |
61 |         return Document(contents=parsed_contents, cost=self.context.cost)
62 |
63 |     @retry(
64 |         # retry=retry_if_exception_type(ValidationError),
65 |         stop=stop_after_attempt(3),
66 |         wait=wait_fixed(2),
67 |     )
68 |     def __judge_document_type(self, page: LoadPageContents) -> DocumentType:
69 |         judge_document = self.judge_document if page.image else no_judge()
70 |         return judge_document.invoke(page, config=self.config)
71 |
72 |     @retry(
73 |         # retry=retry_if_exception_type(ValidationError),
74 |         stop=stop_after_attempt(3),
75 |         wait=wait_fixed(2),
76 |     )
77 |     def __parse_document(self, input_parse_document: InputParseDocument) -> ParseDocument:
78 |         return self.parser.invoke(input_parse_document, config=self.config)
79 |
80 |     @retry(
81 |         # retry=retry_if_exception_type(ValidationError),
82 |         stop=stop_after_attempt(3),
83 |         wait=wait_fixed(2),
84 |     )
85 |     def __update_context(self, parsed_document: ParseDocument) -> ContextData:
86 |         return self.context_updater.invoke(parsed_document, config=self.config)
87 |


--------------------------------------------------------------------------------
/exparso/core/prompt/__init__.py:
--------------------------------------------------------------------------------
1 | from .default_prompt import ENGLISH_CORE_PROMPT, JAPANESE_CORE_PROMPT
2 | from .prompt import CorePrompt
3 |
4 | __all__ = [
5 |     "CorePrompt",
6 |     "JAPANESE_CORE_PROMPT",
7 |     "ENGLISH_CORE_PROMPT",
8 | ]
9 |


--------------------------------------------------------------------------------
/exparso/core/prompt/default_prompt.py:
--------------------------------------------------------------------------------
  1 | from .prompt import CorePrompt
  2 |
  3 | JAPANESE_CORE_PROMPT = CorePrompt(
  4 |     judge_document_type="""Analyze the input image and classify its content according to the following properties.
  5 | # Steps
  6 |
  7 | 1. Analyze the input image to identify all content types present.
  8 | 2. For each property, select all that apply.
  9 |
 10 | # Types
 11 | {types_explanation}
 12 |
 13 | # Output Format
 14 | {format_instructions}
 15 | """,  # noqa
 16 |     extract_document="""あなたは画像から文書を読み取る専門家です。与えられた画像の内容を正確に書き起こしてください。
 17 |
 18 | # Constraints
 19 |
 20 | - ユーザーが文章を入力します。ドキュメントをより正確にするために修正してください。
 21 | - 画像に存在しない内容は回答しないでください。
 22 | - Document Type はデータを読み込みときの参考情報として提供されます。
 23 | - Document Context はドキュメントの参考情報として提供されます。
 24 |
 25 | # Document Type
 26 |
 27 | ## Text
 28 |
 29 | - 画像内のすべてのテキストを正しく抽出してください。
 30 |
 31 | {document_type_prompt}
 32 |
 33 | # Document Context
 34 |
 35 | {context}
 36 |
 37 | # Output
 38 | {format_instruction}
 39 | """,  # noqa
 40 |     update_context="""提供されたコンテキストと新しい情報に基づいて、コンテキストを更新してください。
 41 |
 42 | # Constraints
 43 |
 44 | - 新しい要件、前提条件、またはアクション項目をリストにしてください。これは、今後の処理で必要になる可能性があります。
 45 | - 新しい情報はユーザー入力によって提供されます。
 46 | - コンテキストは5〜7文で維持してください。
 47 |
 48 | # Context
 49 |
 50 | {context}
 51 |
 52 | # Example
 53 |
 54 | 応募者は申請前に少なくとも1年間その州に居住している必要があります。
 55 | 必要書類には有効な運転免許証または州発行のIDが含まれます。
 56 | 応募者は18歳以上でなければなりません。
 57 | 所得証明書（最近の給与明細または納税申告書）が必要です。
 58 | 応募者は最終承認前に必須のトレーニングセッションを完了しなければなりません。
 59 |
 60 | # Output
 61 | {format_instructions}
 62 | """,  # noqa
 63 |     table_prompt="""
 64 | ## Table
 65 |
 66 | - テーブル内の情報をマークダウン形式で記述してください。
 67 | - 出力にテーブルの概要を追加してください。
 68 |
 69 | ### Example
 70 | **Input**: 名前と年齢が含まれるテーブル。
 71 | **Output**:
 72 | このテーブルは2人の名前と年齢を示しています。
 73 |
 74 | | Name  | Age |
 75 | |-------|-----|
 76 | | Alice | 25  |
 77 | | Bob   | 30  |
 78 |
 79 | """,
 80 |     flowchart_prompt="""
 81 | ## Flowchart
 82 |
 83 | - フローチャートの情報を説明してください。
 84 | - フローチャートをMermaid形式に変換してください。
 85 | - 出力にフローチャートの概要を追加してください。
 86 |
 87 | ### Example
 88 | **Input**: ケーキ作りのプロセスを示すフローチャート。
 89 | **Output**:
 90 | このフローチャートはケーキ作りのプロセスを示しています。
 91 | ```mermaid
 92 | graph TD;
 93 |     A(Start) --> B(Add flour)
 94 |     B --> C(Add sugar)
 95 |     C --> D(Bake)
 96 |     D --> E(End)
 97 | ```
 98 |
 99 | """,
100 |     graph_prompt="""
101 | ## Graph
102 |
103 | - グラフ内の情報を説明してください。
104 | - グラフ内のテキストを読み取り、内容を記述してください。
105 | - 出力にグラフの概要を追加してください。
106 |
107 | ### Example
108 | **Input**: 人数と車の数が含まれるグラフ。
109 | **Output**:
110 | このグラフは人数と車の数の関係を示しています。
111 | 人数が増加している一方、車の数は減少しています。
112 | 2020年には、人数が100人で、車の数が50台です。
113 |
114 | """,
115 |     image_prompt="""
116 | ## Image
117 |
118 | - 画像内の情報を説明してください。
119 | - 画像にテキストが含まれている場合、その内容を記述してください。
120 |
121 | ### Example
122 | **Input**: 異なるセクションを説明するラベルが付いた円グラフが含まれる画像。
123 | **Output**:
124 | この画像は、異なるセクションを説明するラベルが付いた円グラフを示しています。
125 | 最も大きなセクションはAで、続いてBとCが続きます。
126 |
127 | """,
128 |     extract_document_text_prompt="以下のテキストを読み取りました。\n {document_text}",
129 |     extract_image_only_prompt="入力は画像のみです。",
130 | )
131 |
132 | ENGLISH_CORE_PROMPT = CorePrompt(
133 |     judge_document_type="""Analyze the input image and classify its content according to the following properties.
134 | # Steps
135 |
136 | 1. Analyze the input image to identify all content types present.
137 | 2. For each property, select all that apply.
138 |
139 | # Types
140 | {types_explanation}
141 |
142 | # Output Format
143 | {format_instructions}
144 | """,  # noqa
145 |     extract_document="""You are an expert in reading documents from images.
146 | Please write out the content accurately, staying faithful to the given image content.
147 |
148 | # Constraints
149 | - User will input the sentence. Please modify the sentence to make it more accurate.
150 | - Don't hallucinate the content that doesn't exist in the image.
151 | - Document Text is provided for reference.
152 | - Document Context is provided for reference.
153 |
154 | # Document Type
155 |
156 | ## Text
157 |
158 | - Please extract the all texts in this documents.
159 |
160 | {document_type_prompt}
161 |
162 | # Document Context
163 |
164 | {context}
165 |
166 | # Output
167 | {format_instruction}
168 | """,  # noqa
169 |     update_context="""Based on the provided context and new information, update the context to include relevant information.
170 |
171 | # Constraints
172 | - List any requirements, prerequisites, or action items extracted from new information, as they may be necessary for further pages.
173 | - New information is provided by user input.
174 | - Maintain the context with 5-7 sentences.
175 |
176 | # Context
177 |
178 | {context}
179 |
180 | # Example
181 |
182 | The applicant must be a resident of the state for at least one year before applying.
183 | Required documents include a valid driver’s license or state ID.
184 | The applicant must be at least 18 years old.
185 | Proof of income (recent pay stubs or tax returns) is required.
186 | A mandatory training session must be completed by the applicant before final approval.
187 |
188 | # Output
189 | {format_instructions}
190 | """,  # noqa
191 |     table_prompt="""
192 | ## Table
193 |
194 | - Please describe the information in the table in markdown format.
195 | - Add summary of the table in the output.
196 |
197 | ### Example
198 |
199 | **Input**: A table contains the age and name.
200 | **Output**:
201 | This table shows the name and age of two people.
202 |
203 | | Name  | Age |
204 | |-------|-----|
205 | | Alice | 25  |
206 | | Bob   | 30  |
207 |
208 | """,
209 |     flowchart_prompt="""
210 | ## Flowchart
211 |
212 | - Please describe the information in the flowchart.
213 | - Translate the flowchart into mermaid format.
214 | - Add summary of the flowchart in the output.
215 |
216 | ### Example
217 | **Input**: A flowchart contains the process of making a cake.
218 | **Output**:
219 | This flowchart shows the process of making a cake.
220 | ```mermaid
221 | graph TD;
222 |     A(Start) --> B(Add flour)
223 |     B --> C(Add sugar)
224 |     C --> D(Bake)
225 |     D --> E(End)
226 | ```
227 |
228 | """,
229 |     graph_prompt="""
230 | ## Graph
231 |
232 | - Please describe the information in the graph.
233 | - Read the text in the graph and describe the content.
234 | - Add summary of the graph in the output.
235 |
236 | ### Example
237 | **Input**: A graph contains the number of people and the number of cars.
238 | **Output**:
239 | This graph shows the relationship between the number of people and the number of cars.
240 | The number of people is increasing, while the number of cars is decreasing.
241 | In 2020, the number of people is 100, and the number of cars is 50.
242 |
243 | """,
244 |     image_prompt="""
245 | ## Image
246 |
247 | - Please describe the information in the image.
248 | - If the image contains text, please describe the content.
249 |
250 | ### Example
251 | **Input**: An image contains a pie chart with labels describing different sections.
252 | **Output**:
253 | This image shows a pie chart with labels describing different sections.
254 | The largest section is A, followed by B and C.
255 |
256 | """,  # noqa
257 |     extract_document_text_prompt="I have read the following text.\n {document_text}",
258 |     extract_image_only_prompt="The input is an image only.",
259 | )
260 |


--------------------------------------------------------------------------------
/exparso/core/prompt/prompt.py:
--------------------------------------------------------------------------------
 1 | from pydantic import BaseModel, ConfigDict, Field, field_validator
 2 |
 3 |
 4 | class CorePrompt(BaseModel):
 5 |     """Prompt class for core functionalities."""
 6 |
 7 |     judge_document_type: str = Field(description="Prompt for judging document type.")
 8 |     extract_document: str = Field(
 9 |         description="Prompt for extracting document content.",
10 |     )
11 |     update_context: str = Field(
12 |         description="Prompt for updating context.",
13 |     )
14 |
15 |     # Prompt for different document types
16 |     table_prompt: str = Field(
17 |         description="Prompt for extracting table data.",
18 |     )
19 |     flowchart_prompt: str = Field(
20 |         description="Prompt for extracting flowchart data.",
21 |     )
22 |     graph_prompt: str = Field(
23 |         description="Prompt for extracting graph data.",
24 |     )
25 |     image_prompt: str = Field(
26 |         description="Prompt for extracting image data.",
27 |     )
28 |
29 |     extract_document_text_prompt: str = Field(
30 |         description="Prompt for extracting text from a document.",
31 |     )
32 |     extract_image_only_prompt: str = Field(description="Prompt for extracting text from an image.")
33 |
34 |     def extract_human_message(self, document_text: str) -> str:
35 |         """Generates a human message based on the document text and image."""
36 |         return (
37 |             self.extract_document_text_prompt.format(document_text=document_text)
38 |             if document_text
39 |             else self.extract_image_only_prompt.format(document_text=document_text)
40 |         )
41 |
42 |     @field_validator("judge_document_type")
43 |     def validate_judge_document_type(cls, value):
44 |         if "{types_explanation}" not in value:
45 |             raise ValueError("The string must contain '{types_explanation}'.")
46 |         elif "{format_instructions}" not in value:
47 |             raise ValueError("The string must contain '{format_instructions}'.")
48 |         return value
49 |
50 |     @field_validator("extract_document")
51 |     def validate_extract_document(cls, value):
52 |         if "{document_type_prompt}" not in value:
53 |             raise ValueError("The string must contain '{document_type_prompt}'.")
54 |         elif "{context}" not in value:
55 |             raise ValueError("The string must contain '{context}'.")
56 |         elif "{format_instruction}" not in value:
57 |             raise ValueError("The string must contain '{format_instruction}'.")
58 |         return value
59 |
60 |     @field_validator("update_context")
61 |     def validate_update_context(cls, value):
62 |         if "{context}" not in value:
63 |             raise ValueError("The string must contain '{context}'.")
64 |         elif "{format_instructions}" not in value:
65 |             raise ValueError("The string must contain '{format_instructions}'.")
66 |         return value
67 |
68 |     @field_validator("extract_document_text_prompt")
69 |     def validate_extract_document_text_prompt(cls, value):
70 |         if "{document_text}" not in value:
71 |             raise ValueError("The string must contain '{document_text}'.")
72 |         return value
73 |
74 |     model_config = ConfigDict(frozen=True)
75 |


--------------------------------------------------------------------------------
/exparso/core/type.py:
--------------------------------------------------------------------------------
 1 | from enum import Enum
 2 |
 3 | from pydantic import BaseModel
 4 |
 5 | from ..model import Cost, LoadPageContents, PageContents
 6 |
 7 |
 8 | class DocumentTypeEnum(Enum):
 9 |     TABLE = "table"
10 |     FLOWCHART = "flowchart"
11 |     GRAPH = "graph"
12 |     IMAGE = "image"
13 |     TEXT = "text"
14 |     TEXT_ONLY = "text_only"
15 |
16 |     @staticmethod
17 |     def enum_explain():
18 |         return """
19 | - **table**: Select if the image contains a table, such as a grid or matrix displaying structured data.
20 | - **flowchart**: Select if the image contains a flowchart or diagram illustrating a process or sequence of steps.
21 | - **graph**: Select if the image contains a graph, chart, or plot.
22 | - **image**: Select if the image contains any other image except for tables and graphs.
23 | - **text**: Select if the image contains any text, even if other elements are also present.
24 | - **text_only**: Select if the image contains only text and no other elements.
25 | """
26 |
27 |
28 | class DocumentType(BaseModel):
29 |     types: list[DocumentTypeEnum]
30 |     cost: Cost
31 |
32 |
33 | class ContextData(BaseModel):
34 |     path: str
35 |     cost: Cost
36 |     content: str = ""
37 |     user_context: str | None = None
38 |
39 |     def text(self):
40 |         retval = "## path\n" + self.path
41 |         if self.user_context:
42 |             retval += "\n## user_context\n" + self.user_context
43 |         if self.content:
44 |             retval += "\n## content\n" + self.content
45 |         return retval
46 |
47 |
48 | class ParseDocument(BaseModel):
49 |     new_page: PageContents
50 |     context: ContextData
51 |
52 |
53 | class InputParseDocument:
54 |     def __init__(
55 |         self,
56 |         page: LoadPageContents,
57 |         context: ContextData,
58 |         document_type: list[DocumentTypeEnum],
59 |     ):
60 |         self.page = page
61 |         self.context = context
62 |         self.document_type = document_type
63 |


--------------------------------------------------------------------------------
/exparso/llm/__init__.py:
--------------------------------------------------------------------------------
1 | from .llm_factory import LlmFactory
2 |
3 | __all__ = [
4 |     "LlmFactory",
5 | ]
6 |


--------------------------------------------------------------------------------
/exparso/llm/claude.py:
--------------------------------------------------------------------------------
 1 | from typing import Sequence
 2 |
 3 | from langchain_core.language_models.chat_models import BaseChatModel
 4 | from langchain_core.messages import BaseMessage
 5 | from langchain_core.messages import HumanMessage as _HumanMessage
 6 | from langchain_core.messages import SystemMessage as _SystemMessage
 7 | from langchain_core.runnables import RunnableLambda
 8 |
 9 | from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage
10 |
11 |
12 | def convert_message(messages: Sequence[HumanMessage | SystemMessage]) -> Sequence[_HumanMessage | _SystemMessage]:
13 |     retval: list[_HumanMessage | _SystemMessage] = []
14 |     MAX_IMAGE_LENGTH = 384.0
15 |     for m in messages:
16 |         if isinstance(m, HumanMessage):
17 |             if m.image:
18 |                 if m.image_low:
19 |                     large_length = max(m.image.width, m.image.height)
20 |                     scale = MAX_IMAGE_LENGTH / large_length
21 |                     m.scale_image(scale)
22 |                 media_type, base64 = m.image_base64
23 |                 retval.append(
24 |                     _HumanMessage(
25 |                         role="user",
26 |                         content=[
27 |                             {"type": "text", "text": m.content},
28 |                             {
29 |                                 "type": "image",
30 |                                 "source": {
31 |                                     "type": "base64",
32 |                                     "media_type": media_type,
33 |                                     "data": base64,
34 |                                 },
35 |                             },
36 |                         ],
37 |                     )
38 |                 )
39 |             else:
40 |                 retval.append(_HumanMessage(role="user", content=m.content))
41 |         elif isinstance(m, SystemMessage):
42 |             retval.append(_SystemMessage(role="system", content=m.content))
43 |     return retval
44 |
45 |
46 | def parse_response(response: BaseMessage) -> LlmResponse:
47 |     assert isinstance(response, BaseMessage)
48 |     content = response.content
49 |     cost = Cost(
50 |         input_token=response.response_metadata.get("usage", {}).get("input_tokens", 0),
51 |         output_token=response.response_metadata.get("usage", {}).get("output_tokens", 0),
52 |         llm_model_name=response.response_metadata.get("model", "unknown"),
53 |     )
54 |     assert isinstance(content, str)
55 |     return LlmResponse(content=content, cost=cost)
56 |
57 |
58 | def generate_claude_llm(model: BaseChatModel) -> LlmModel:
59 |     return RunnableLambda(convert_message) | model | RunnableLambda(parse_response)
60 |


--------------------------------------------------------------------------------
/exparso/llm/gemini.py:
--------------------------------------------------------------------------------
 1 | from typing import Sequence
 2 |
 3 | from langchain_core.language_models.chat_models import BaseChatModel
 4 | from langchain_core.messages import AIMessage
 5 | from langchain_core.messages import HumanMessage as _HumanMessage
 6 | from langchain_core.runnables import RunnableLambda
 7 |
 8 | from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage
 9 |
10 |
11 | def convert_message(
12 |     messages: Sequence[HumanMessage | SystemMessage],
13 | ) -> Sequence[_HumanMessage | str]:
14 |     MAX_IMAGE_LENGTH = 384.0  # low resolution解析のための画像サイズ
15 |
16 |     retval: list[str | _HumanMessage] = []
17 |     for m in messages:
18 |         if isinstance(m, HumanMessage):
19 |             if m.image:
20 |                 if m.image_low:
21 |                     large_length = max(m.image.width, m.image.height)
22 |                     scale = MAX_IMAGE_LENGTH / large_length
23 |                     m.scale_image(scale)
24 |                 mime_type, base64 = m.image_base64
25 |                 retval.append(
26 |                     _HumanMessage(
27 |                         role="user",
28 |                         content=[
29 |                             m.content,
30 |                             {"type": "media", "mime_type": mime_type, "data": base64},
31 |                         ],
32 |                     )
33 |                 )
34 |
35 |             else:
36 |                 retval.append(m.content)
37 |         elif isinstance(m, SystemMessage):
38 |             retval.append(m.content)
39 |     return retval
40 |
41 |
42 | def generate_gemini_llm(model: BaseChatModel) -> LlmModel:
43 |     def parse_response(response: AIMessage) -> LlmResponse:
44 |         content = response.content
45 |         input_token = response.usage_metadata.get("input_tokens", 0) if response.usage_metadata else 0
46 |         output_token = response.usage_metadata.get("output_tokens", 0) if response.usage_metadata else 0
47 |         assert isinstance(content, str)
48 |         return LlmResponse(
49 |             content=content,
50 |             cost=Cost(
51 |                 input_token=input_token,
52 |                 output_token=output_token,
53 |                 llm_model_name=model.model_name if model.model_name else "unknown",  # type: ignore
54 |             ),
55 |         )
56 |
57 |     return RunnableLambda(convert_message) | model | RunnableLambda(parse_response)
58 |


--------------------------------------------------------------------------------
/exparso/llm/llm_factory.py:
--------------------------------------------------------------------------------
 1 | from langchain_core.language_models.chat_models import BaseChatModel
 2 |
 3 | from ..model import LlmModel
 4 | from .claude import generate_claude_llm
 5 | from .gemini import generate_gemini_llm
 6 | from .openai import generate_openai_llm
 7 |
 8 |
 9 | class LlmFactory:
10 |     @staticmethod
11 |     def create(model: BaseChatModel | None) -> LlmModel | None:
12 |         if not model:
13 |             return None
14 |
15 |         model_name = model.__class__.__name__
16 |         if model_name == "AzureChatOpenAI" or model_name == "ChatOpenAI":
17 |             return generate_openai_llm(model)
18 |         elif "ChatAnthropic" in model_name:
19 |             return generate_claude_llm(model)
20 |         elif "ChatVertexAI" in model_name:
21 |             return generate_gemini_llm(model)
22 |         else:
23 |             raise ValueError(f"Unsupported model: {model_name}")
24 |


--------------------------------------------------------------------------------
/exparso/llm/openai.py:
--------------------------------------------------------------------------------
 1 | from typing import Sequence
 2 |
 3 | from langchain_core.language_models.chat_models import BaseChatModel
 4 | from langchain_core.messages import BaseMessage
 5 | from langchain_core.messages import HumanMessage as _HumanMessage
 6 | from langchain_core.messages import SystemMessage as _SystemMessage
 7 | from langchain_core.runnables import RunnableLambda
 8 |
 9 | from ..model import Cost, HumanMessage, LlmModel, LlmResponse, SystemMessage
10 |
11 |
12 | def convert_message(
13 |     messages: Sequence[HumanMessage | SystemMessage],
14 | ) -> Sequence[_HumanMessage | _SystemMessage]:
15 |     retval: list[_HumanMessage | _SystemMessage] = []
16 |     for m in messages:
17 |         if isinstance(m, HumanMessage):
18 |             if m.image:
19 |                 image_type, base64 = m.image_base64
20 |                 retval.append(
21 |                     _HumanMessage(
22 |                         role="user",
23 |                         content=[
24 |                             {"type": "text", "text": m.content},
25 |                             {
26 |                                 "type": "image_url",
27 |                                 "image_url": {
28 |                                     "url": f"data:{image_type};base64,{base64}",
29 |                                 },
30 |                                 "detail": "low" if m.image_low else "high",
31 |                             },
32 |                         ],
33 |                     )
34 |                 )
35 |             else:
36 |                 retval.append(_HumanMessage(role="user", content=m.content))
37 |         elif isinstance(m, SystemMessage):
38 |             retval.append(_SystemMessage(role="system", content=m.content))
39 |     return retval
40 |
41 |
42 | def parse_response(response: BaseMessage) -> LlmResponse:
43 |     assert isinstance(response, BaseMessage)
44 |     content = response.content
45 |     model_name = response.response_metadata.get("model_name", "unknown")
46 |     token_usage = response.response_metadata.get("token_usage", {})
47 |     output_token = token_usage.get("completion_tokens", 0)
48 |     input_token = token_usage.get("prompt_tokens", 0)
49 |     assert isinstance(content, str)
50 |     assert isinstance(model_name, str)
51 |     return LlmResponse(
52 |         content=content,
53 |         cost=Cost(
54 |             input_token=input_token,
55 |             output_token=output_token,
56 |             llm_model_name=model_name,
57 |         ),
58 |     )
59 |
60 |
61 | def generate_openai_llm(model: BaseChatModel) -> LlmModel:
62 |     return (
63 |         RunnableLambda(convert_message)
64 |         | model.bind(response_format={"type": "json_object"})
65 |         | RunnableLambda(parse_response)
66 |     )
67 |


--------------------------------------------------------------------------------
/exparso/loader/__init__.py:
--------------------------------------------------------------------------------
1 | from .loader_factory import LoaderFactory
2 |
3 | __all__ = ["LoaderFactory"]
4 |


--------------------------------------------------------------------------------
/exparso/loader/csv_loader.py:
--------------------------------------------------------------------------------
 1 | import csv
 2 |
 3 | from ..model import LoadPageContents, PageLoader
 4 |
 5 |
 6 | class CsvLoader(PageLoader):
 7 |     def load(self, path: str) -> list[LoadPageContents]:
 8 |         with open(path, "r", encoding="utf-8") as file:
 9 |             reader = csv.reader(file)
10 |
11 |             # Convert CSV rows into a list of lists (table)
12 |             table = [row for row in reader]
13 |
14 |             # Create a PageContents object with the table and other fields set as required
15 |             page_contents = LoadPageContents(
16 |                 contents=file.read(),
17 |                 page_number=0,
18 |                 image=None,
19 |                 tables=[table],
20 |             )
21 |         return [page_contents]
22 |


--------------------------------------------------------------------------------
/exparso/loader/docx_loader.py:
--------------------------------------------------------------------------------
1 | from ..model import LoadPageContents, PageLoader
2 | from .pdf_loader import PdfLoaderService
3 |
4 |
5 | class DocxLoader(PageLoader):
6 |     def load(self, path: str) -> list[LoadPageContents]:
7 |         pdf_pages = PdfLoaderService.load(path)
8 |         return pdf_pages
9 |


--------------------------------------------------------------------------------
/exparso/loader/image_loader.py:
--------------------------------------------------------------------------------
 1 | from PIL import Image
 2 |
 3 | from ..model import LoadPageContents, PageLoader
 4 |
 5 |
 6 | class ImageLoader(PageLoader):
 7 |     def load(self, path: str) -> list[LoadPageContents]:
 8 |         with Image.open(path) as im:
 9 |             image = im.convert("RGB")
10 |         return [
11 |             LoadPageContents(
12 |                 contents="",
13 |                 page_number=0,
14 |                 image=image,
15 |                 tables=[],
16 |             )
17 |         ]
18 |


--------------------------------------------------------------------------------
/exparso/loader/loader_factory.py:
--------------------------------------------------------------------------------
 1 | from ..model import PageLoader
 2 | from .csv_loader import CsvLoader
 3 | from .docx_loader import DocxLoader
 4 | from .image_loader import ImageLoader
 5 | from .pdf_loader import PdfLoader
 6 | from .pptx_loader import PptxLoader
 7 | from .text_file_loader import TextFileLoader
 8 | from .xlsx_loader import XlsxLoader
 9 |
10 |
11 | class LoaderFactory:
12 |     @staticmethod
13 |     def create(extension: str) -> PageLoader:
14 |         extension = extension.lower()
15 |         if extension == "pdf":
16 |             return PdfLoader()
17 |         elif extension in ["txt", "md"]:
18 |             return TextFileLoader()
19 |         elif extension == "csv":
20 |             return CsvLoader()
21 |         elif extension in ["xlsx", "xls"]:
22 |             return XlsxLoader()
23 |         elif extension in ["jpg", "jpeg", "png", "bmp", "gif"]:
24 |             return ImageLoader()
25 |         elif extension in ["docx", "doc"]:
26 |             return DocxLoader()
27 |         elif extension == "pptx":
28 |             return PptxLoader()
29 |         else:
30 |             raise ValueError("Unsupported file extension")
31 |


--------------------------------------------------------------------------------
/exparso/loader/pdf_loader.py:
--------------------------------------------------------------------------------
 1 | import os
 2 | import subprocess
 3 | import tempfile
 4 |
 5 | import pdfplumber
 6 | from pdfplumber.page import Page
 7 |
 8 | from ..model import LoadPageContents, PageLoader
 9 |
10 |
11 | class PdfLoader(PageLoader):
12 |     def load(self, path: str) -> list[LoadPageContents]:
13 |         pages = []
14 |         with pdfplumber.open(path) as pdf:
15 |             for page in pdf.pages:
16 |                 pages.append(self._load_page(page))
17 |         return pages
18 |
19 |     def _load_page(self, page: Page) -> LoadPageContents:
20 |         return LoadPageContents(
21 |             page_number=page.page_number - 1,
22 |             contents=page.extract_text(),
23 |             tables=page.extract_tables(),  # type: ignore
24 |             image=page.to_image().original,
25 |         )
26 |
27 |
28 | class PdfLoaderService:
29 |     @staticmethod
30 |     def load(path: str) -> list[LoadPageContents]:
31 |         loader = PdfLoader()
32 |         pdf_filename = os.path.splitext(os.path.basename(path))[0] + ".pdf"
33 |         with tempfile.TemporaryDirectory() as tmpdir:
34 |             pdf_path = f"{tmpdir}/{pdf_filename}"
35 |             process = subprocess.run(
36 |                 [
37 |                     "soffice",
38 |                     "--headless",
39 |                     "--convert-to",
40 |                     "pdf",
41 |                     "--outdir",
42 |                     tmpdir,
43 |                     path,
44 |                 ]
45 |             )
46 |             if process.returncode != 0:
47 |                 return []
48 |
49 |             pdf_pages = loader.load(pdf_path)
50 |             loader = PdfLoader()
51 |         return pdf_pages
52 |


--------------------------------------------------------------------------------
/exparso/loader/pptx_loader.py:
--------------------------------------------------------------------------------
1 | from ..model import LoadPageContents, PageLoader
2 | from .pdf_loader import PdfLoaderService
3 |
4 |
5 | class PptxLoader(PageLoader):
6 |     def load(self, path: str) -> list[LoadPageContents]:
7 |         pdf_pages = PdfLoaderService.load(path)
8 |         return pdf_pages
9 |


--------------------------------------------------------------------------------
/exparso/loader/text_file_loader.py:
--------------------------------------------------------------------------------
 1 | from ..model import LoadPageContents, PageLoader
 2 |
 3 |
 4 | class TextFileLoader(PageLoader):
 5 |     def load(self, path: str) -> list[LoadPageContents]:
 6 |         with open(path, "r") as f:
 7 |             contents = f.read()
 8 |         return [
 9 |             LoadPageContents(
10 |                 contents=contents,
11 |                 page_number=0,
12 |                 image=None,
13 |                 tables=[],
14 |             )
15 |         ]
16 |


--------------------------------------------------------------------------------
/exparso/loader/xlsx_loader.py:
--------------------------------------------------------------------------------
 1 | from openpyxl import load_workbook
 2 |
 3 | from ..model import LoadPageContents, PageLoader
 4 |
 5 |
 6 | class XlsxLoader(PageLoader):
 7 |     def load(self, path: str) -> list[LoadPageContents]:
 8 |         page_contents_list = []
 9 |         workbook = load_workbook(filename=path)
10 |         for index, sheet in enumerate(workbook.sheetnames):
11 |             worksheet = workbook[sheet]
12 |             table = [[cell.value for cell in row] for row in worksheet.iter_rows()]
13 |             contents = f"{sheet}\n" + "\n".join([",".join([str(cell) for cell in row]) for row in table])
14 |             page_contents = LoadPageContents(
15 |                 contents=contents,
16 |                 page_number=index,
17 |                 image=None,
18 |                 tables=[table],  # type: ignore
19 |             )
20 |             page_contents_list.append(page_contents)
21 |         return page_contents_list
22 |


--------------------------------------------------------------------------------
/exparso/model/__init__.py:
--------------------------------------------------------------------------------
 1 | from .cost import Cost
 2 | from .document import Document
 3 | from .image import Image
 4 | from .llm import HumanMessage, LlmModel, LlmResponse, SystemMessage
 5 | from .page_contents import LoadPageContents, PageContents
 6 | from .page_loader import PageLoader
 7 |
 8 | __all__ = [
 9 |     "Cost",
10 |     "Document",
11 |     "PageContents",
12 |     "Image",
13 |     "PageLoader",
14 |     "LlmModel",
15 |     "HumanMessage",
16 |     "SystemMessage",
17 |     "LlmResponse",
18 |     "LoadPageContents",
19 | ]
20 |


--------------------------------------------------------------------------------
/exparso/model/cost.py:
--------------------------------------------------------------------------------
 1 | from dataclasses import dataclass
 2 |
 3 |
 4 | @dataclass
 5 | class Cost:
 6 |     input_token: int
 7 |     output_token: int
 8 |     llm_model_name: str
 9 |
10 |     def __add__(self, other: "Cost") -> "Cost":
11 |         return Cost(
12 |             input_token=self.input_token + other.input_token,
13 |             output_token=self.output_token + other.output_token,
14 |             llm_model_name=other.llm_model_name,
15 |         )
16 |
17 |     @staticmethod
18 |     def zero_cost() -> "Cost":
19 |         return Cost(input_token=0, output_token=0, llm_model_name="")
20 |


--------------------------------------------------------------------------------
/exparso/model/document.py:
--------------------------------------------------------------------------------
 1 | from .cost import Cost
 2 | from .page_contents import LoadPageContents, PageContents
 3 |
 4 |
 5 | class Document:
 6 |     contents: list[PageContents]
 7 |     cost: Cost
 8 |
 9 |     def __init__(self, contents: list[PageContents], cost: Cost):
10 |         self.contents = contents
11 |         self.cost = cost
12 |
13 |     @classmethod
14 |     def from_load_data(cls, load_data: list[LoadPageContents]) -> "Document":
15 |         return cls(
16 |             contents=[PageContents.from_load_data(data) for data in load_data],
17 |             cost=Cost.zero_cost(),
18 |         )
19 |


--------------------------------------------------------------------------------
/exparso/model/image.py:
--------------------------------------------------------------------------------
1 | from typing import TypeAlias
2 |
3 | from PIL import Image as _Image
4 |
5 | # Imageをtypealis
6 | Image: TypeAlias = _Image.Image
7 |


--------------------------------------------------------------------------------
/exparso/model/llm.py:
--------------------------------------------------------------------------------
 1 | import base64
 2 | import copy
 3 | import json
 4 | from dataclasses import dataclass
 5 | from io import BytesIO
 6 | from typing import Sequence, TypeAlias
 7 |
 8 | from langchain_core.runnables import RunnableSerializable
 9 | from pydantic_core._pydantic_core import ValidationError
10 |
11 | from .cost import Cost
12 | from .image import Image
13 |
14 |
15 | class HumanMessage:
16 |     def __init__(self, content: str, image: Image | None = None, image_low: bool = False):
17 |         self.content = content
18 |         self.image = copy.deepcopy(image)
19 |         self.image_low = image_low
20 |
21 |     @property
22 |     def image_base64(self) -> tuple[str, str]:
23 |         if not self.image:
24 |             return "", ""
25 |         img_base64 = base64.b64encode(self.image_bytes).decode("utf-8")
26 |         return "image/png", img_base64
27 |
28 |     @property
29 |     def image_bytes(self) -> bytes:
30 |         if not self.image:
31 |             return b""
32 |
33 |         buffered = BytesIO()
34 |         self.image.save(buffered, format="PNG")
35 |         return buffered.getvalue()
36 |
37 |     def scale_image(self, scale: float):
38 |         if not self.image:
39 |             return
40 |         height = int(self.image.height * scale)
41 |         width = int(self.image.width * scale)
42 |         self.image = self.image.resize((width, height))
43 |
44 |
45 | @dataclass
46 | class SystemMessage:
47 |     content: str
48 |
49 |
50 | class LlmResponse:
51 |     content: dict
52 |
53 |     def __init__(self, content: str, cost: Cost):
54 |         if not content.startswith("{"):
55 |             index = content.find("{")
56 |             if index < 0:
57 |                 raise ValidationError("Content should start with '{'")
58 |             content = content[index:]
59 |         if not content.endswith("}"):
60 |             index = content.rfind("}")
61 |             if index < 0:
62 |                 raise ValidationError("Content should end with '}'")
63 |             content = content[: index + 1]
64 |
65 |         self.content = json.loads(content, strict=False)
66 |         # self.contentの文字列の改行を置換する
67 |         if isinstance(self.content, dict):
68 |             self.content = {k: v.replace("<br>", "\n") if isinstance(v, str) else v for k, v in self.content.items()}
69 |         self.cost = cost
70 |
71 |
72 | LlmModel: TypeAlias = RunnableSerializable[Sequence[HumanMessage | SystemMessage], LlmResponse]
73 |


--------------------------------------------------------------------------------
/exparso/model/page_contents.py:
--------------------------------------------------------------------------------
 1 | from dataclasses import dataclass
 2 | from typing import Sequence
 3 |
 4 | from .image import Image
 5 |
 6 |
 7 | @dataclass
 8 | class LoadPageContents:
 9 |     contents: str
10 |     page_number: int
11 |     image: Image | None
12 |     tables: Sequence[Sequence[Sequence[str | None]]]
13 |
14 |
15 | @dataclass
16 | class PageContents:
17 |     contents: str
18 |     page_number: int
19 |
20 |     @classmethod
21 |     def from_load_data(cls, data: LoadPageContents) -> "PageContents":
22 |         return cls(
23 |             contents=data.contents,
24 |             page_number=data.page_number,
25 |         )
26 |


--------------------------------------------------------------------------------
/exparso/model/page_loader.py:
--------------------------------------------------------------------------------
 1 | from abc import abstractmethod
 2 |
 3 | from .page_contents import LoadPageContents
 4 |
 5 |
 6 | class PageLoader:
 7 |     @abstractmethod
 8 |     def load(self, path: str) -> list[LoadPageContents]:
 9 |         pass
10 |


--------------------------------------------------------------------------------
/mkdocs.yml:
--------------------------------------------------------------------------------
 1 | site_name: Exparso
 2 | site_dir: site
 3 | docs_dir: docs
 4 | repo_url: https://github.com/InsightEdgeJP/exparso
 5 | nav:
 6 |   - 🏠 Home: index.md
 7 |   - 🤖 Algorithm: argo.md
 8 |   - 🛠️ Prompt: prompts.md
 9 |   - 📊 Evaluation:
10 |     - 🧑‍💻 Method: eval-method.md
11 |     - 💾 Dataset: eval-dataset.md
12 |     - 📈 Result: eval-result.md
13 |   - 🏛️ OSS:
14 |       - 🤝 Contributing: contributing.md
15 |   - 🔗 Links:
16 |       - Report: https://docs.google.com/presentation/d/10j4X4ubeY-nHvuWmKlLYm2WUvd6cumRd?rtpof=true&usp=drive_fs
17 |
18 | markdown_extensions:
19 |   - pymdownx.details
20 |   - pymdownx.tabbed:
21 |       alternate_style: true
22 |   - pymdownx.superfences:
23 |       custom_fences:
24 |         - name: mermaid
25 |           class: mermaid
26 |           format: !!python/name:pymdownx.superfences.fence_div_format
27 |
28 | extra_css:
29 |   - https://unpkg.com/mermaid@8.0.0/dist/mermaid.css
30 |
31 | extra_javascript:
32 |   - https://unpkg.com/mermaid@8.0.0/dist/mermaid.min.js
33 |
34 | theme:
35 |   name: material
36 |   palette:
37 |     primary: "blue"
38 |     accent: "idingo"
39 |


--------------------------------------------------------------------------------
/pyproject.toml:
--------------------------------------------------------------------------------
 1 | [project]
 2 | name = "exparso"
 3 | version = "0.0.2"
 4 | description = "Analyzing and parsing documents"
 5 | readme = "README.md"
 6 | requires-python = ">=3.10"
 7 | license = "MIT"
 8 | keywords = [ "langchain", "openai", "pdfplumber", "pillow", "openpyxl", "pdf"]
 9 | dependencies = [
10 |     "langchain>=0.3.14",
11 |     "openpyxl>=3.1.5",
12 |     "pdfplumber>=0.11.4",
13 |     "pillow>=10.4.0",
14 | ]
15 |
16 | [tool.uv]
17 | default-groups = ["dev", "test"]
18 |
19 | [dependency-groups]
20 | dev = [
21 |     "pip-licenses>=5.0.0",
22 |     "pre-commit>=4.0.1",
23 |     "pylance>=0.28.0",
24 |     "mypy>=1.15.0",
25 |     "types-openpyxl>=3.1.5.20250516",
26 |     "ruff>=0.11.4",
27 | ]
28 | test = [
29 |     "pytest>=8.3.3",
30 |     "pytest-dotenv>=0.5.2",
31 |     "pytest>=8.3.3",
32 |     "pytest-dotenv>=0.5.2",
33 |     "openai>=1.51.2",
34 |     "langchain-openai>=0.3.0",
35 |     "anthropic[vertex]>=0.36.0",
36 |     "google-cloud-aiplatform>=1.70.0",
37 |     "langchain-google-vertexai<=2.0.10",
38 | ]
39 | eval = [
40 |     "google-cloud-aiplatform>=1.70.0",
41 |     "langchain-google-vertexai<=2.0.10",
42 |     "azure-ai-documentintelligence==1.0.0",
43 |     "azure-identity>=1.19.0",
44 |     "docling==2.15.1",
45 |     "pymupdf4llm==0.0.17",
46 |     "google-cloud-storage>=2.18.2",
47 |     "matplotlib>=3.9.2",
48 |     "pandas>=2.2.3",
49 |     "tqdm>=4.66.5",
50 |     "langfuse>=2.57.0",
51 |     "pydantic-settings>=2.7.1",
52 | ]
53 | deploy = [
54 |     "twine>=5.1.1",
55 | ]
56 | docs = [
57 |     "mkdocs>=1.6.1",
58 |     "mkdocs-material>=9.5.44",
59 |     "pymdown-extensions>=10.11.2",
60 | ]
61 |
62 | [tool.ruff]
63 | line-length = 120
64 | indent-width = 4
65 |
66 | [tool.ruff.lint]
67 | select = ["E4", "E7", "E9", "F"]
68 | ignore = []
69 |
70 | [tool.pytest.ini_options]
71 | pythonpath = "exparso"
72 | testpaths = "tests"
73 | addopts = "-s"
74 | env_files = [".env"]
75 |
76 | [build-system]
77 | requires = ["hatchling"]
78 | build-backend = "hatchling.build"
79 |
80 | [tool.hatch.build.targets.sdist]
81 | exclude = ["tests", "eval", "docs", "uv.lock", "*.yml", ".*", "*.md"]
82 |
83 | [tool.hatch.build.targets.wheel]
84 | exclude = ["tests", "eval", "docs", "uv.lock", "*.yml", ".*", "*.md"]
85 |


--------------------------------------------------------------------------------
/tests/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/__init__.py


--------------------------------------------------------------------------------
/tests/constants.py:
--------------------------------------------------------------------------------
1 | PDF_TABLE_DOCUMENT = "tests/data/test.pdf"
2 | MARKDOWN_TEXT_DOCUMENT = "tests/data/test.md"
3 | JPEG_DOCUMENT = "tests/data/test.jpg"
4 | BMP_DOCUMENT = "tests/data/test.bmp"
5 | CSV_DOCUMENT = "tests/data/test.csv"
6 | XLSX_DOCUMENT = "tests/data/test.xlsx"
7 | PPTX_DOCUMENT = "tests/data/test.pptx"
8 | DOCX_DOCUMENT = "tests/data/test.docx"
9 |


--------------------------------------------------------------------------------
/tests/data/test.bmp:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:88a7b1451d3585a40a87281856249f68670016f1209c73d947ab425c6d6ec0ba
3 | size 9208346
4 |


--------------------------------------------------------------------------------
/tests/data/test.csv:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:30f816dafc44a56bc7380aafe310bf540e2ccef800e769e112ecab746f14ec4e
3 | size 77
4 |


--------------------------------------------------------------------------------
/tests/data/test.docx:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:2ee2c2382db04f95cef5ea9ba23530cd927ee5496e18f530ad093935d4f06298
3 | size 13494
4 |


--------------------------------------------------------------------------------
/tests/data/test.jpg:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:b3f4d694d7cfbcb255a6067b95e06d3f1b6d16272e23e00cd1caf34554b63f00
3 | size 46746
4 |


--------------------------------------------------------------------------------
/tests/data/test.md:
--------------------------------------------------------------------------------
 1 | ### 量子重力共鳴理論（Quantum Gravity Resonance Theory）
 2 |
 3 | **背景:**
 4 | この理論は、宇宙の最小単位である量子と、重力という巨大な力の相互作用を統一的に説明するために考案されました。通常の物理学では、量子力学と一般相対性理論は別々に扱われていますが、量子重力共鳴理論は、この2つの理論を「共鳴」という現象で結びつけます。
 5 |
 6 | **基本概念:**
 7 | 量子重力共鳴理論の核心は、「共鳴振動場（Resonant Oscillation Field）」と呼ばれる新しい物理場にあります。この場は、宇宙の基本粒子が一定の条件下で振動することで生まれ、重力と量子状態の間のエネルギー交換を可能にします。すなわち、量子粒子が特定の周波数で振動すると、重力場がそれに呼応して共鳴することで、重力そのものが量子化されるのです。
 8 |
 9 | **理論の重要な要素:**
10 |
11 | 1. **共鳴振動子（Quantum Resonators）:**
12 |    特定のエネルギーレベルにおいて、量子粒子が振動する装置です。これにより、粒子の振動周波数が重力場と共鳴し、エネルギー交換が発生します。これを利用して、重力の強さを調整することが可能になるとされます。
13 |
14 | 2. **重力共鳴波（Gravitational Resonant Waves）:**
15 |    共鳴振動場で生成された重力波です。これらの波は通常の重力波とは異なり、量子レベルのスケールで発生し、物質の振る舞いを直接制御することができます。重力共鳴波は、エネルギーや情報を瞬時に遠距離へ伝達する役割も果たします。
16 |
17 | 3. **共鳴エネルギー転送（Resonant Energy Transfer, RET）:**
18 |    共鳴振動子が作り出す周波数を用いて、異なる物質間でエネルギーを移動させるプロセスです。この技術を応用することで、物質のテレポーテーションや、エネルギー効率の飛躍的向上が実現可能になると予測されています。
19 |
20 | **応用例:**
21 | 量子重力共鳴理論を実用化することで、次のような応用が考えられています。
22 |
23 | 1. **重力制御技術:**
24 |    特定の物質や空間で重力の強さを自由に変えることができる技術です。これにより、人工重力を作り出したり、超高精度の空間探査を行うことが可能になります。
25 |
26 | 2. **量子エネルギーネットワーク:**
27 |    RET技術を使ったエネルギー供給システムで、地球のどこにいても効率的にエネルギーを供給できます。これにより、発電所の位置や電力網の設計が大幅に変わることが期待されます。
28 |
29 | 3. **次元共鳴通信:**
30 |    重力共鳴波を利用した新しい通信技術です。通常の電磁波通信に比べて、はるかに遠い距離でも遅延なく情報を伝達できるため、宇宙探査や深宇宙通信に革命をもたらします。
31 |
32 | **課題:**
33 | 量子重力共鳴理論には、いくつかの未解決問題があります。特に、共鳴振動場の安定性や、エネルギー消費を抑えた共鳴の持続方法が課題となっています。また、理論を実験的に検証するためには、現行の技術では達成不可能なほどの精度が求められています。
34 |
35 | **結論:**
36 | 量子重力共鳴理論は、現在の物理学の限界を超える新たな視点を提供する理論です。この理論が完全に解明されれば、重力と量子の世界を統一的に理解し、宇宙の根本的な構造を解き明かす鍵となるかもしれません。
37 |


--------------------------------------------------------------------------------
/tests/data/test.pdf:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:d7986880603921d1120c9a3d37def8330d56565fa4f45043bc0d024f45ff45ec
3 | size 630047
4 |


--------------------------------------------------------------------------------
/tests/data/test.pptx:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:869403508499cef99debaba2e9bf83aa7e10f10bda895686a5212a511aca6a62
3 | size 46605
4 |


--------------------------------------------------------------------------------
/tests/data/test.xlsx:
--------------------------------------------------------------------------------
1 | version https://git-lfs.github.com/spec/v1
2 | oid sha256:9e0f8ef0500b5727c08b0bcfe2234c83a10262033f2d91987c6a3276153958f2
3 | size 9933
4 |


--------------------------------------------------------------------------------
/tests/integrate/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/integrate/__init__.py


--------------------------------------------------------------------------------
/tests/integrate/conftest.py:
--------------------------------------------------------------------------------
 1 | import os
 2 |
 3 | import pytest
 4 | import vertexai
 5 | from langchain_google_vertexai import ChatVertexAI
 6 | from langchain_google_vertexai.model_garden import ChatAnthropicVertex
 7 | from langchain_openai import AzureChatOpenAI
 8 |
 9 |
10 | @pytest.fixture
11 | def chat_vertex_ai() -> ChatVertexAI:
12 |     model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash-002")
13 |     region = os.getenv("GEMINI_REGION", "us-central1")
14 |     project = os.getenv("GCP_PROJECT", "")
15 |     vertexai.init(project=project, location=region)
16 |     return ChatVertexAI(model_name=model_name)
17 |
18 |
19 | @pytest.fixture
20 | def azure_chat_openai() -> AzureChatOpenAI:
21 |     return AzureChatOpenAI(model="gpt-4o", api_version="2024-06-01")
22 |
23 |
24 | @pytest.fixture
25 | def chat_anthropic_vertex() -> ChatAnthropicVertex:
26 |     model = os.getenv("CLAUDE_MODEL_NAME", "claude-3-5-sonnet-v2@20241022")
27 |     region = os.getenv("CLAUDE_REGION", "us-east5")
28 |     project = os.getenv("GCP_PROJECT", "")
29 |     return ChatAnthropicVertex(
30 |         model_name=model,
31 |         location=region,
32 |         project=project,
33 |     )
34 |


--------------------------------------------------------------------------------
/tests/integrate/core/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/integrate/core/__init__.py


--------------------------------------------------------------------------------
/tests/integrate/core/conftest.py:
--------------------------------------------------------------------------------
1 | import pytest
2 |
3 |
4 | @pytest.fixture
5 | def llm_model(chat_vertex_ai):
6 |     from exparso.llm.gemini import generate_gemini_llm
7 |
8 |     return generate_gemini_llm(chat_vertex_ai)
9 |


--------------------------------------------------------------------------------
/tests/integrate/core/test_docs_type.py:
--------------------------------------------------------------------------------
 1 | import pytest
 2 | from PIL import Image
 3 |
 4 | from exparso.core.docs_type import judge_document_type
 5 | from exparso.core.prompt import JAPANESE_CORE_PROMPT
 6 | from exparso.model import LlmModel, LoadPageContents
 7 |
 8 |
 9 | @pytest.fixture
10 | def page() -> LoadPageContents:
11 |     img = Image.new("RGB", (100, 100), color="red")
12 |     return LoadPageContents(contents="contents", image=img, page_number=1, tables=[])
13 |
14 |
15 | def test_docs_type(llm_model: LlmModel, page: LoadPageContents):
16 |     test_docs_type = judge_document_type(llm_model, JAPANESE_CORE_PROMPT)
17 |     assert test_docs_type.invoke(page)
18 |


--------------------------------------------------------------------------------
/tests/integrate/core/test_parse_document.py:
--------------------------------------------------------------------------------
 1 | import pytest
 2 | from PIL import Image
 3 |
 4 | from exparso.core.parse.parse_document import parse_document
 5 | from exparso.core.prompt import JAPANESE_CORE_PROMPT
 6 | from exparso.core.type import ContextData, DocumentTypeEnum, InputParseDocument
 7 | from exparso.model import Cost, LlmModel, LoadPageContents
 8 |
 9 |
10 | @pytest.fixture
11 | def page() -> LoadPageContents:
12 |     img = Image.new("RGB", (100, 100), color="red")
13 |     return LoadPageContents(contents="contents", image=img, page_number=1, tables=[])
14 |
15 |
16 | def test_parse_document(llm_model: LlmModel, page: LoadPageContents):
17 |     input = InputParseDocument(
18 |         page=page,
19 |         context=ContextData(path="path", cost=Cost.zero_cost(), content="content"),
20 |         document_type=[DocumentTypeEnum.IMAGE],
21 |     )
22 |     model = parse_document(llm_model, JAPANESE_CORE_PROMPT)
23 |     assert model.invoke(input)
24 |


--------------------------------------------------------------------------------
/tests/integrate/core/test_update_context.py:
--------------------------------------------------------------------------------
 1 | from exparso.core.context import update_context
 2 | from exparso.core.prompt import JAPANESE_CORE_PROMPT
 3 | from exparso.core.type import ContextData, ParseDocument
 4 | from exparso.model import Cost, LlmModel, PageContents
 5 |
 6 |
 7 | def test_update_context(llm_model: LlmModel):
 8 |     context = ContextData(
 9 |         path="名簿.xlsx",
10 |         content="",
11 |         cost=Cost.zero_cost(),
12 |     )
13 |     new_page = PageContents(
14 |         contents="たなか けんじ 男 30歳\nやまだ さちこ 女 25歳\n",
15 |         page_number=1,
16 |     )
17 |     data = ParseDocument(
18 |         new_page=new_page,
19 |         context=context,
20 |     )
21 |     model = update_context(llm_model, prompt=JAPANESE_CORE_PROMPT)
22 |     context = model.invoke(data)
23 |     assert context
24 |     assert context.cost.input_token > 0
25 |     assert context.content
26 |     assert context.path == "名簿.xlsx"
27 |


--------------------------------------------------------------------------------
/tests/integrate/llm/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/integrate/llm/__init__.py


--------------------------------------------------------------------------------
/tests/integrate/llm/conftest.py:
--------------------------------------------------------------------------------
1 | import pytest
2 | from PIL import Image
3 |
4 |
5 | @pytest.fixture
6 | def example_image():
7 |     img = Image.new("RGB", (100, 100), color="red")
8 |     return img
9 |


--------------------------------------------------------------------------------
/tests/integrate/llm/test_claude.py:
--------------------------------------------------------------------------------
 1 | from langchain_google_vertexai.model_garden import ChatAnthropicVertex
 2 |
 3 | from exparso.llm.claude import generate_claude_llm
 4 | from exparso.model import HumanMessage, Image, SystemMessage
 5 |
 6 |
 7 | def test_chat_anthropic_vertex(chat_anthropic_vertex: ChatAnthropicVertex):
 8 |     model = generate_claude_llm(chat_anthropic_vertex)
 9 |     response = model.invoke(
10 |         [
11 |             SystemMessage(
12 |                 content='# Output\n以下のJson形式に従って下さい\n"answer":str',
13 |             ),
14 |             HumanMessage(content="京都は日本の首都ですか?"),
15 |         ]
16 |     )
17 |     assert response
18 |     assert response.cost.input_token > 0
19 |     assert response.cost.output_token > 0
20 |     assert response.content
21 |     assert "answer" in response.content
22 |
23 |
24 | def test_chat_anthropic_vertex_with_image(example_image: Image, chat_anthropic_vertex: ChatAnthropicVertex):
25 |     model = generate_claude_llm(chat_anthropic_vertex)
26 |     response = model.invoke(
27 |         [
28 |             SystemMessage(
29 |                 content="あなたは博識です" + '# Output\n以下のJson形式に従って下さい\n"answer":str',
30 |             ),
31 |             HumanMessage(content="これは何色ですか", image=example_image, image_low=True),
32 |         ]
33 |     )
34 |     assert response
35 |     assert response.cost.input_token > 0
36 |     assert response.cost.output_token > 0
37 |     assert response.content
38 |     assert "answer" in response.content
39 |


--------------------------------------------------------------------------------
/tests/integrate/llm/test_gemini.py:
--------------------------------------------------------------------------------
 1 | from langchain_google_vertexai import ChatVertexAI
 2 |
 3 | from exparso.llm.gemini import generate_gemini_llm
 4 | from exparso.model import HumanMessage, Image, SystemMessage
 5 |
 6 |
 7 | def test_gemini_vertexai(chat_vertex_ai: ChatVertexAI):
 8 |     gemini = generate_gemini_llm(chat_vertex_ai)
 9 |     response = gemini.invoke(
10 |         [
11 |             SystemMessage(
12 |                 content="京都は日本の首都ですか" + '\n# Output\n以下のJson形式に従って下さい\n{"answer":str}'
13 |             ),
14 |         ]
15 |     )
16 |     assert response
17 |     assert response.cost.input_token > 0
18 |     assert response.cost.output_token > 0
19 |     assert response.cost.llm_model_name
20 |     assert "answer" in response.content
21 |
22 |
23 | def test_gemini_vertexai_with_image(example_image: Image, chat_vertex_ai: ChatVertexAI):
24 |     gemini = generate_gemini_llm(chat_vertex_ai)
25 |     response = gemini.invoke(
26 |         [
27 |             SystemMessage(content='あなたは博識です\n # Output\n以下のJson形式に従って下さい\n"answer":str'),
28 |             HumanMessage(content="これは何色ですか", image=example_image, image_low=True),
29 |         ]
30 |     )
31 |     assert response
32 |     assert response.cost.input_token > 0
33 |     assert response.cost.output_token > 0
34 |     assert "answer" in response.content
35 |


--------------------------------------------------------------------------------
/tests/integrate/llm/test_openai.py:
--------------------------------------------------------------------------------
 1 | from langchain_openai import AzureChatOpenAI
 2 |
 3 | from exparso.llm.openai import generate_openai_llm
 4 | from exparso.model import HumanMessage, Image, SystemMessage
 5 |
 6 |
 7 | def test_aoai(azure_chat_openai: AzureChatOpenAI):
 8 |     aoai = generate_openai_llm(azure_chat_openai)
 9 |     response = aoai.invoke(
10 |         [
11 |             SystemMessage(content="京都は日本の首都ですか" + '# Output\n以下のJson形式に従って下さい\n{"answer":str}'),
12 |         ]
13 |     )
14 |     assert response
15 |     assert response.cost.input_token > 0
16 |     assert response.cost.output_token > 0
17 |     assert "gpt-4o" in response.cost.llm_model_name
18 |     assert "answer" in response.content
19 |
20 |
21 | def test_aoai_with_image(example_image: Image, azure_chat_openai: AzureChatOpenAI):
22 |     aoai = generate_openai_llm(azure_chat_openai)
23 |     response = aoai.invoke(
24 |         [
25 |             SystemMessage(content="あなたは博識です" + '# Output\n以下のJson形式に従って下さい\n{"answer":str}'),
26 |             HumanMessage(content="これは何色ですか", image=example_image, image_low=True),
27 |         ],
28 |     )
29 |     assert response
30 |     assert response.cost.input_token > 0
31 |     assert response.cost.output_token > 0
32 |     assert "gpt-4o" in response.cost.llm_model_name
33 |     assert "answer" in response.content
34 |


--------------------------------------------------------------------------------
/tests/integrate/loader/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/integrate/loader/__init__.py


--------------------------------------------------------------------------------
/tests/integrate/loader/test_docx_loader.py:
--------------------------------------------------------------------------------
1 | from exparso.loader.docx_loader import DocxLoader
2 | from tests.constants import DOCX_DOCUMENT
3 |
4 |
5 | def test_docx_loader():
6 |     loader = DocxLoader()
7 |     pages = loader.load(DOCX_DOCUMENT)
8 |     assert len(pages) == 1
9 |


--------------------------------------------------------------------------------
/tests/integrate/loader/test_pptx_loader.py:
--------------------------------------------------------------------------------
1 | from exparso.loader.pptx_loader import PptxLoader
2 | from tests.constants import PPTX_DOCUMENT
3 |
4 |
5 | def test_pptx_loader():
6 |     loader = PptxLoader()
7 |     pages = loader.load(PPTX_DOCUMENT)
8 |     assert len(pages) == 3
9 |


--------------------------------------------------------------------------------
/tests/integrate/test_error.py:
--------------------------------------------------------------------------------
 1 | import pytest
 2 |
 3 | from exparso import parse_document
 4 | from tests.constants import PDF_TABLE_DOCUMENT
 5 |
 6 |
 7 | def test_not_exist_file():
 8 |     with pytest.raises(FileNotFoundError):
 9 |         parse_document("not_exist_file.txt")
10 |
11 |
12 | def test_not_support_model():
13 |     with pytest.raises(ValueError):
14 |         parse_document(PDF_TABLE_DOCUMENT, "not_support_model")  # type: ignore
15 |
16 |
17 | def test_not_support_extension():
18 |     with pytest.raises(ValueError):
19 |         parse_document(__file__)
20 |


--------------------------------------------------------------------------------
/tests/integrate/test_model_aoai.py:
--------------------------------------------------------------------------------
 1 | from langchain_openai import AzureChatOpenAI
 2 |
 3 | from exparso import parse_document
 4 | from tests.constants import (
 5 |     BMP_DOCUMENT,
 6 |     CSV_DOCUMENT,
 7 |     DOCX_DOCUMENT,
 8 |     JPEG_DOCUMENT,
 9 |     MARKDOWN_TEXT_DOCUMENT,
10 |     PDF_TABLE_DOCUMENT,
11 |     PPTX_DOCUMENT,
12 |     XLSX_DOCUMENT,
13 | )
14 |
15 |
16 | def test_model_aoai_with_pdf(azure_chat_openai: AzureChatOpenAI):
17 |     documents = parse_document(PDF_TABLE_DOCUMENT, azure_chat_openai)
18 |     assert documents
19 |
20 |
21 | def test_model_aoai_with_text(azure_chat_openai: AzureChatOpenAI):
22 |     documents = parse_document(MARKDOWN_TEXT_DOCUMENT, azure_chat_openai)
23 |     assert documents
24 |
25 |
26 | def test_model_aoai_with_jpg(azure_chat_openai: AzureChatOpenAI):
27 |     documents = parse_document(JPEG_DOCUMENT, azure_chat_openai)
28 |     assert documents
29 |
30 |
31 | def test_model_aoai_with_bmp(azure_chat_openai: AzureChatOpenAI):
32 |     documents = parse_document(BMP_DOCUMENT, azure_chat_openai)
33 |     assert documents
34 |
35 |
36 | def test_model_aoai_with_csv(azure_chat_openai: AzureChatOpenAI):
37 |     documents = parse_document(CSV_DOCUMENT, azure_chat_openai)
38 |     assert documents
39 |
40 |
41 | def test_model_aoai_with_xlsx(azure_chat_openai: AzureChatOpenAI):
42 |     documents = parse_document(XLSX_DOCUMENT, azure_chat_openai)
43 |     assert documents
44 |
45 |
46 | def test_model_aoai_with_pptx(azure_chat_openai: AzureChatOpenAI):
47 |     documents = parse_document(PPTX_DOCUMENT, azure_chat_openai)
48 |     assert documents
49 |
50 |
51 | def test_model_aoai_with_docx(azure_chat_openai: AzureChatOpenAI):
52 |     documents = parse_document(DOCX_DOCUMENT, azure_chat_openai)
53 |     assert documents
54 |


--------------------------------------------------------------------------------
/tests/integrate/test_model_claude.py:
--------------------------------------------------------------------------------
 1 | import pytest
 2 | from langchain_google_vertexai.model_garden import ChatAnthropicVertex
 3 |
 4 | from exparso import parse_document
 5 | from tests.constants import (
 6 |     BMP_DOCUMENT,
 7 |     CSV_DOCUMENT,
 8 |     DOCX_DOCUMENT,
 9 |     JPEG_DOCUMENT,
10 |     MARKDOWN_TEXT_DOCUMENT,
11 |     PDF_TABLE_DOCUMENT,
12 |     PPTX_DOCUMENT,
13 |     XLSX_DOCUMENT,
14 | )
15 |
16 |
17 | def test_model_claude_with_pdf(chat_anthropic_vertex: ChatAnthropicVertex):
18 |     documents = parse_document(PDF_TABLE_DOCUMENT, chat_anthropic_vertex)
19 |     assert documents
20 |
21 |
22 | @pytest.mark.skip(reason="API料金の節約")
23 | def test_model_claude_with_text(chat_anthropic_vertex: ChatAnthropicVertex):
24 |     documents = parse_document(MARKDOWN_TEXT_DOCUMENT, chat_anthropic_vertex)
25 |     assert documents
26 |
27 |
28 | @pytest.mark.skip(reason="API料金の節約")
29 | def test_model_claude_with_jpg(chat_anthropic_vertex: ChatAnthropicVertex):
30 |     documents = parse_document(JPEG_DOCUMENT, chat_anthropic_vertex)
31 |     assert documents
32 |
33 |
34 | @pytest.mark.skip(reason="API料金の節約")
35 | def test_model_claude_with_bmp(chat_anthropic_vertex: ChatAnthropicVertex):
36 |     documents = parse_document(BMP_DOCUMENT, chat_anthropic_vertex)
37 |     assert documents
38 |
39 |
40 | def test_model_claude_with_csv(chat_anthropic_vertex: ChatAnthropicVertex):
41 |     documents = parse_document(CSV_DOCUMENT, chat_anthropic_vertex)
42 |     assert documents
43 |
44 |
45 | def test_model_claude_with_xlsx(chat_anthropic_vertex: ChatAnthropicVertex):
46 |     documents = parse_document(XLSX_DOCUMENT, chat_anthropic_vertex)
47 |     assert documents
48 |
49 |
50 | @pytest.mark.skip(reason="API料金の節約")
51 | def test_model_claude_with_pptx(chat_anthropic_vertex: ChatAnthropicVertex):
52 |     documents = parse_document(PPTX_DOCUMENT, chat_anthropic_vertex)
53 |     assert documents
54 |
55 |
56 | @pytest.mark.skip(reason="API料金の節約")
57 | def test_model_claude_with_docx(chat_anthropic_vertex: ChatAnthropicVertex):
58 |     documents = parse_document(DOCX_DOCUMENT, chat_anthropic_vertex)
59 |     assert documents
60 |


--------------------------------------------------------------------------------
/tests/integrate/test_model_gemini.py:
--------------------------------------------------------------------------------
 1 | import pytest
 2 | from langchain_google_vertexai import ChatVertexAI
 3 |
 4 | from exparso import parse_document
 5 | from tests.constants import (
 6 |     BMP_DOCUMENT,
 7 |     CSV_DOCUMENT,
 8 |     DOCX_DOCUMENT,
 9 |     JPEG_DOCUMENT,
10 |     MARKDOWN_TEXT_DOCUMENT,
11 |     PDF_TABLE_DOCUMENT,
12 |     PPTX_DOCUMENT,
13 |     XLSX_DOCUMENT,
14 | )
15 |
16 |
17 | def test_model_gemini_with_pdf(chat_vertex_ai: ChatVertexAI):
18 |     documents = parse_document(PDF_TABLE_DOCUMENT, chat_vertex_ai)
19 |     assert documents
20 |
21 |
22 | @pytest.mark.skip(reason="API料金の節約")
23 | def test_model_gemini_with_text(chat_vertex_ai: ChatVertexAI):
24 |     documents = parse_document(MARKDOWN_TEXT_DOCUMENT, chat_vertex_ai)
25 |     assert documents
26 |
27 |
28 | @pytest.mark.skip(reason="API料金の節約")
29 | def test_model_gemini_with_jpg(chat_vertex_ai: ChatVertexAI):
30 |     documents = parse_document(JPEG_DOCUMENT, chat_vertex_ai)
31 |     assert documents
32 |
33 |
34 | @pytest.mark.skip(reason="API料金の節約")
35 | def test_model_gemini_with_bmp(chat_vertex_ai: ChatVertexAI):
36 |     documents = parse_document(BMP_DOCUMENT, chat_vertex_ai)
37 |     assert documents
38 |
39 |
40 | def test_model_gemini_with_csv(chat_vertex_ai: ChatVertexAI):
41 |     documents = parse_document(CSV_DOCUMENT, chat_vertex_ai)
42 |     assert documents
43 |
44 |
45 | def test_model_gemini_with_xlsx(chat_vertex_ai: ChatVertexAI):
46 |     documents = parse_document(XLSX_DOCUMENT, chat_vertex_ai)
47 |     assert documents
48 |
49 |
50 | @pytest.mark.skip(reason="API料金の節約")
51 | def test_model_gemini_with_pptx(chat_vertex_ai: ChatVertexAI):
52 |     documents = parse_document(PPTX_DOCUMENT, chat_vertex_ai)
53 |     assert documents
54 |
55 |
56 | @pytest.mark.skip(reason="API料金の節約")
57 | def test_model_gemini_with_docx(chat_vertex_ai: ChatVertexAI):
58 |     documents = parse_document(DOCX_DOCUMENT, chat_vertex_ai)
59 |     assert documents
60 |


--------------------------------------------------------------------------------
/tests/integrate/test_model_none.py:
--------------------------------------------------------------------------------
 1 | from exparso import parse_document
 2 | from tests.constants import (
 3 |     BMP_DOCUMENT,
 4 |     CSV_DOCUMENT,
 5 |     DOCX_DOCUMENT,
 6 |     JPEG_DOCUMENT,
 7 |     MARKDOWN_TEXT_DOCUMENT,
 8 |     PDF_TABLE_DOCUMENT,
 9 |     PPTX_DOCUMENT,
10 |     XLSX_DOCUMENT,
11 | )
12 |
13 |
14 | def test_model_none_with_pdf():
15 |     documents = parse_document(PDF_TABLE_DOCUMENT)
16 |     assert documents
17 |
18 |
19 | def test_model_none_with_text():
20 |     documents = parse_document(MARKDOWN_TEXT_DOCUMENT)
21 |     assert documents
22 |
23 |
24 | def test_model_none_with_jpg():
25 |     documents = parse_document(JPEG_DOCUMENT)
26 |     assert documents
27 |
28 |
29 | def test_model_none_with_bmp():
30 |     documents = parse_document(BMP_DOCUMENT)
31 |     assert documents
32 |
33 |
34 | def test_model_none_with_csv():
35 |     documents = parse_document(CSV_DOCUMENT)
36 |     assert documents
37 |
38 |
39 | def test_model_none_with_xlsx():
40 |     documents = parse_document(XLSX_DOCUMENT)
41 |     assert documents
42 |
43 |
44 | def test_model_none_with_pptx():
45 |     documents = parse_document(PPTX_DOCUMENT)
46 |     assert documents
47 |
48 |
49 | def test_model_none_with_docx():
50 |     documents = parse_document(DOCX_DOCUMENT)
51 |     assert documents
52 |


--------------------------------------------------------------------------------
/tests/unit/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/unit/__init__.py


--------------------------------------------------------------------------------
/tests/unit/core/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/unit/core/__init__.py


--------------------------------------------------------------------------------
/tests/unit/core/prompt/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/unit/core/prompt/__init__.py


--------------------------------------------------------------------------------
/tests/unit/core/prompt/test_prompt.py:
--------------------------------------------------------------------------------
  1 | import pytest
  2 | from pydantic import ValidationError
  3 |
  4 | from exparso.core.prompt.prompt import CorePrompt
  5 |
  6 |
  7 | def test_core_prompt_valid():
  8 |     """Test creating a valid CorePrompt instance."""
  9 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
 10 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
 11 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
 12 |     extract_doc_text = "Here is the document text: {document_text}"
 13 |     extract_img_only = "Image only document"
 14 |
 15 |     prompt = CorePrompt(
 16 |         judge_document_type=judge_doc_type,
 17 |         extract_document=extract_doc,
 18 |         update_context=update_ctx,
 19 |         table_prompt="Table prompt",
 20 |         flowchart_prompt="Flowchart prompt",
 21 |         graph_prompt="Graph prompt",
 22 |         image_prompt="Image prompt",
 23 |         extract_document_text_prompt=extract_doc_text,
 24 |         extract_image_only_prompt=extract_img_only,
 25 |     )
 26 |     # Check judge_document_type placeholders
 27 |     assert "{types_explanation}" in prompt.judge_document_type
 28 |     assert "{format_instructions}" in prompt.judge_document_type
 29 |
 30 |     # Check extract_document placeholders
 31 |     assert "{document_type_prompt}" in prompt.extract_document
 32 |     assert "{context}" in prompt.extract_document
 33 |     assert "{format_instruction}" in prompt.extract_document
 34 |
 35 |     # Check update_context placeholders
 36 |     assert "{context}" in prompt.update_context
 37 |     assert "{format_instructions}" in prompt.update_context
 38 |
 39 |     # Check extract_document_text_prompt placeholder
 40 |     assert "{document_text}" in prompt.extract_document_text_prompt
 41 |
 42 |
 43 | def test_judge_document_type_missing_types_explanation():
 44 |     """Test validation error when {types_explanation} is missing in judge_document_type."""
 45 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
 46 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
 47 |     extract_doc_text = "Here is the document text: {document_text}"
 48 |     extract_img_only = "Image only document"
 49 |
 50 |     with pytest.raises(ValidationError) as excinfo:
 51 |         CorePrompt(
 52 |             judge_document_type="Format: {format_instructions}",
 53 |             extract_document=extract_doc,
 54 |             update_context=update_ctx,
 55 |             table_prompt="Table prompt",
 56 |             flowchart_prompt="Flowchart prompt",
 57 |             graph_prompt="Graph prompt",
 58 |             image_prompt="Image prompt",
 59 |             extract_document_text_prompt=extract_doc_text,
 60 |             extract_image_only_prompt=extract_img_only,
 61 |         )
 62 |
 63 |     # Check that the error message contains the expected text
 64 |     error_msg = str(excinfo.value)
 65 |     assert "The string must contain '{types_explanation}'" in error_msg
 66 |
 67 |
 68 | def test_judge_document_type_missing_format_instructions():
 69 |     """Test validation error when {format_instructions} is missing in judge_document_type."""
 70 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
 71 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
 72 |     extract_doc_text = "Here is the document text: {document_text}"
 73 |     extract_img_only = "Image only document"
 74 |
 75 |     with pytest.raises(ValidationError) as excinfo:
 76 |         CorePrompt(
 77 |             judge_document_type="Types: {types_explanation}",
 78 |             extract_document=extract_doc,
 79 |             update_context=update_ctx,
 80 |             table_prompt="Table prompt",
 81 |             flowchart_prompt="Flowchart prompt",
 82 |             graph_prompt="Graph prompt",
 83 |             image_prompt="Image prompt",
 84 |             extract_document_text_prompt=extract_doc_text,
 85 |             extract_image_only_prompt=extract_img_only,
 86 |         )
 87 |
 88 |     # Check that the error message contains the expected text
 89 |     error_msg = str(excinfo.value)
 90 |     assert "The string must contain '{format_instructions}'" in error_msg
 91 |
 92 |
 93 | def test_extract_document_missing_document_type_prompt():
 94 |     """Test validation error when {document_type_prompt} is missing in extract_document."""
 95 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
 96 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
 97 |     extract_doc_text = "Here is the document text: {document_text}"
 98 |     extract_img_only = "Image only document"
 99 |
100 |     with pytest.raises(ValidationError) as excinfo:
101 |         CorePrompt(
102 |             judge_document_type=judge_doc_type,
103 |             extract_document="Context: {context}\nFormat: {format_instruction}",
104 |             update_context=update_ctx,
105 |             table_prompt="Table prompt",
106 |             flowchart_prompt="Flowchart prompt",
107 |             graph_prompt="Graph prompt",
108 |             image_prompt="Image prompt",
109 |             extract_document_text_prompt=extract_doc_text,
110 |             extract_image_only_prompt=extract_img_only,
111 |         )
112 |
113 |     # Check that the error message contains the expected text
114 |     error_msg = str(excinfo.value)
115 |     assert "The string must contain '{document_type_prompt}'" in error_msg
116 |
117 |
118 | def test_extract_document_missing_context():
119 |     """Test validation error when {context} is missing in extract_document."""
120 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
121 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
122 |     extract_doc_text = "Here is the document text: {document_text}"
123 |     extract_img_only = "Image only document"
124 |
125 |     with pytest.raises(ValidationError) as excinfo:
126 |         CorePrompt(
127 |             judge_document_type=judge_doc_type,
128 |             extract_document="Document type: {document_type_prompt}\nFormat: {format_instruction}",
129 |             update_context=update_ctx,
130 |             table_prompt="Table prompt",
131 |             flowchart_prompt="Flowchart prompt",
132 |             graph_prompt="Graph prompt",
133 |             image_prompt="Image prompt",
134 |             extract_document_text_prompt=extract_doc_text,
135 |             extract_image_only_prompt=extract_img_only,
136 |         )
137 |
138 |     # Check that the error message contains the expected text
139 |     error_msg = str(excinfo.value)
140 |     assert "The string must contain '{context}'" in error_msg
141 |
142 |
143 | def test_extract_document_missing_format_instruction():
144 |     """Test validation error when {format_instruction} is missing in extract_document."""
145 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
146 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
147 |     extract_doc_text = "Here is the document text: {document_text}"
148 |     extract_img_only = "Image only document"
149 |
150 |     with pytest.raises(ValidationError) as excinfo:
151 |         CorePrompt(
152 |             judge_document_type=judge_doc_type,
153 |             extract_document="Document type: {document_type_prompt}\nContext: {context}",
154 |             update_context=update_ctx,
155 |             table_prompt="Table prompt",
156 |             flowchart_prompt="Flowchart prompt",
157 |             graph_prompt="Graph prompt",
158 |             image_prompt="Image prompt",
159 |             extract_document_text_prompt=extract_doc_text,
160 |             extract_image_only_prompt=extract_img_only,
161 |         )
162 |
163 |     # Check that the error message contains the expected text
164 |     error_msg = str(excinfo.value)
165 |     assert "The string must contain '{format_instruction}'" in error_msg
166 |
167 |
168 | def test_update_context_missing_context():
169 |     """Test validation error when {context} is missing in update_context."""
170 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
171 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
172 |     extract_doc_text = "Here is the document text: {document_text}"
173 |     extract_img_only = "Image only document"
174 |
175 |     with pytest.raises(ValidationError) as excinfo:
176 |         CorePrompt(
177 |             judge_document_type=judge_doc_type,
178 |             extract_document=extract_doc,
179 |             update_context="Format instructions: {format_instructions}",
180 |             table_prompt="Table prompt",
181 |             flowchart_prompt="Flowchart prompt",
182 |             graph_prompt="Graph prompt",
183 |             image_prompt="Image prompt",
184 |             extract_document_text_prompt=extract_doc_text,
185 |             extract_image_only_prompt=extract_img_only,
186 |         )
187 |
188 |     # Check that the error message contains the expected text
189 |     error_msg = str(excinfo.value)
190 |     assert "The string must contain '{context}'" in error_msg
191 |
192 |
193 | def test_update_context_missing_format_instructions():
194 |     """Test validation error when {format_instructions} is missing in update_context."""
195 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
196 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
197 |     extract_doc_text = "Here is the document text: {document_text}"
198 |     extract_img_only = "Image only document"
199 |
200 |     with pytest.raises(ValidationError) as excinfo:
201 |         CorePrompt(
202 |             judge_document_type=judge_doc_type,
203 |             extract_document=extract_doc,
204 |             update_context="Here is the context: {context}",
205 |             table_prompt="Table prompt",
206 |             flowchart_prompt="Flowchart prompt",
207 |             graph_prompt="Graph prompt",
208 |             image_prompt="Image prompt",
209 |             extract_document_text_prompt=extract_doc_text,
210 |             extract_image_only_prompt=extract_img_only,
211 |         )
212 |
213 |     # Check that the error message contains the expected text
214 |     error_msg = str(excinfo.value)
215 |     assert "The string must contain '{format_instructions}'" in error_msg
216 |
217 |
218 | def test_extract_document_text_prompt_missing_document_text():
219 |     """Test validation error when {document_text} is missing in extract_document_text_prompt."""
220 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
221 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
222 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
223 |     extract_img_only = "Image only document"
224 |
225 |     with pytest.raises(ValidationError) as excinfo:
226 |         CorePrompt(
227 |             judge_document_type=judge_doc_type,
228 |             extract_document=extract_doc,
229 |             update_context=update_ctx,
230 |             table_prompt="Table prompt",
231 |             flowchart_prompt="Flowchart prompt",
232 |             graph_prompt="Graph prompt",
233 |             image_prompt="Image prompt",
234 |             extract_document_text_prompt="Missing document text placeholder",
235 |             extract_image_only_prompt=extract_img_only,
236 |         )
237 |
238 |     # Check that the error message contains the expected text
239 |     error_msg = str(excinfo.value)
240 |     assert "The string must contain '{document_text}'" in error_msg
241 |
242 |
243 | def test_extract_human_message():
244 |     """Test the extract_human_message method."""
245 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
246 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
247 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
248 |     extract_doc_text = "Here is the document text: {document_text}"
249 |     extract_img_only = "Image only document"
250 |
251 |     prompt = CorePrompt(
252 |         judge_document_type=judge_doc_type,
253 |         extract_document=extract_doc,
254 |         update_context=update_ctx,
255 |         table_prompt="Table prompt",
256 |         flowchart_prompt="Flowchart prompt",
257 |         graph_prompt="Graph prompt",
258 |         image_prompt="Image prompt",
259 |         extract_document_text_prompt=extract_doc_text,
260 |         extract_image_only_prompt=extract_img_only,
261 |     )
262 |
263 |     # Test with document text
264 |     document_text = "Sample document text"
265 |     message = prompt.extract_human_message(document_text)
266 |     assert document_text in message
267 |     assert message == extract_doc_text.format(document_text=document_text)
268 |
269 |     # Test with empty document text
270 |     empty_document_text = ""
271 |     message = prompt.extract_human_message(empty_document_text)
272 |     assert message == extract_img_only.format(document_text=empty_document_text)
273 |
274 |
275 | def test_model_is_frozen():
276 |     """Test that the model is frozen (immutable)."""
277 |     judge_doc_type = "Types: {types_explanation}\nFormat: {format_instructions}"
278 |     extract_doc = "Document type: {document_type_prompt}\nContext: {context}\nFormat: {format_instruction}"
279 |     update_ctx = "Here is the context: {context}\nFormat instructions: {format_instructions}"
280 |     extract_doc_text = "Here is the document text: {document_text}"
281 |     extract_img_only = "Image only document"
282 |
283 |     prompt = CorePrompt(
284 |         judge_document_type=judge_doc_type,
285 |         extract_document=extract_doc,
286 |         update_context=update_ctx,
287 |         table_prompt="Table prompt",
288 |         flowchart_prompt="Flowchart prompt",
289 |         graph_prompt="Graph prompt",
290 |         image_prompt="Image prompt",
291 |         extract_document_text_prompt=extract_doc_text,
292 |         extract_image_only_prompt=extract_img_only,
293 |     )
294 |
295 |     # Attempting to modify the model should raise an error
296 |     # Pydantic v2 raises ValidationError for frozen instances
297 |     with pytest.raises(Exception) as excinfo:
298 |         prompt.table_prompt = "New table prompt"
299 |
300 |     # Check that the error message indicates the instance is frozen
301 |     assert "frozen" in str(excinfo.value).lower()
302 |


--------------------------------------------------------------------------------
/tests/unit/llm/__Init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/unit/llm/__Init__.py


--------------------------------------------------------------------------------
/tests/unit/llm/test_llm_factory.py:
--------------------------------------------------------------------------------
 1 | import os
 2 |
 3 | import vertexai
 4 | from langchain_google_vertexai import ChatVertexAI
 5 | from langchain_google_vertexai.model_garden import ChatAnthropicVertex
 6 | from langchain_openai import AzureChatOpenAI, ChatOpenAI
 7 |
 8 | from exparso.llm.llm_factory import LlmFactory
 9 |
10 |
11 | def test_azure_chat_openai():
12 |     os.environ["AZURE_OPENAI_API_KEY"] = "dummy"
13 |     os.environ["OPENAI_API_VERSION"] = "2023-05-15"
14 |     os.environ["AZURE_OPENAI_ENDPOINT"] = "dummy"
15 |     model = AzureChatOpenAI()
16 |     assert model.__class__.__name__ == "AzureChatOpenAI"
17 |     llm = LlmFactory.create(model)
18 |     assert llm
19 |
20 |
21 | def test_chat_openai():
22 |     model = ChatOpenAI(api_key="dummy")  # type: ignore
23 |     assert model.__class__.__name__ == "ChatOpenAI"
24 |     llm = LlmFactory.create(model)
25 |     assert llm
26 |
27 |
28 | def test_chat_anthropic_vertex():
29 |     llm = ChatAnthropicVertex(
30 |         model_name="dummy-model",
31 |         location="dummy-location",
32 |         project="dummy-project",
33 |     )
34 |
35 |     model = LlmFactory.create(llm)
36 |     assert model
37 |
38 |
39 | def test_chat_vertextai():
40 |     vertexai.init(project="dummy-project", location="us-east1")
41 |     llm = ChatVertexAI(model_name="dummy-model")
42 |     model = LlmFactory.create(llm)
43 |     assert model
44 |


--------------------------------------------------------------------------------
/tests/unit/loader/__Init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/unit/loader/__Init__.py


--------------------------------------------------------------------------------
/tests/unit/loader/test_csv_loader.py:
--------------------------------------------------------------------------------
 1 | from exparso.loader.csv_loader import CsvLoader
 2 | from tests.constants import CSV_DOCUMENT
 3 |
 4 |
 5 | def test_csv_loader():
 6 |     loader = CsvLoader()
 7 |     pages = loader.load(CSV_DOCUMENT)
 8 |     assert len(pages) == 1
 9 |     assert pages[0].page_number == 0
10 |     assert pages[0].image is None
11 |     assert pages[0].tables == [
12 |         [
13 |             ["Name", "Age", "Occupation"],
14 |             ["Alice", "30", "Engineer"],
15 |             ["Bob", "25", "Designer"],
16 |             ["Charlie", "35", "Manager"],
17 |         ]
18 |     ]
19 |


--------------------------------------------------------------------------------
/tests/unit/loader/test_image_loader.py:
--------------------------------------------------------------------------------
 1 | from exparso.loader.image_loader import ImageLoader
 2 | from tests.constants import BMP_DOCUMENT, JPEG_DOCUMENT
 3 |
 4 |
 5 | def test_image_loader_jpg():
 6 |     loader = ImageLoader()
 7 |     pages = loader.load(JPEG_DOCUMENT)
 8 |     assert len(pages) == 1
 9 |     assert pages[0].page_number == 0
10 |     assert pages[0].image is not None
11 |     assert pages[0].tables == []
12 |
13 |
14 | def test_image_loader_bmp():
15 |     loader = ImageLoader()
16 |     pages = loader.load(BMP_DOCUMENT)
17 |     assert len(pages) == 1
18 |     assert pages[0].page_number == 0
19 |     assert pages[0].image is not None
20 |     assert pages[0].tables == []
21 |


--------------------------------------------------------------------------------
/tests/unit/loader/test_pdf_loader.py:
--------------------------------------------------------------------------------
 1 | from exparso.loader.pdf_loader import PdfLoader
 2 | from tests.constants import PDF_TABLE_DOCUMENT
 3 |
 4 |
 5 | def test_pdf_loader_with_tables():
 6 |     loader = PdfLoader()
 7 |     pages = loader.load(PDF_TABLE_DOCUMENT)
 8 |     assert len(pages) == 2
 9 |     assert pages[0].page_number == 0
10 |     assert pages[0].image
11 |     assert pages[0].tables
12 |
13 |     assert pages[1].page_number == 1
14 |     assert pages[1].image
15 |     assert pages[1].tables
16 |


--------------------------------------------------------------------------------
/tests/unit/loader/test_text_file_loader.py:
--------------------------------------------------------------------------------
 1 | from exparso.loader.text_file_loader import TextFileLoader
 2 | from tests.constants import MARKDOWN_TEXT_DOCUMENT
 3 |
 4 |
 5 | def test_text_file_loader():
 6 |     loader = TextFileLoader()
 7 |     pages = loader.load(MARKDOWN_TEXT_DOCUMENT)
 8 |     assert len(pages) == 1
 9 |     assert pages[0].page_number == 0
10 |     assert pages[0].image is None
11 |     assert pages[0].tables == []
12 |


--------------------------------------------------------------------------------
/tests/unit/loader/test_xlsx_loader.py:
--------------------------------------------------------------------------------
 1 | from exparso.loader.xlsx_loader import XlsxLoader
 2 | from tests.constants import XLSX_DOCUMENT
 3 |
 4 |
 5 | def test_csv_loader():
 6 |     loader = XlsxLoader()
 7 |     pages = loader.load(XLSX_DOCUMENT)
 8 |     assert len(pages) == 2
 9 |     assert pages[0].page_number == 0
10 |     assert pages[0].image is None
11 |     assert pages[0].tables == [
12 |         [["Name", "Age", "Occpation"], ["John", 33, "Engineer"], ["Bob", 29, "Designer"], ["Alice", 49, "Manager"]]
13 |     ]
14 |     assert pages[0].contents.startswith("Sheet1\n")
15 |


--------------------------------------------------------------------------------
/tests/unit/model/__init__.py:
--------------------------------------------------------------------------------
https://raw.githubusercontent.com/InsightEdgeJP/exparso/7d254361ec256df51fadbf0fd40330a671d29c8b/tests/unit/model/__init__.py


--------------------------------------------------------------------------------
/tests/unit/model/test_document.py:
--------------------------------------------------------------------------------
 1 | from exparso.model import Cost, Document, PageContents
 2 |
 3 |
 4 | def test_document():
 5 |     document = Document(
 6 |         contents=[
 7 |             PageContents(
 8 |                 contents="",
 9 |                 page_number=0,
10 |             )
11 |         ],
12 |         cost=Cost(input_token=0, output_token=0, llm_model_name="aoai"),
13 |     )
14 |     assert document.contents
15 |


--------------------------------------------------------------------------------
/tests/unit/model/test_llm_model.py:
--------------------------------------------------------------------------------
 1 | from PIL import Image as PILImage
 2 |
 3 | from exparso.model import HumanMessage
 4 |
 5 |
 6 | def test_human_message():
 7 |     message = HumanMessage(content="Hello, World!")
 8 |     assert message.content == "Hello, World!"
 9 |     assert message.image is None
10 |
11 |
12 | def test_human_with_image():
13 |     image = PILImage.new("RGB", (100, 100))
14 |     message = HumanMessage(content="Hello, World!", image=image)
15 |     assert message.content == "Hello, World!"
16 |     image_type, base64 = message.image_base64
17 |     assert image_type.startswith("image/png")
18 |     assert base64
19 |     assert message.image_bytes
20 |
21 |
22 | def test_human_with_image_low():
23 |     image = PILImage.new("RGB", (160, 100))
24 |     message = HumanMessage(content="Hello, World!", image=image, image_low=True)
25 |     assert message.image
26 |     assert message.image.height == 100
27 |     assert message.image.width == 160
28 |     message.scale_image(0.5)
29 |     assert message.image.height == 50
30 |     assert message.image.width == 80
31 |


--------------------------------------------------------------------------------

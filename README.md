# Tetris

テトリスを題材に、プログラミングパラダイムや設計方法の違い、機能追加による変化、処理速度を比較・学習するためのプロジェクトです。

## フォルダ構成

| フォルダ | 説明 |
| --- | --- |
| [00_base](./00_base/) | 各プログラミングパラダイムのベースとなるソースコードです。 |
| [01_RC_score_rate](./01_RC_score_rate/) | スコア機能を追加した各パラダイムの実装です。 |
| [02_RC_hard_drop](./02_RC_hard_drop/) | ハードドロップ機能を追加した各パラダイムの実装です。 |
| [03_ProcessMeasurement](./03_ProcessMeasurement/) | 各プログラミングパラダイムの処理速度を計測します。 |
| [04_ProcessMeasurement](./04_ProcessMeasurement/) | `03_ProcessMeasurement` で一部正しく計測できていなかった箇所を改修した計測用コードです。 |
| [03-01_SurveySeparationOfDuties](./03-01_SurveySeparationOfDuties/) | 責務分離を検討するための調査用実装です。 |
| [03-02_SurveyDataclass](./03-02_SurveyDataclass/) | `dataclass` の利用方法を検討するための調査用実装です。 |
| [05_ProgramLang](./05_ProgramLang/) | `rev0.2` をベースに C、C++、C# で実装し、言語ごとの処理速度を計測します。 |
| [06_update](./06_update/) | テトリスの機能を開発・更新するための実装です。 |
| [07_GUI](./07_GUI/) | GUI を実装し、GUI ライブラリや環境による違いを比較します。 |

## 設計の段階

各 `rev` は、同じ題材を異なる設計段階で実装したものです。

| バージョン | 設計方針 |
| --- | --- |
| `rev0.1` | モノリシック |
| `rev0.2` | 構造化プログラミング |
| `rev0.3` | オブジェクト指向（クラス化を行った段階） |
| `rev0.4` | オブジェクト指向（責務を分離） |
| `rev0.5` | 簡易ドメイン駆動設計（クリーンアーキテクチャ、レイヤードアーキテクチャ、Entity、Value Object） |

## サポートする OS

| OS | 対応状況 | 備考 |
| --- | --- | --- |
| Linux | サポート | Debian 13 で開発・動作確認しています。 |
| Windows | 非サポート | キー入力処理が未完成のため、動作を保証しません。 |
| macOS | 非サポート | 動作を保証しません。 |

キー入力処理は OS に依存します。Debian 13 以外の Linux ディストリビューションでも動作する可能性はありますが、すべての環境で確認したわけではありません。ターミナルや GUI ライブラリなど、実行環境ごとの条件も満たす必要があります。

## 必要な環境とライブラリ

| 対象 | 必要なもの | 用途 |
| --- | --- | --- |
| Python の CUI 版 | Python 3（標準ライブラリ） | `00_base` などの Python 実装 |
| Python の GUI 版 | Python 3、`pygame` | `07_GUI/01_pygame` |
| Python の raylib 版 | Python 3、`raylib` パッケージ（`pyray` モジュール） | `07_GUI/02_raylib/python` |
| C / C++ | CMake 3.25.1 以上、C / C++ コンパイラ | `05_ProgramLang` のビルド |
| C# | .NET 10 SDK | `05_ProgramLang/cs`、`05_ProgramLang/cs_arrayC` |
| C の raylib 版 | CMake 3.25.1 以上、C コンパイラ、raylib の開発用ライブラリと CMake パッケージ | `07_GUI/02_raylib/c` |

CUI 版や `05_ProgramLang` の各言語版は外部ライブラリを使わず、各言語の標準機能で動作します。GUI 版だけ、該当するライブラリをインストールしてください。CMake を使う C / C++ 版のコンパイラは、CMake から利用できるように設定してください。

Python の GUI 用ライブラリは、必要なものだけインストールします。

```bash
python3 -m pip install pygame
python3 -m pip install raylib
```

`raylib` は Python バインディングのパッケージ名で、コードからは `pyray` として読み込みます。C 版 raylib は別途、利用する OS のパッケージマネージャーなどで開発用ライブラリを導入し、CMake から `raylib` パッケージを検出できるようにしてください。

## 実行方法

以下はプロジェクトルートで実行する例です。Python 版は実行したいバージョンの `main.py` を指定します。

```bash
python3 00_base/rev0.2/main.py
```

### Python

例として、ベース実装と Pygame 版を実行します。

```bash
python3 00_base/rev0.2/main.py
python3 07_GUI/01_pygame/rev0.2/main.py
python3 07_GUI/02_raylib/python/rev0.2/main.py
```

### C

```bash
cmake -S 05_ProgramLang/c -B build/tetris-c
cmake --build build/tetris-c
./build/tetris-c/rev0.2/main.out
```

### C++

```bash
cmake -S 05_ProgramLang/cpp -B build/tetris-cpp
cmake --build build/tetris-cpp
./build/tetris-cpp/rev0.2/main.out
```

C の raylib GUI 版は、先に raylib の C 開発用ライブラリを導入してからビルドします。

```bash
cmake -S 07_GUI/02_raylib/c -B build/tetris-raylib-c
cmake --build build/tetris-raylib-c
./build/tetris-raylib-c/rev0.2/main.out
```

### C#

`.NET 10 SDK` をインストールしてから実行します。

```bash
dotnet run --project 05_ProgramLang/cs/rev0.2/Tetris.csproj
```

配列を C 言語風に扱う版は、プロジェクトパスを `05_ProgramLang/cs_arrayC/rev0.2/Tetris.csproj` に変更してください。

## 計測について

処理速度の結果は、実行環境や計測方法に依存します。異なる言語・設計間の比較では、各計測コードと実行条件を確認してください。

## ライセンス

[MIT License](./LICENSE) のもとで公開しています。

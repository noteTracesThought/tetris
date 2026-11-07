#---------------------------------------------
# # src配下のcppファイルを再帰検索し、ビルドする（テスト向き。運用向きではない）
#---------------------------------------------
# cmake_minimum_required(VERSION 3.10)
# project(DDDTest)

# set(CMAKE_CXX_STANDARD 17)

# file(GLOB_RECURSE SOURCES
#     src/*.cpp
# )

# add_executable(main.out ${SOURCES})
#---------------------------------------------


# CMakeのバージョンを設定（コマンドプロンプトで"cmake --version"で確認）
cmake_minimum_required(VERSION 3.25.1)

# プロジェクト名と使用する言語を設定
project(Ctetris)

# set(CMAKE_C_COMPILER /usr/bin/gcc)
# set(CMAKE_CXX_COMPILER /usr/bin/g++)

# サブディレクトリを登録
add_subdirectory(rev0.2)

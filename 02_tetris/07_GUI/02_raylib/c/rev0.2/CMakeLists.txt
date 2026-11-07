
# サブディレクトリを登録
add_subdirectory(block)
add_subdirectory(board)
add_subdirectory(collision)
add_subdirectory(input)
add_subdirectory(cycle)
add_subdirectory(game)
add_subdirectory(view)
# カレントディレクトリ
add_executable(main.out # 実行ファイル
        main.c # ソースファイル*
        settings.c
)

find_package(raylib CONFIG REQUIRED)

# 最適化(-O0:ほぼ最適化しない、-O1:軽い最適化、-O2:かなり積極的に最適化、-O3:-O2よりさらに速度重視)
target_compile_options(game PRIVATE -O0)
# target_compile_options(game PRIVATE -pg)
# target_compile_options(block PRIVATE -pg)
# target_compile_options(board PRIVATE -pg)
# target_compile_options(collision PRIVATE -pg)
# target_compile_options(input PRIVATE -pg)
# target_compile_options(cycle PRIVATE -pg)
# target_compile_options(view PRIVATE -pg)

# target_link_options(game PRIVATE -pg)

# サブディレクトリを紐づける
target_link_libraries(main.out
        PRIVATE game
        PRIVATE view
        PRIVATE raylib
)
# ※ main は一番外側の game だけに依存させるのが綺麗
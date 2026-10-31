
# サブディレクトリを登録
add_subdirectory(block)
add_subdirectory(board)
add_subdirectory(collision)
add_subdirectory(game)
add_subdirectory(input)

# カレントディレクトリ
add_executable(main.out # 実行ファイル 
        main.c # ソースファイル*
        settings.c
)

# 最適化(-O0:ほぼ最適化しない、-O1:軽い最適化、-O2:かなり積極的に最適化、-O3:-O2よりさらに速度重視)
target_compile_options(game PRIVATE -O0)
# target_compile_options(game PRIVATE -pg)
# target_compile_options(block PRIVATE -pg)
# target_compile_options(board PRIVATE -pg)
# target_compile_options(collision PRIVATE -pg)
# target_compile_options(input PRIVATE -pg)

# target_link_options(game PRIVATE -pg)

# サブディレクトリを紐づける
target_link_libraries(main.out 
        game
)
# ※ main は一番外側の game だけに依存させるのが綺麗
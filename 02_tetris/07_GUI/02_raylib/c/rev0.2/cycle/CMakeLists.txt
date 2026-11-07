# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE CYCLE_SOURCES *.c)

# domainフォルダ内に、静的ライブラリを作成する
add_library(cycle STATIC ${CYCLE_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(cycle
    PRIVATE block
    PRIVATE board
    PRIVATE collision
    PRIVATE input
    PRIVATE game
    PRIVATE view
)

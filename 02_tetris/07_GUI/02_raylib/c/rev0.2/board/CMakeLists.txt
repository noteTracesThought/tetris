# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE BOARD_SOURCES *.c)

# domainフォルダ内に、静的ライブラリを作成する
add_library(board STATIC ${BOARD_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(board
    PRIVATE block
    PRIVATE collision
    PRIVATE input
    PRIVATE cycle
    PRIVATE game
    PRIVATE view
)

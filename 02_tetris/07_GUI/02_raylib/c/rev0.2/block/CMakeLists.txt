# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE BLOCK_SOURCES *.c)

# domainフォルダ内に、静的ライブラリを作成する
add_library(block STATIC ${BLOCK_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(block
    PRIVATE board
    PRIVATE collision
    PRIVATE input
    PRIVATE cycle
    PRIVATE game
    PRIVATE view
)

# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE VIEW_SOURCES *.c)

# domainフォルダ内に、静的ライブラリを作成する
add_library(view STATIC ${VIEW_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(view
    PRIVATE block
    PRIVATE board
    PRIVATE collision
    PRIVATE input
    PRIVATE cycle
    PRIVATE game
)

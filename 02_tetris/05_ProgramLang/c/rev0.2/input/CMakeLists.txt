# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE INPUT_SOURCES *.c)

# domainフォルダ内に、静的ライブラリを作成する
add_library(input STATIC ${INPUT_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(input
    PRIVATE block
    PRIVATE board
    PRIVATE collision
    PRIVATE game
)

# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE GAME_SOURCES *.c)

# domainフォルダ内に、静的ライブラリを作成する
add_library(game STATIC ${GAME_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(game
    PRIVATE block
    PRIVATE board
    PRIVATE collision
    PRIVATE input
    PRIVATE cycle
)

# サブディレクトリ含め、フォルダ配下のcppファイルをコンパイルする
file(GLOB_RECURSE COLLISION_SOURCES *.cpp)

# domainフォルダ内に、静的ライブラリを作成する
add_library(collision STATIC ${COLLISION_SOURCES})

# 依存ルールをコンパイルで守る
target_link_libraries(collision
    PRIVATE block
    PRIVATE board
    PRIVATE game
    PRIVATE input
)

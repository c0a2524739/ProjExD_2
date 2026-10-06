import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate
def gameover(screen: pg.Surface) -> None:
    # 黒い背景
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(180)

    # GAME OVERの文字
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))

    # 泣いているこうかとんをロード
    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 1)

    # 黒い画面を表示
    screen.blit(black, (0, 0))

    # 左側の泣いているこうかとん
    screen.blit(
        kk_img,
        kk_img.get_rect(
            center=(WIDTH // 2 - 250, 200)
        )
    )

    # GAME OVER
    screen.blit(
        text,
        text.get_rect(
            center=(WIDTH // 2, 200)
        )
    )

    # 右側の泣いているこうかとん
    screen.blit(
        kk_img,
        kk_img.get_rect(
            center=(WIDTH // 2 + 250, 200)
        )
    )

    pg.display.update()

    # 5秒間表示
    time.sleep(5)

def get_kk_img(original_img: pg.Surface, sum_mv: list[int]) -> pg.Surface:
    """
    こうかとんの移動方向に応じて画像の向きを変更する。
    """

    if sum_mv == [0, -5]:          # 上
        return pg.transform.rotozoom(original_img, -90, 0.9)

    elif sum_mv == [0, 5]:         # 下
        return pg.transform.rotozoom(original_img, 90, 0.9)

    elif sum_mv == [5, 0]:        # 左
        return pg.transform.flip(original_img, True, False)

    elif sum_mv == [-5, 0]:         # 右
        return original_img

    elif sum_mv == [5, -5]:       # 左上
        img = pg.transform.rotozoom(original_img, -45, 0.9)
        return pg.transform.flip(img, True, False)

    elif sum_mv == [-5, -5]:        # 右上
        return pg.transform.rotozoom(original_img, -45, 0.9)

    elif sum_mv == [5, 5]:        # 左下
        img = pg.transform.rotozoom(original_img, 45, 0.9)
        return pg.transform.flip(img, True, False)

    elif sum_mv == [-5, 5]:         # 右下
        return pg.transform.rotozoom(original_img, 45, 0.9)

    else:                           # 動いていない
        return original_img 

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 練習2：空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2：赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 練習2：四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx, vy = +5, +5  # 練習2：爆弾の初期速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5



    
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
# 移動方向に合わせてこうかとんの向きを変更
        kk_img = get_kk_img(
            pg.image.load("fig/3.png"),
            sum_mv
        )
        kk_rct = kk_img.get_rect(center=kk_rct.center)
        kk_rct.move_ip(sum_mv)



        
        if check_bound(kk_rct) != (True, True):  # どこからしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先程の動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2：爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()  
    sys.exit()

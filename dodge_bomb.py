import random
import sys
import time
import pygame as pg

# 移動方向の設定
delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
        }


accs = [a for a in range(1, 11)]

# 画面判定
def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数１：画面SurfaceのRect
    引数２：こうかとん、または、爆弾SurfaceのRect
    戻り値：横方向、縦方向のはみだし判定結果（画面内：True／画面外：False
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    font1 = pg.font.SysFont("UDデジタル教科書体", 400)  # フォントの設定
    text1 = font1.render("Game Over", True, (255, 0, 0))  # テキストの設定
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾の描画
    bb_img.set_colorkey((0, 0, 0))  # クロマキー
    x, y = random.randint(0, 1600), random.randint(0, 900)
    vx, vy = +1, +1
    bb_rct = bb_img.get_rect()
    bb_rct.center = x, y
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0
        tmr += 1
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
        avx, avy = vx*accs[min(tmr//1000, 9)], vy*accs[min(tmr//1000, 9)]
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  
        if kk_rct.colliderect(bb_rct):  # 衝突処理
            screen.blit(text1, (40,300))  # ゲームオーバーテキスト表示
            pg.display.update()
            time.sleep(4)
            return
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
from playwright.sync_api import sync_playwright
import subprocess,os
FPS=30
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto('file://'+os.path.abspath('lb.html')); pg.wait_for_timeout(800)
    TOT=pg.evaluate('window.TOT'); n=int(TOT*FPS)
    ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart','lb_silent.mp4'],stdin=subprocess.PIPE)
    for f in range(n):
        pg.evaluate(f'render({f/FPS})')
        ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
    ff.stdin.close(); ff.wait(); b.close(); print(n,TOT)

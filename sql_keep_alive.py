import time

import app
while(1):
    app.cur.execute("SELECT 1")
    app.con.commit()
    time.sleep(60)

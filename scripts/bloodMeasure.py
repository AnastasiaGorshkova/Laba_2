import bloodFunctions as b
import time
b.initSpiAdc()
data = []
try:
    start = time.time()
    finish = time.time()
    while finish - start < 60:
        data.append(b.getAdc())
        finish = time.time()
finally:
    b.save(data, start, finish)
    b.deinitSpiAdc()

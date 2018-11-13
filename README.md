# Pipeline Tools

A set of scripts that can be used as reference / learning for vfx pipelines and tools

---

## moveTool.py

Modify the src\_folder to point to your main folder that contains a \_submit folder with quicktimes.


```python
print ("Logging to %s" % setupLogging())
logging.info("Move Tool Started")
src_folder=r'/Users/moliver/Desktop/personal/test'
moveQuicktimes(src_folder, wait_time=10)
```

To Execute:

```cmd
python moveTool.py
```


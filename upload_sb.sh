cd /home/pipeline/sailbuoy_download
/home/pipeline/sailbuoy_download/venv/bin/python  sailbuoy_download.py
rsync -r nrt/*.csv "pipeline@88.99.244.110:/data/sailbuoy/raw/"

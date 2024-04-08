cd /home/pipeline/sailbuoy_download
/home/pipeline/sailbuoy_download/venv/bin/python  sailbuoy_download.py
rsync -r nrt/*.csv "pipeline@16.170.107.21:/data/sailbuoy/raw/"

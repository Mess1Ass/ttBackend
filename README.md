退出venu<br>
deactivate<br>
服务器启动django项目流程<br>
进入toolBackend文件夹<br>
source venv/bin/activate<br>
pm2 start /root/timeTable/ttBackend/venv/bin/gunicorn \
  --name ttBackend \
  --interpreter none \
  -- --bind 0.0.0.0:3000 ttBackend.wsgi:application<br>
pm2 logs backend<br>
安装所需依赖（pip install -r requirements.txt ）<br>
确认 Nginx 已安装并运行：<br>
systemctl status nginx<br>
1. 新建Nginx配置文件<br>
在服务器上执行：<br>
sudo nano /etc/nginx/sites-available/ttbackend.conf<br>
写入以下配置内容<br>
server {<br>
    listen 80;<br>
    server_name ttapi.tool4me.cn;<br>
    location / {<br>
        proxy_pass http://127.0.0.1:3000;   # 你的Gunicorn运行在3000端口<br>
        proxy_set_header Host $host;<br>
        proxy_set_header X-Real-IP $remote_addr;<br>
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;<br>
        proxy_set_header X-Forwarded-Proto $scheme;<br>
    }<br>
}<br>
3. 建立软链接启用配置<br>
sudo ln -s /etc/nginx/sites-available/ttapi.conf /etc/nginx/sites-enabled/<br>
4. 测试配置是否正确<br>
sudo nginx -t<br>
5. 重启 Nginx<br>
sudo systemctl restart nginx<br>

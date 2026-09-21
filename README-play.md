# 一箭又一箭 Arrow Heart
## 项目简介
本项目是基于Pygame实现的“一箭又一箭”点击解谜小游戏。玩家点击棋盘上带方向的爱心箭头，若前方无其他箭头阻挡，则爱心飞出棋盘消除；如果前方存在阻挡，则爱心晃动提示，消耗一次失误机会。清空所有爱心即可通关进入下一关；失误次数耗尽，本关失败，可按R键重开。


---


## 开发环境
- Python版本：3.11+
- 依赖库：pygame 2.6.1


---


## **图片截图**
<img width="1002" height="790" alt="关卡1" src="https://github.com/user-attachments/assets/c7cb7164-8bd4-4ea9-965d-637050057f83" />
<img width="1002" height="790" alt="关卡2" src="https://github.com/user-attachments/assets/a2b1dfbd-ae07-4c37-997a-06b7814ff556" />
<img width="1002" height="790" alt="关卡3" src="https://github.com/user-attachments/assets/2a9b6928-f111-4da8-bd28-82df46d54358" />
<img width="1002" height="790" alt="成功 下一关" src="https://github.com/user-attachments/assets/13c265be-11a4-4ed7-afd2-a303ea248f52" />
<img width="1002" height="790" alt="失败  R返回" src="https://github.com/user-attachments/assets/9ec3dc61-c050-4135-9252-d7c8cc8645fe" />



---



##  **功能清单**
1. 包含开始界面、游戏界面、通关界面、失败界面
2. 上/下/左/右四个方向爱心箭头
3. 路径阻挡检测
4. 碰撞晃动动画
5. 界面展示关卡编号、剩余箭头、失误次数
6. 3个独立可通关关卡
7. R键重置关卡


---


## 安装与运行
1. 安装依赖
```bash
pip install pygame

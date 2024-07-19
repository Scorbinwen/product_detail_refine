# 营销图细节优化
## 优化方案：
 0. 使用SD inpaint低强度重绘商品主题和背景部分
 1. 使用SAM分割出商品主体部分
 2. 使用harris角点检测+opencv的findcounter得到更完整得文字细节mask
 3. 使用泊松融合的seamlessClone将参考图的mask部分融合到目标图中

## 运行
用于测试结果的图像在`example/`文件夹中
> python main.py

## 结果展示
前景背景贴图            |  SD Inpaint低幅度重绘前景背景 | 本算法优化细节结果
:-------------------------:|:-------------------------:|:-------------------------:
![1690784723456_3_ref](https://github.com/user-attachments/assets/6f16927f-6a8b-4259-bcf4-2606445449cf)|
![1690784723456_3](https://github.com/user-attachments/assets/632a1b53-c763-4364-95f3-4f6a7cd8c57c)|
![mix_clone](https://github.com/user-attachments/assets/4b086fb3-615e-40a3-8877-ef04dcf57a11)

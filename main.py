# 优化方案：
# 1. 使用SAM分割出商品主体部分
# 2. 使用harris角点检测+opencv的findcounter得到更完整得文字细节mask
# 3. 使用泊松融合的seamlessClone将参考图的mask部分融合到目标图中

# 1. 使用SAM分割出商品主体部分
# 该部分在Google Colab上运行得到的mask

# 2. 使用harris角点检测+opencv的findcounter得到更完整得文字细节mask
import cv2
import numpy as np
from os.path import join as opj
# 读入图像并转化为float类型，用于传递给harris函数
img = cv2.imread("example/1690784723456_3_ref.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_img = np.float32(gray_img)
# 对图像执行harris
blockSize = 2     # 邻域半径
apertureSize = 3  # 邻域大小
Harris_detector = cv2.cornerHarris(gray_img, blockSize, apertureSize, 0.04)

# 膨胀harris结果
dilate_kernel = np.ones((15, 15), np.uint8)
dst = cv2.dilate(Harris_detector, dilate_kernel)

openning_kernel = np.ones((20, 20), np.uint8)
dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, openning_kernel)
# 设置阈值
thres = 0.01 * dst.max()
# 使用SAM分割出商品主体mask makeup_mask.png
mask_img = cv2.imread("example/makeup_mask.png")
mask_img[dst < thres] = [0, 0, 0]
cv2.imwrite("example/makeup_harris_processed_mask.jpg", mask_img)

# 3. 尝试使用泊松融合的seamlessClone
import cv2
import numpy as np
src = cv2.imread('example/1690784723456_3_ref.png')
tgt = cv2.imread('example/harris_mask_inpaint.png')
mask = cv2.imread("example/makeup_harris_processed_mask.jpg")
src = cv2.resize(src, (tgt.shape[1], tgt.shape[0]))
mask = cv2.resize(mask, (tgt.shape[1], tgt.shape[0]))
invert_mask = mask

assert src.shape == tgt.shape

height, width, _ = tgt.shape
center = (width //2 - 3, height // 2+48)

dilate_kernel = np.ones((5, 5), np.uint8)
invert_mask = cv2.dilate(invert_mask, dilate_kernel)
cv2.imwrite("example/text_invert_mask.png", invert_mask)

# cv2.imwrite("example/text_mask.png", mask)
masked_src = src * (invert_mask != [0, 0, 0])
cv2.imwrite("example/masked_src.png", masked_src)
full_mask = 255 * np.ones(masked_src.shape, masked_src.dtype)
normal_clone = cv2.seamlessClone(masked_src, tgt, invert_mask, center, cv2.NORMAL_CLONE)
cv2.imwrite('example/normal_clone.png', normal_clone)
# max_clone
max_clone = cv2.seamlessClone(masked_src, tgt, invert_mask, center, cv2.MIXED_CLONE)
cv2.imwrite('example/mix_clone.png', max_clone)

# 后续优化==> 使用直方图均衡先预处理参考图，使得更多暗处的文字细节也能够检测出。

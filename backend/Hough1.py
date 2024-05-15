import cv2
import numpy as np


def test_show(img, name="output"):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 检查椭圆
def tuoyuan(img):
    if_tuoyuan = False
    binary = cv2.Canny(img, 30, 200)
    # test_show(binary, "Canny")
    cnt, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_width, min_height = img.shape[0] * 0.48, img.shape[0] * 0.48  # 椭圆最小大小
    max_width, max_height = img.shape[0] * 0.85, img.shape[0] * 0.85  # 椭圆最大大小
    min_distance = img.shape[0] * 0.4  # 椭圆中心之间的最小间隔
    center_point = []
    for i in range(len(cnt)):
        # 椭圆拟合
        # print(i, len(cnt[i]))
        if len(cnt[i]) >= 5:
            # print(cnt[i])
            max_x, max_y = 0, 0
            min_x, min_y = img.shape[0], img.shape[1]
            for k in range(len(cnt[i])):
                # cnt示例:
                # [[[726 748]]
                #  [[726 749]]
                #  [[727 748]]
                #  [[728 749]]
                #  [[728 748]]]
                if cnt[i][k][0][0] > max_x:
                    max_x = cnt[i][k][0][0]
                if cnt[i][k][0][1] > max_y:
                    max_y = cnt[i][k][0][1]
                if cnt[i][k][0][0] < min_x:
                    min_x = cnt[i][k][0][0]
                if cnt[i][k][0][1] < min_y:
                    min_y = cnt[i][k][0][1]
            '''print(max_x - min_x, min_width, max_width)
            print(max_y - min_y, min_height, max_height)
            test = copy.copy(img)
            ellipse = cv2.fitEllipse(cnt[i])
            cv2.ellipse(test, ellipse, (0, 255, 255), 2)
            test_show(test)'''
            if max_width >= max_x - min_x >= min_width and max_height >= max_y - min_y >= min_height:
                if len(center_point) == 0:
                        center_point.append([(max_x - min_x) / 2, (max_y - min_y) / 2])
                        print("检测到：中心", center_point)
                        ellipse = cv2.fitEllipse(cnt[i])
                        # 绘制椭圆
                        cv2.ellipse(img, ellipse, (0, 255, 255), 2)
                        if_tuoyuan = True
                        test_show(img)
                else:
                    too_close = False
                    for point in center_point:
                        if ((max_x - min_x) / 2 - point[0]) ** 2 + ((max_y - min_y) / 2 - point[1]) ** 2\
                                <= min_distance ** 2:
                            too_close = True
                    if not too_close:
                        center_point.append([(max_x - min_x) / 2, (max_y - min_y) / 2])
                        # print(center_point)
                        ellipse = cv2.fitEllipse(cnt[i])
                        # 绘制椭圆
                        cv2.ellipse(img, ellipse, (0, 255, 255), 2)
                        if_tuoyuan = True
                        test_show(img)
    return if_tuoyuan

def hough(image):
    # 转换为灰度图像
    gary_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊以减少图像噪声
    blurred = cv2.GaussianBlur(gary_image, (5, 5), 0)

    gary_image = cv2.Canny(gary_image, 100, 200)
    # 假设你知道图像中圆形的大致半径范围
    min_radius = int(20)  # 最小半径
    max_radius = int(80)  # 最大半径
    # 使用霍夫圆检测
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT,
                               dp=1, minDist=int((min_radius + max_radius) / 2),
                               param1=65, param2=70,  # 1太高漏检，2太低错检太高漏检
                               minRadius=min_radius, maxRadius=max_radius)

    results = []
    # 确保找到了圆
    if circles is not None:
        # 将坐标和半径从浮点数转换为整数
        circles = np.uint16(np.around(circles))

        # 遍历检测到的每个圆
        for (x, y, radius) in circles[0, :]:
            # 计算包含圆的边界框（这里简单地使用半径的两倍作为宽高，并适当外扩）
            left = max(0, int(x - 1.5 * radius))
            top = max(0, int(y - 1.5 * radius))
            right = min(gary_image.shape[1], int(x + 1.5 * radius))
            bottom = min(gary_image.shape[0], int(y + 1.5 * radius))

            # 裁剪出包含圆的图像区域
            circle_roi = image[top:bottom, left:right]
            # 在裁剪区域中检测椭圆，如果有结果，椭圆检测中画黄色椭圆，下面画绿色霍夫圆，并显示
            if_tuoyuan = tuoyuan(circle_roi)
            # 绘制圆形和圆心（仅用于调试，可以注释掉）
            # cv2.circle(circle_roi, (x - left, y - top), radius, (0, 255, 0), 2)
            # cv2.circle(circle_roi, (x - left, y - top), 2, (0, 0, 255), -1)

            # test_show(circle_roi, f'{x},{y}, {if_tuoyuan}')

            if if_tuoyuan:
                results.append(image[top:bottom, left:right])

    return results


# Test
img_path = "D:\PyProjcet\\traffic_signal_recognition_system_taotao\\backend\gtsrb\\test_imgs\\RealImg1.jpg"

image = cv2.imread(img_path)
# 确保图片读取成功
if image is None:
    print("Error: Could not read the image.")
    exit()

image = image.astype(np.uint8)
test_show(image, "Original")

hough(image)

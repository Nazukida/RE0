#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui_c.h>

using namespace cv;

int main()
{
    // 使用Mat类型来储存图片的数据
    // 图片的读取就要使用到imread函数
    Mat img = imread("20241227185637.jpg"); // 注意：图片要在当前文件夹中才能直接这么写，否则要加上路径

    if (img.empty())
    {
        std::cout << "mat::" << std::endl;
        return -1;
    }
    return 0;
}
#Project2 编程画一个真实感静态景物
- 16307130201 肖起凡
##内容组成
- main.py：主程序，实现绘制真实感静态景物的功能。
- texture.png：程序中必需的图形文件。
##依赖关系
- Python$\geq3.7$
- Numpy$\geq1.15.2$
- PyOpenGL$\geq3.1.3$
- matplotlib
##程序说明
- 正常运行程序会生成加上纹理的$3D$花瓶，可以通过修改参数改变输出的$3D$实物类型。
	- "-t"与"--texture"：值非'n'时会为物品添加纹理，值为'n'时不会为物品添加纹理。预设值为'y'。
	- "-o"与"--object"：值为'Vase'时会生成花瓶，值为'Ball'时会生成球体，值为其它值时会报错并结束程序。预设值为'Vase'。
##算法原理
- 利用PyOpenGL旋转坐标系并预设光源位置，然后将预设的纹理图片导入并与PyOpenGL使用的默认纹理绑定，最后利用PyOpenGL提供的GL_POLYGON类型2D图形在3D坐标系上绘制若干个圆形拼接成目标3D图形。
##参考文献
- OpenGL官方文档：http://pyopengl.sourceforge.net/documentation/
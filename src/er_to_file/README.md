## er_to_file.py使用说明

### 功能说明：
* 该工具旨在简化从oracle导出ER结构并保存到Word的繁琐步骤,极大地节省时间。
* 人生短暂，将更多的时间投入到更有意义的事情中。

* 目前实现了基本功能
    * 2018-10-12
        * 修复TIMESTAMP类型在导出ER表到word时的双括号问题。  
    
    * 2018-10-10
        * ER表的'字段释义'列取自comments
        * ER表的'备注'列目前只标注了是否非空
        * 表名称大纲级别和表头填充色暂时不能设置

### 1. 环境准备
* Python3.x.x
* Python库：cx_Oracle, python-docx, DBUtils

### 2. 使用设置
* 将*er_to_file.py* 和 *orcl_pools.py* 放在同一目录下;
* 用文本编辑器打开*er_to_file.py*
    * 修改orcl_cfg配置，该配置为连接oracle数据库的相关信息；
    * 修改tbl_names，该配置中填写的是要导出ER结构的表,  
      若tbl_names没有填写表名称，则程序默认导出所有表ER结构。
   
### 3. 开始使用
* 切换到*er_to_file.py* 所在目录，运行  
  ```python er_to_file.py```
* 执行完成后会在 *er_to_file.py* 同级目录下生成 *ER.doc* 文件。

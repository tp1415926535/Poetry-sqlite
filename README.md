# Poetry-sqlite
Poetry库的古诗词转sqlite数据库

# 前言
* 本项目将 [Poetry](https://github.com/Werneror/Poetry) 项目的csv文件合并为 sqlite 本地数据库，方便查询。
* [当前项目](https://github.com/tp1415926535/Poetry-sqlite) 是基于 [Poetry](https://github.com/Werneror/Poetry) 项目的数据（csv文件）。      
  另外我还写了个项目 [Chinese-poetry-json2sqlite](https://github.com/tp1415926535/Chinese-poetry-json2sqlite) 是基于 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 项目的数据（json文件）。      
  都是将诗词库转为sqlite本地数据库。
  
# 使用方法
* **方法1**：下载本项目的[Release](https://github.com/tp1415926535/Poetry-sqlite/releases/latest)的成品数据库文件。    
* **方法2**：下载本项目文件，和最新版的 Poetry 项目文件，修改 poetryConfig.json 配置文件。然后运行 py 脚本，或者封装好的 exe 即可。目前生成数据库耗时在十几秒左右。

## 配置文件说明
文件 **“poetryConfig.json”** ，需要跟python脚本或者exe放在同一个目录下。       
因为数据源格式比较规范，没什么好配置的，只设置输入和输出路径。     
其中 ["dbPath"] 的值为输出的sqlite文件路径，  ["dataSourceFolder"] 的值改为 Poetry 项目文件夹路径：
```json
{
  "dbPath":"poetry.db",
  "dataSourceFolder":"D:/Poetry-master"
 }
```

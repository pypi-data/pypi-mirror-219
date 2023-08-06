import os
import platform
import inspect
import sys
import zipfile
import subprocess

class IO:
    """
    @author noobug 
    @desc IO类提供生成数据文件的所有功能
    """

    def __init__(self, data_count, prefix="", std="std", save_path="tmp/", suffix_in=".in", suffix_out=".out", debug=True):
        """
        @data_count 数据点个数，必填！
        @prefix 生成文件的前缀名，默认空
        @std 标程名称，windows下会自动带上.exe
        @save_path 指定生成数据文件存放的路径，必须以/结尾，默认tmp文件夹
        @suffix_in 指定输入文件的后缀名，默认.in
        @suffix_out 指定输出文件的后缀名，默认.out
        @debug 默认开启显示数据生成进度，设置为False关闭
        """
        assert data_count > 0
        self.debug = debug
        self.IN = []
        self.OUT = []
        self.FILES = []
        self.suffix_in = suffix_in
        self.suffix_out = suffix_out
        # self.funclist = [None for _ in range(MAX_DATA_COUNT+5)]
        self.prefix = prefix
        self.data_count = data_count

        # 处理保存路径
        if os.path.isabs(save_path):
            self.save_path = save_path
        else:
            sp = self.getRunningScriptPath()
            self.save_path = os.path.join(sp, save_path)

        # os.path.abspath(sys.argv[0])
        if platform.system() == "Windows":
            if std.endswith(".exe"):
                self.std = std
            else:
                self.std = std + ".exe"
        else:
            self.std = std

        # 处理std路径
        if not os.path.isabs(self.std):
            sp = self.getRunningScriptPath()
            self.std = os.path.join(sp, self.std)

    # 获取当前执行文件所在目录
    def getRunningScriptPath(self):
        p = os.path.abspath(sys.argv[0])
        return os.path.split(p)[0]

    def resetIO(self):
        self.IN = []
        self.OUT = []

    def write(self, *params, **keys):
        l = len(self.IN)
        if l == 0:
            self.IN.append([])
        arr = self.IN[-1]
        arr.extend(params)
    
    def writeln(self, *params):
        l = len(self.IN)
        if l == 0:
            self.IN.append([])
        arr = self.IN[-1]
        arr.extend(params)
        self.IN.append([])

    def _writeDataIntoFile(self, fp, data):
        t = type(data)
        if t is str:
            data = data.strip()
            fp.write(str(data))
            fp.write(" ")
        elif t is list or t is tuple:
            for d in data:
                self._writeDataIntoFile(fp, d)
        else:
            fp.write(str(data))
            fp.write(" ")

    def _processData(self, func, id, isdefault):
        self.resetIO()
        if isdefault:
            func(id)
        else:
            func(id)
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        fname = f"{self.prefix}{id}{self.suffix_in}"
        finpath = os.path.join(self.save_path,fname)
        with open(finpath, "w", encoding="UTF-8") as f:
            lim = len(self.IN)
            for i,a in enumerate(self.IN):
                self._writeDataIntoFile(f, a)
                if i < lim-1:
                    f.write("\n")

        foutname = f"{self.prefix}{id}{self.suffix_out}"
        foutpath = os.path.join(self.save_path,foutname)

        if platform.system() == "Windows":
            ret = subprocess.run([self.std, "<", finpath, ">", foutpath], shell=True)
            if ret.returncode != 0:
                if self.debug: print(ret)
        else:
            os.system(f"\"{self.std}\" < \"{finpath}\" > \"{foutpath}\"")
        self.FILES.append(finpath)
        self.FILES.append(foutpath)
        
    def done(self, o, zip=False):
        '''
        开始根据配置生成数据，需传入一个对象实例。
        '''
        if self.debug: print(f"=========OJUtil生成数据==========")
        for i in range(1, self.data_count+1):
            if self.debug: print(f">>> 生成第 {i} 个数据点...", end="")
            fname = f"data_{i}"
            if hasattr(o, fname):
                f = getattr(o, fname)
                if inspect.ismethod(f):
                    self._processData(f, i, False)
            else:
                if hasattr(o, "default"):
                    f = getattr(o, "default")
                    if inspect.ismethod(f):
                        self._processData(f, i, True)
            if self.debug: print(f"OK. <<<")
        if self.debug: print(f"=========数据已生成完毕==========")

        if zip:
            zipname = self.prefix
            if zipname == None or zipname == "": 
                zipname = "data.zip"
            else:
                zipname += ".zip"
            zippath = os.path.join(self.save_path, zipname)
            zz = zipfile.ZipFile(zippath, "w")
            for x in self.FILES:
                if os.path.exists(x):
                    zz.write(x, arcname=os.path.split(x)[1])
            zz.close()
            if self.debug: print(f"=========压缩完毕==========")
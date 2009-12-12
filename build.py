#!/usr/bin/env python

import os
from zipfile import ZipFile, BadZipfile

class Builder:
    
    javascript_files = []
    extra_zip_files = []

    def __init__(self, build_folder='Build/', minify_postfix='min', extension='js'):
        self.minify_posfix = minify_postfix
        self.build_folder = build_folder
        self.extension = '.' + extension
                
    def add_files(self, list_name, files, root='', path='', extension=''):
        if type(files) == dict:
            for key in files.keys():
                self.add_files(list_name, files[key], root, path=path + key + '/', extension=extension)
        elif type(files) == list or type(files) == tuple:
            for _file in files:
                getattr(self, list_name).append((_file, root + path + _file + extension))
        elif type(files) == str:
            getattr(self, list_name).append((files, root + path + files + extension))
            
    def read_file(self, _file):
        f = open(_file,'r')
        ret = []
        try:
            ret = f.readlines()
        finally:
            f.close()
        ret.append('\r\n')
        return ret

    def create_built_file(self):
        file_name = self.build_folder + self.file_name + self.extension
        built_file = open(file_name, 'w+')
        try:
            for name, absolute_name in self.javascript_files:
                built_file.writelines(self.read_file(absolute_name))
        finally:
            built_file.close()
        print '** Succesfully created "' + file_name + '" file. **'
    
    def create_minified_file(self):
        uncompressed_file = self.build_folder + self.file_name + self.extension 
        compressed_file = self.build_folder + self.file_name + '.' + self.minify_posfix + self.extension
        os.system('java -jar ../../assets/yui-compressor/yui.jar --warn --charset utf8 %(uncompressed)s >> %(compressed)s' % {
            'uncompressed': uncompressed_file,
            'compressed': compressed_file
        })
        print '** Succesfully created minified file. **'
        
    def build(self, file_name, files, root='Source/'):
        self.file_name = file_name
        try:
            os.mkdir(self.build_folder)
        except OSError:
            # ok the folder might be still there
            pass
        self.add_files('javascript_files', files, root=root, extension=self.extension)
        
        print 'Starting to build ' + file_name + ' files...'
        self.create_built_file()
        self.create_minified_file()
        print ''
        
        self.javascript_files = []
    
if __name__ == '__main__':
    builder = Builder()
    builder.build('Meio.Mask', (
        'Meio.Mask',
        'Meio.Mask.Fixed',
        'Meio.Mask.Reverse',
        'Meio.Mask.Repeat',
        'Meio.Mask.Regexp',
        'Meio.Mask.Extras'
    ))
    